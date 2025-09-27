# SafeLayer (SL) — Agentic Python Guardrails
SafeLayer (SL) is a modular, agentic Python library providing composable guardrails for LLM and agent-based AI systems. Use SafeLayer to enforce PII controls, tone filtering, TTS safety, or custom guard logic—at function boundaries, tool-call wrappers, agent frameworks, or service integration points.

---
## What’s New (Advanced Features)
- Policy-driven configuration (policy.py): YAML/JSON policies, inheritance/merge, validation, env-based loading
- Real-time API (streaming.py): optional FastAPI HTTP / WebSocket endpoints for synchronous and streaming processing
- Upcoming in this release cycle: crypto-verifiable audit backends, contextual guards, explainability APIs, multilingual adapters, synthetic test utilities, enhanced guard chaining, CI hardening, and data residency stubs

See docs/ for detailed guides. Minimal changes below keep existing behavior intact while enabling opt-in advanced features.

---
## Features
- ✅ Composable Guards: PII, Tone, TTS and easy custom extension
- ✅ Pluggable Decorators: Add as @decorator or via GuardManager in flows
- ✅ Policy-driven: Centralized guard actions, thresholds, and severity by policy
- ✅ Optional Real-time API: Run as an HTTP/WebSocket service for streaming moderation/masking
- ✅ Audit-Friendly: Built-in logging & explainability (for compliance)
- ✅ Testable: All guards and logic can be unit tested and inspected
- ✅ Enterprise Readiness: Professional code, no banners or intrusive logos

---
## Quickstart
Install:
```
pip install -e .  # if packaged, or clone and use directly
```

Use guards via manager:
```python
from safelayer.safelayer.manager import GuardManager
from safelayer.safelayer.guards.pii import PIIGuard
from safelayer.safelayer.guards.tone import ToneGuard

text = "Email me at alice@example.com"
manager = GuardManager([PIIGuard(), ToneGuard()])
result = manager.run(text)
print(result)
```

Load a policy (YAML/JSON):
```python
from safelayer.safelayer.policy import get_policy_manager, load_policy_from_env
pm = get_policy_manager()
# pm.load_policy("./policies/prod.yaml"); pm.set_active_policy("prod")
load_policy_from_env()  # if SAFELAYER_POLICY=/path/to/policy.yaml is set
```

Run optional API (requires FastAPI/uvicorn):
```python
# pip install fastapi uvicorn
from safelayer.safelayer.streaming import StreamingServer
from safelayer.safelayer.guards.pii import PIIGuard
server = StreamingServer([PIIGuard()])
server.run(host="0.0.0.0", port=8080)
```

---
## Roadmap (this repo)
- Crypto-verifiable audit: JSONL hash-chain, HMAC/Ed25519 optional, file/SQLite sinks
- Contextual guards: conversation/tool context, role-aware logic, policy-based routing
- Explainability APIs: structured per-guard explanations and traces
- Multilingual adapters: stubs for language detection, locale-specific PII/tone heuristics
- Synthetic test utilities: PII/tone generators and streaming harness
- Guard chaining: short-circuit, parallel, weighted thresholds by policy
- CI/CD: lint, type-check, unit tests; packaging workflow
- Data residency: region-aware storage adapters and local storage controls

---
## Contributing
- PRs welcome. Keep zero or minimal hard dependencies; use optional extras for integrations.
- Add/extend unit tests for all new logic.

## License
Apache-2.0
