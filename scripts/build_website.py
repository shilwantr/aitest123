#!/usr/bin/env python3
"""
Wrapper to execute master page and sitemap generation.
"""
import subprocess
import sys
from pathlib import Path

script_path = Path(__file__).parent / "generate_all_pages.py"
result = subprocess.run([sys.executable, str(script_path)])
sys.exit(result.returncode)
