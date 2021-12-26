import subprocess
import sys

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "blazegraph-python/dist/pymantic-0.1.1.dev0-py3-none-any.whl"])

if __name__ == "__main__":
  install()