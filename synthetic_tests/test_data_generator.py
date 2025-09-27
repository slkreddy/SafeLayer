"""
Synthetic test data generator for SafeLayer.
Generates text samples containing PII, toxic tone, and clean content for testing.
"""
from __future__ import annotations
import random
from typing import List, Dict

PII_EMAILS = [
    "alice@example.com", "bob.smith@gmail.com", "carol_jones@acme.co",
]
PII_PHONES = [
    "+1-202-555-0100", "(415) 555-2671", "+44 20 7946 0958",
]
TOXIC_WORDS = ["damn", "crap", "stupid", "idiot"]
CLEAN_SENTENCES = [
    "Hello there, how can I help you today?",
    "The weather is nice and sunny.",
    "Let's schedule a meeting for next week.",
]

def random_email() -> str:
    return random.choice(PII_EMAILS)


def random_phone() -> str:
    return random.choice(PII_PHONES)


def random_toxic_word() -> str:
    return random.choice(TOXIC_WORDS)


def make_sample(include_email=True, include_phone=True, include_toxic=True) -> str:
    parts: List[str] = []
    if include_email:
        parts.append(f"Email me at {random_email()}")
    if include_phone:
        parts.append(f"Call me at {random_phone()}")
    if include_toxic:
        parts.append(f"This is {random_toxic_word()}!")
    if not parts:
        parts.append(random.choice(CLEAN_SENTENCES))
    return " ".join(parts)


def generate_dataset(n: int = 50) -> List[Dict[str, str]]:
    """Generate a mixed dataset of synthetic samples.

    Returns list of dicts: {"text": str, "label": str}
    Labels: pii, tone, mixed, clean
    """
    data: List[Dict[str, str]] = []

    for _ in range(n):
        mode = random.random()
        if mode < 0.25:
            text = make_sample(include_email=True, include_phone=False, include_toxic=False)
            label = "pii"
        elif mode < 0.5:
            text = make_sample(include_email=False, include_phone=True, include_toxic=False)
            label = "pii"
        elif mode < 0.75:
            text = make_sample(include_email=False, include_phone=False, include_toxic=True)
            label = "tone"
        else:
            # 50/50 chance of fully clean vs mixed
            if random.random() < 0.5:
                text = make_sample(include_email=False, include_phone=False, include_toxic=False)
                label = "clean"
            else:
                text = make_sample(include_email=True, include_phone=True, include_toxic=True)
                label = "mixed"
        data.append({"text": text, "label": label})
    return data


def main():
    import json
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic test dataset for SafeLayer")
    parser.add_argument("-n", "--num", type=int, default=50, help="number of samples")
    parser.add_argument("-o", "--out", type=str, default="synthetic_tests/dataset.jsonl", help="output JSONL path")
    args = parser.parse_args()

    ds = generate_dataset(args.num)
    # Ensure dir exists
    import os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        for row in ds:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(ds)} samples to {args.out}")


if __name__ == "__main__":
    main()
