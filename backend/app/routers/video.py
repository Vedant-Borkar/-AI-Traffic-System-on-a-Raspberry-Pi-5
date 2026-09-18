import cv2
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import logging

logger = logging.getLogger(__name__)

# Create a new router for video streaming
video_router = APIRouter()

class VideoStreamer:
    def __init__(self):
        self.caps = {}  # Store video captures for each approach
        
    async def get_video_stream(self, approach: str):
        """Generate video stream with YOLO detection overlay"""
        try:
            # Get the video source for this approach
            video_source = await self._get_video_source(approach)
            if not video_source:
                raise HTTPException(status_code=404, detail=f"No video source for {approach}")
            
            # Open video capture
            cap = cv2.VideoCapture(video_source)
            if not cap.isOpened():
                raise HTTPException(status_code=500, detail=f"Failed to open video for {approach}")
            
            self.caps[approach] = cap
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    # Loop video when ended
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Process frame with YOLO detection (you can integrate your detector here)
                processed_frame = await self._process_frame(frame, approach)
                
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', processed_frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                # Small delay to control frame rate
                await asyncio.sleep(0.03)  # ~30 FPS
                
        except Exception as e:
            logger.error(f"Video streaming error for {approach}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _get_video_source(self, approach: str) -> str:
        """Get video source path for the given approach"""
        # You can get this from your system_state or config
        # For now, using the uploaded files path
        import os
        video_path = f"uploads/{approach}.mp4"
        if os.path.exists(video_path):
            return video_path
        return None
    
    async def _process_frame(self, frame, approach: str):
        """Process frame with vehicle detection and counting"""
        try:
            # Get current counts for this approach from system state
            from app.models.state import system_state
            from app.websocket_manager import broadcaster
            
            # You can integrate your YOLO detector here
            # For now, we'll just draw basic info on the frame
            
            # Get current vehicle counts
            counts = system_state.live_counts.get(approach, {})
            total_vehicles = counts.get('total', 0)
            
            # Add text overlay
            cv2.putText(frame, f"{approach.upper()} - Vehicles: {total_vehicles}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Add approach direction indicator
            direction_indicators = {
                "north": "⬆️ NORTH",
                "south": "⬇️ SOUTH", 
                "east": "➡️ EAST",
                "west": "⬅️ WEST"
            }
            
            cv2.putText(frame, direction_indicators.get(approach, approach.upper()),
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            return frame
            
        except Exception as e:
            logger.error(f"Frame processing error: {e}")
            return frame

# Create global video streamer instance
video_streamer = VideoStreamer()

@video_router.get("/video_feed/{approach}")
async def video_feed(approach: str):
    """Video streaming route for each approach"""
    return StreamingResponse(
        video_streamer.get_video_stream(approach),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# Include the video router in your main app
# Add this to your main.py after creating the FastAPI app