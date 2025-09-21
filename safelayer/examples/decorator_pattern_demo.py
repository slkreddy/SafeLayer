from safelayer.guards import PIIGuard, ToneGuard
from safelayer.manager import GuardManager
from safelayer.decorators import apply_guards

guards = [PIIGuard(), ToneGuard()]
manager = GuardManager(guards)

@apply_guards(manager)
def get_agent_reply():
    return "Write to jill@xyz.com. Damn!"

print(get_agent_reply())
