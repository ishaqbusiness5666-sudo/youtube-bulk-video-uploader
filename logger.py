import os
import datetime
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

class Logger:
    def __init__(self, log_file: str = "upload_log.txt"):
        self.log_file = log_file

    def _write_to_file(self, message: str) -> None:
        """Appends a message to the log file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def log_success(self, filename: str, video_id: str) -> None:
        """Logs a successful upload both to the file and console."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] SUCCESS - File: {filename} - Video ID: {video_id}"
        self._write_to_file(log_entry)
        
        print(f"{Fore.GREEN}Upload Successful{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Video ID: {video_id}{Style.RESET_ALL}\n")

    def log_error(self, filename: str, error_msg: str) -> None:
        """Logs a failed upload both to the file and console."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ERROR - File: {filename} - Error: {error_msg}"
        self._write_to_file(log_entry)
        
        print(f"{Fore.RED}Upload Failed for {filename}{Style.RESET_ALL}")
        print(f"{Fore.RED}Error: {error_msg}{Style.RESET_ALL}\n")

    def log_skip(self, filename: str) -> None:
        """Logs when a file is skipped because it was already uploaded."""
        print(f"{Fore.YELLOW}Skipping already uploaded video: {filename}{Style.RESET_ALL}")

    def info(self, message: str) -> None:
        """Prints an informational message in cyan."""
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    def get_uploaded_files(self) -> set:
        """Reads the log file to determine which videos have already been uploaded."""
        uploaded = set()
        if not os.path.exists(self.log_file):
            return uploaded
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if "SUCCESS" in line:
                    # Parse the successful log entry to extract the filename
                    # Format: [2023-10-15 12:00:00] SUCCESS - File: video21.mp4 - Video ID: abcdefg
                    parts = line.split(" - ")
                    for part in parts:
                        if part.startswith("File:"):
                            filename = part.replace("File:", "").strip()
                            uploaded.add(filename)
        return uploaded
