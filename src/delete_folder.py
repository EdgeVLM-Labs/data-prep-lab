"""
Hugging Face folder deletion utility.

Deletes an entire folder (and its contents)
from a Hugging Face dataset repository.

Reads Hugging Face token from a .env file.
"""

import os

from dotenv import load_dotenv
from huggingface_hub import HfApi, list_repo_files

REPO_ID = "EdgeVLM-Labs/QVED-Test-Dataset"  # Your dataset repo
FOLDER = "knee_circles"  # Folder to delete
REPO_TYPE = "dataset"  # "dataset" or "model"
DRY_RUN = False  # Set False to actually delete


def main():
    """Delete a folder from Hugging Face dataset repository."""
    load_dotenv()
    token = os.getenv("HF_TOKEN")

    if not token:
        print("❌ HF_TOKEN not found in .env file. Please add it like:")
        print("HF_TOKEN=your_huggingface_token_here")
        return

    api = HfApi(token=token)
    print(f"🔍 Scanning files in repo: {REPO_ID}/{FOLDER}")
    all_files = list_repo_files(REPO_ID, repo_type=REPO_TYPE)
    to_delete = [f for f in all_files if f.startswith(FOLDER + "/")]

    if not to_delete:
        print(f"⚠️ No files found under folder '{FOLDER}' in {REPO_ID}.")
        return

    print(f"🧾 Found {len(to_delete)} files under '{FOLDER}':")
    for f in to_delete:
        print("  -", f)

    if DRY_RUN:
        print("\n💡 DRY_RUN enabled. Set DRY_RUN=False to actually delete.")
        return

    # Perform deletion
    for f in to_delete:
        try:
            api.delete_file(path_in_repo=f, repo_id=REPO_ID, repo_type=REPO_TYPE)
            print(f"🗑️ Deleted: {f}")
        except Exception as e:
            print(f"⚠️ Error deleting {f}: {e}")

    print(f"\n✅ Folder '{FOLDER}' and its contents deleted from {REPO_ID}.")


if __name__ == "__main__":
    main()
