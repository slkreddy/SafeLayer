from safelayer.guards.base import BaseGuard
from safelayer.manager import GuardManager

class SecretGuard(BaseGuard):
    def check(self, text):
        findings = []
        if "supersecret" in text:
            findings.append({
                "entity": "secret",
                "start": text.index("supersecret"),
                "end": text.index("supersecret") + len("supersecret"),
                "explanation": "Found secret keyword"
            })
        return findings

    def mask(self, text):
        return text.replace("supersecret", "[REDACTED]")

# Add your custom guard to the chain!
guards = [SecretGuard()]
manager = GuardManager(guards)

response = "This contains supersecret information."
sanitized = manager.run(response)
print("Guarded:", sanitized)
