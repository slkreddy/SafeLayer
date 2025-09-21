import re
from .base import BaseGuard

try:
    from presidio_analyzer import AnalyzerEngine
    PRESIDIO = True
except ImportError:
    PRESIDIO = False

EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'\b\d{10}\b')

class PIIGuard(BaseGuard):
    def __init__(self, mask=True, explain=False):
        super().__init__(explain)
        self.mask = mask
        self.engine = AnalyzerEngine() if PRESIDIO else None

    def check(self, text: str):
        results = []
        if PRESIDIO and self.engine:
            hits = self.engine.analyze(text=text, entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], language="en")
            for h in hits:
                results.append({"entity": h.entity_type, "start": h.start, "end": h.end, "explanation": f"Presidio: {h.entity_type} @ {h.start}-{h.end}"})
        else:
            for m in EMAIL_RE.finditer(text):
                results.append({"entity": "email", "start": m.start(), "end": m.end(), "explanation": f"EMAIL: {m.group()} @ {m.span()}"})
            for m in PHONE_RE.finditer(text):
                results.append({"entity": "phone", "start": m.start(), "end": m.end(), "explanation": f"PHONE: {m.group()} @ {m.span()}"})
        return results

    def mask(self, text: str) -> str:
        text = EMAIL_RE.sub("[EMAIL MASKED]", text)
        return PHONE_RE.sub("[PHONE MASKED]", text)
