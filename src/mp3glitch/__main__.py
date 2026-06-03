import os
import sys


def main():
    from mp3glitch.cli import app

    return app()


if __name__ == "__main__":
    # receives exit code from main() (here, 0/1)
    sys.exit(main())

if not __package__:
    # Make CLI runnable from source tree with python src/package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)
