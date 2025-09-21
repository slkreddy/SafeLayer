

```markdown
# SafeLayer Architecture

This document describes the high-level architecture and design of the SafeLayer (SL) agentic Python guardrails library.

---

## Key Components

- **BaseGuard:**  
  Abstract base class. All guards inherit and implement:
  - `check(text)`: returns detections/issues.
  - `mask(text)`: returns a redacted/cleansed version.
  - `explain_action(details)`: (optional, for audit/explanation).

- **Built-in Guards:**
  - **PIIGuard:** Detects and masks emails/phone numbers (regex or Presidio).
  - **ToneGuard:** Detects and censors profane/offensive words.
  - **TTSGuard:** Removes patterns unsafe for text-to-speech output.
  - (Add more in `safelayer/guards/`…)

- **GuardManager:**
  - Executes a sequence of guards.
  - Applies each detection and masking, with logs.

- **Decorators:**
  - `apply_guards(manager)`: Function decorator for pre/post-LLM or agent outputs.

- **Audit Logging:**
  - Every detection or action is recorded to an audit log for compliance.

---

## Example Flow

```
> agent.py
  |
  V
GuardManager (runs sequence)
  |
  V
[Guard: PIIGuard] -> [Guard: ToneGuard] -> [Guard: TTSGuard] ...
  |
  V
Output string (processed, redacted, auditable)
```

---

## Extensibility

- Minimal dependencies; pure Python.
- Add custom guards via `guards/` and inherit `BaseGuard`.
- Plug into agents, LLMs, and server flows via decorators or manager.

---

## Design Principles

- **Composability:** Guards are independent, chainable, and order-agnostic.
- **Auditability:** Every action is logged and explainable.
- **Agentic Ready:** Integrate with any agent, LLM, or framework.
- **Minimalism:** No intrusive runtime logos or banners.
- **Professionalism:** Written for enterprise adoption.

---

For deeper details, patterns, and anti-patterns, see `developer_guide.md`.

Contributions, issues, and PRs welcome!
```
