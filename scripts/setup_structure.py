# Professional Research Project Structure Created

import os
from pathlib import Path

# Define base directories
BASE = Path(".")

# Create clean structure
folders = [
    "data/raw",
    "data/processed", 
    "scripts",
    "outputs/data",
    "outputs/figures", 
    "outputs/tables",
    "docs",
    "analysis"
]

print("Creating professional folder structure...")
for folder in folders:
    (BASE / folder).mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {folder}/")

print("\n✓ Folder structure created successfully!")
print("\nNext: Move datasets to data/raw/")
