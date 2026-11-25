import os
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def main():
    print("=" * 60)
    print("Running Project: 04_Multi_Agent_Supervisor_and_Swarm_Duplicate")
    print("Category:        04_Agents")
    print("=" * 60)

if __name__ == "__main__":
    main()
