import os
from config import load_config
from logger import Logger
from title_generator import TitleGenerator
from youtube_uploader import YouTubeUploader
from thumbnail_generator import extract_thumbnail

def main():
    logger = Logger()
    
    logger.info("Loading configuration...")
    try:
        config = load_config()
    except Exception as e:
        logger.log_error("config.json", f"Failed to load config: {e}")
        return

    logger.info("Authenticating with YouTube API...")
    try:
        uploader = YouTubeUploader()
        logger.info("Successfully authenticated!")
    except Exception as e:
        logger.log_error("Authentication", f"Failed to authenticate: {e}")
        return

    video_folder = config.video_folder
    thumbnail_folder = "video_Theminal"
    
    # Check if folder exists, if not create it
    if not os.path.exists(video_folder):
        logger.info(f"Video folder '{video_folder}' does not exist. Creating it now.")
        os.makedirs(video_folder)
        logger.info(f"Please place your .mp4 videos inside the '{video_folder}' folder and run the script again.")
        return

    os.makedirs(thumbnail_folder, exist_ok=True)

    # Discover and sort MP4 files alphabetically to preserve order
    videos = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]
    videos.sort()

    thumb_files = sorted([
        f for f in os.listdir(thumbnail_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

    if not videos:
        logger.info(f"No .mp4 files found in '{video_folder}'. Please add some videos.")
        return

    total_videos = len(videos)
    logger.info(f"Found {total_videos} videos in '{video_folder}'.")

    # Read log to know which ones we've already successfully uploaded
    uploaded_files = logger.get_uploaded_files()
    
    print("\n" + "="*50)
    starting_title = input("Enter the starting title (e.g. Brain Out Level 21 Solution): ")
    print("="*50 + "\n")
    
    # Read starting description from descration.txt
    desc_path = "descration.txt"
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            starting_description = f.read()
        logger.info(f"Loaded description from '{desc_path}'")
    else:
        logger.info(f"'{desc_path}' not found. Using empty description.")
        starting_description = ""

    title_gen = TitleGenerator(starting_title, starting_description)

    # Process each video
    for i, video_file in enumerate(videos, 1):
        # If uploaded previously, skip the actual upload but STILL advance the level numbers
        # so the next video gets the correct title/description
        if video_file in uploaded_files:
            logger.log_skip(video_file)
            title_gen.advance_to_next_level()
            continue

        title, description = title_gen.get_current_metadata()
        
        print("-" * 50)
        logger.info(f"Progress: {i}/{total_videos} | Remaining: {total_videos - i} | Uploading file: {video_file}")
        logger.info(f"Title:\n{title}\n")
        
        file_path = os.path.join(video_folder, video_file)
        thumb_path = None
        if i - 1 < len(thumb_files):
            thumb_path = os.path.join(thumbnail_folder, thumb_files[i - 1])
            logger.info(f"Using thumbnail: {thumb_path}")
        
        try:
            # Attempt to upload video
            video_id = uploader.upload_video(
                file_path=file_path,
                title=title,
                description=description,
                category=config.category,
                tags=config.tags,
                privacy=config.privacy,
                thumbnail_path=thumb_path
            )
            
            # Log success
            logger.log_success(video_file, video_id)
            
        except Exception as e:
            logger.log_error(video_file, str(e))
            logger.info("Stopping execution due to fatal upload failure.")
            break

        # Always advance to the next level whether it succeeded or failed,
        # but if we broke the loop on error, it doesn't matter much. 
        # By doing it here, we prepare for the next video properly.
        title_gen.advance_to_next_level()
        
    logger.info("All finished!")

if __name__ == "__main__":
    main()
