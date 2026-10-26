import os
import time
from typing import Optional, List
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for YouTube Data API v3 upload
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "token.json"
FORCE_REAUTH = os.getenv("YOUTUBE_FORCE_REAUTH", "").lower() in {"1", "true", "yes"}

class YouTubeUploader:
    def __init__(self):
        self.youtube = self._authenticate()

    def _authenticate(self):
        """Authenticates with YouTube API using OAuth 2.0."""
        creds = None

        if FORCE_REAUTH and os.path.exists(TOKEN_FILE):
            print("Force re-auth is enabled. Clearing saved token.json to sign in with a new Google account.")
            os.remove(TOKEN_FILE)
        
        # Load existing token if available
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # If no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(f"Missing {CLIENT_SECRETS_FILE}. Please download it from Google Cloud Console.")
                
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for next time
            with open(TOKEN_FILE, "w", encoding="utf-8") as token_file:
                token_file.write(creds.to_json())
                
        return build("youtube", "v3", credentials=creds)

    def upload_video(self, file_path: str, title: str, description: str, category: str, tags: List[str], privacy: str, thumbnail_path: Optional[str] = None, retries: int = 3) -> str:
        """Uploads a video to YouTube with automatic retries for temporary errors."""
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy
            }
        }

        error_msg = ""
        for attempt in range(retries):
            try:
                media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
                request = self.youtube.videos().insert(
                    part=",".join(body.keys()),
                    body=body,
                    media_body=media
                )
                
                response = None
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        print(f"\rUploading... {progress}%", end="", flush=True)
                
                print("\rUploading... 100%")
                video_id = response.get("id")
                
                if thumbnail_path and os.path.exists(thumbnail_path):
                    print(f"Uploading custom thumbnail...")
                    try:
                        self.youtube.thumbnails().set(
                            videoId=video_id,
                            media_body=MediaFileUpload(thumbnail_path)
                        ).execute()
                        print("Thumbnail uploaded successfully.")
                    except Exception as e:
                        print(f"Failed to upload thumbnail: {e}")
                
                return video_id
                
            except HttpError as e:
                error_msg = f"HTTP Error {e.resp.status}: {e.content}"
                print(f"\nUpload failed (attempt {attempt + 1}/{retries}): {error_msg}")
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))  # Exponential backoff
                    
            except Exception as e:
                error_msg = str(e)
                print(f"\nUnexpected error (attempt {attempt + 1}/{retries}): {error_msg}")
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))
                    
        raise Exception(f"Failed to upload after {retries} retries. Last error: {error_msg}")
