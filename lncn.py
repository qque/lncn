import argparse
import sys

def main():
    """
    The main function executed when the 'lncn' command is run.
    This function sets up the argument parser and directs execution
    based on the provided flags.
    """
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a', '--flag-a',
        action='store_true',
        help='Activates feature A (e.g., enable verbose output).'
    )

    parser.add_argument(
        '-b', '--flag-b',
        action='store_true',
        help='Activates feature B (e.g., use a special configuration).'
    )

    args = parser.parse_args()

    print("test")

if __name__ == '__main__': main()