import os
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def main():
    print("=" * 60)
    print("Running Project: 01_Full_Enterprise_Pipeline_Duplicate")
    print("Category:        06_Enterprise_System")
    print("=" * 60)

if __name__ == "__main__":
    main()
