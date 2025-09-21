from safelayer.guards import PIIGuard, ToneGuard, TTSGuard
from safelayer.manager import GuardManager

def ai_tool_response():
    return "Hey, my email is ai@example.com. Crap! <script>dangerous()</script>"

guards = [PIIGuard(), ToneGuard(), TTSGuard()]
manager = GuardManager(guards)

cleaned = manager.run(ai_tool_response())
print("Sanitized Response:", cleaned)
