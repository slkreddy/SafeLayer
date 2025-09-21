from .base import BaseGuard
import re

PROFANITY = {"damn", "crap", "shit", "fuck"}
PROF_RE = re.compile(r'\b(' + '|'.join(re.escape(w) for w in PROFANITY) + r')\b', re.I)

class ToneGuard(BaseGuard):
    def __init__(self, warn_only=True, explain=False):
        super().__init__(explain)
        self.warn_only = warn_only

    def check(self, text):
        results = []
        for m in PROF_RE.finditer(text):
            results.append({
                "entity": "profanity",
                "start": m.start(),
