"""Point d'entrée exécutable : python -m espace5_can ou python scan_espace5.py."""

import sys
from espace5_can.cli import main

if __name__ == "__main__":
    sys.exit(main())
