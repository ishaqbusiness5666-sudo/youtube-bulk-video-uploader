import re
from typing import Tuple, Optional

class TitleGenerator:
    def __init__(self, starting_title: str, starting_description: str):
        self.current_title = starting_title
        self.current_description = starting_description
        self.current_level = self._extract_level(starting_title)

    def _extract_level(self, text: str) -> Optional[int]:
        """Finds the level number that comes after the word 'level' (case-insensitive)."""
        # First try to find the number after "level"
        match = re.search(r'level\s+(\d+)', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Fallback to first number if "level" keyword is not found
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return None

    def _update_text(self, text: str, old_level: int, new_level: int) -> str:
        """Replaces the level number that comes after 'level' keyword."""
        if old_level is None:
            return text
        
        # First try to replace the number that comes after "level"
        pattern = r'(level\s+)' + str(old_level) + r'\b'
        result = re.sub(pattern, lambda m: m.group(1) + str(new_level), text, flags=re.IGNORECASE)
        
        # If no replacement was made (no "level" keyword found), use the original number replacement
        if result == text:
            pattern = r'\b' + str(old_level) + r'\b'
            result = re.sub(pattern, str(new_level), text)
        
        return result

    def get_current_metadata(self) -> Tuple[str, str]:
        """Returns the current title and description."""
        return self.current_title, self.current_description

    def advance_to_next_level(self) -> None:
        """Increments the level number and updates title and description."""
        if self.current_level is not None:
            next_level = self.current_level + 1
            self.current_title = self._update_text(self.current_title, self.current_level, next_level)
            self.current_description = self._update_text(self.current_description, self.current_level, next_level)
            self.current_level = next_level
