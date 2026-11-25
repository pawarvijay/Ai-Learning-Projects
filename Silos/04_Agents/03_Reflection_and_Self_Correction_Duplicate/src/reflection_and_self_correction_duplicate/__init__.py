import os
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def main():
    print("=" * 60)
    print("Running Project: 03_Reflection_and_Self_Correction_Duplicate")
    print("Category:        04_Agents")
    print("=" * 60)

if __name__ == "__main__":
    main()
