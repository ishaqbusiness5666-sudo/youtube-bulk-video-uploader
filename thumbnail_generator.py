import cv2
import os

def extract_thumbnail(video_path: str, output_path: str = "temp_thumbnail.jpg") -> str:
    """
    Extracts a frame exactly 3 seconds before the end of the video.
    Returns the path to the extracted image.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Failed to open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if fps <= 0:
        fps = 30  # Fallback just in case

    # Calculate the frame 3 seconds before the end
    target_frame = max(0, total_frames - int(3 * fps))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()
    
    if not ret:
        cap.release()
        raise Exception(f"Failed to read frame {target_frame} from {video_path}")
        
    cv2.imwrite(output_path, frame)
    cap.release()
    
    return output_path
