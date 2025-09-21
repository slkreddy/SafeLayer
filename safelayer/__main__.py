import argparse
from safelayer.manager import GuardManager
from safelayer.guards import PIIGuard, ToneGuard, TTSGuard

def main():
    parser = argparse.ArgumentParser(description="SafeLayer CLI: Run GuardManager on input text or file.")
    parser.add_argument("-i", "--input", help="Input file path (text). If not set, reads stdin.", default=None)
    parser.add_argument("-c", "--config", help="Optional config file (YAML) for dynamic guard setup.", default=None)
    parser.add_argument("-o", "--output", help="Output file, default: stdout", default=None)
    args = parser.parse_args()

    # Simple default setup
    guards = [PIIGuard(), ToneGuard(), TTSGuard()]
    manager = GuardManager(guards)

    # If implemented, load guards/config from YAML here
    if args.input:
        with open(args.input) as f:
            input_text = f.read()
    else:
        input_text = input("Enter text: ")

    cleaned = manager.run(input_text)
    if args.output:
        with open(args.output, "w") as f:
            f.write(cleaned)
    else:
        print(cleaned)

if __name__ == "__main__":
    main()
