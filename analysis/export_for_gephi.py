"""Thin CLI wrapper that delegates to the importable exporter module.

This file remains as a top-level script for backwards compatibility but
keeps the implementation in `analysis.exporter` for reuse.
"""

from analysis.exporter import main


if __name__ == "__main__":
    main()
