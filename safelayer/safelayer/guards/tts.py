from .base import BaseGuard
import re

INVALID_TTS_PATTERNS = [r'<[^>]*script', r'[^\x00-\x7F]+']

class TTSGuard(BaseGuard):
    def __init__(self, explain=False):
        super().__init__(explain)

    def check(self, text):
        results = []
        for pattern in INVALID_TTS_PATTERNS:
            if re.search(pattern, text, re.I):
                results.append({"entity": "invalid_tts", "pattern": pattern, "explanation": f"Invalid pattern matched: {pattern}"})
        return results

    def mask(self, text):
        t = re.sub(INVALID_TTS_PATTERNS[0], "", text)
        t = re.sub(INVALID_TTS_PATTERNS[1], "", t)
        return t
