from safelayer.guards import TTSGuard
from safelayer.manager import GuardManager

def unsafe_for_tts():
    return "Hello world! <script>alert('hack');</script> Ένα δοκιμαστικό!"

guards = [TTSGuard(explain=True)]
manager = GuardManager(guards)

sanitized = manager.run(unsafe_for_tts())
print("Safe for TTS:", sanitized)
