# YouTube Auto Uploader

This project uploads a sequence of gameplay videos to YouTube automatically using the YouTube Data API v3. It reads your video files in order, creates titles and descriptions, and uploads each one with a configurable delay between uploads.

## How it works

1. The script loads the settings from `config.json`.
2. It authenticates with your YouTube account using the OAuth client credentials in `client_secret.json`.
3. It looks through your `YouTube Videos` folder and sorts the `.mp4` files alphabetically.
4. For each video, it builds the next title and description based on your starting values and a number pattern.
5. It uploads the video, optionally attaches a thumbnail, and records the uploaded file in a local log.
6. If you run the script again, it skips files already uploaded and continues from the correct level.

## Features
- Automatic title/description progression
- Resume-safe uploading using a local log
- Ordered video processing by filename
- Optional thumbnail support
- Configurable wait time between uploads
- YouTube category, privacy, and tags support

## Project structure
- `main.py` — main program entry point
- `config.py` — loads the configuration file
- `youtube_uploader.py` — handles upload/auth logic
- `title_generator.py` — builds the next video title and description
- `thumbnail_generator.py` — prepares thumbnails
- `logger.py` — tracks uploaded files and logs activity
- `config.example.json` — sample configuration template

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Google OAuth credentials
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project.
3. Enable the YouTube Data API v3.
4. Create an OAuth client ID for a desktop app.
5. Download the JSON file and save it as `client_secret.json` in the project root.

### 3. Create your local config file
Make a copy of `config.example.json` and rename it to `config.json`.

```bash
copy config.example.json config.json
```

Then edit the values in `config.json`:
- `video_folder` — folder containing your videos
- `upload_interval` — seconds between uploads
- `category` — YouTube category ID
- `privacy` — `public`, `private`, or `unlisted`
- `tags` — relevant keywords
- `starting_title` — first title for your upload batch
- `starting_description` — first description for your upload batch

### 4. Add your videos
Place all `.mp4` files inside the folder named `YouTube Videos`.

### 5. Run the uploader
```bash
python main.py
```

The first time you run it, a browser window will open so you can log in to your Google account and allow access. The app will create a local `token.json` file for future runs.

## Important for GitHub
The following files are intentionally excluded from GitHub using `.gitignore` because they contain personal or local data:
- `client_secret.json`
- `token.json`
- `config.json`
- `descration.txt`
- `upload_log.txt`
- `YouTube Videos/`
- `video_Theminal/`

This keeps your channel credentials, video content, and personal upload data off the public repository while keeping the project code intact.

## Notes
- If you want to start a new batch, change the title/description in `config.json` or `descration.txt` and run the script again.
- The app automatically keeps the level number moving forward for each new upload.
- The log prevents re-uploading the same file if the script is restarted.

