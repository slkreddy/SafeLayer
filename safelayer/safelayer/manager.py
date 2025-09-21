from .audit import audit_log

class GuardManager:
    def __init__(self, guards):
        self.guards = guards

    def run(self, text):
        for guard in self.guards:
            findings = guard.check(text)
            for finding in findings:
                audit_log(guard=guard.__class__.__name__, **finding)
                guard.explain_action(finding)
                text = guard.mask(text)
        return text
