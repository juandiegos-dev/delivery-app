import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

subprocess.run(
    [sys.executable, "manage.py", "migrate"],
    cwd=BASE_DIR,
    check=True
)

print("Base de datos creada o actualizada correctamente.")