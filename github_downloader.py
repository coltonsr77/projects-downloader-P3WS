import requests
import os
import sys

def download_repo(owner, repo, branch="main", output_dir="."):
    """Download a full GitHub repository as a ZIP file."""
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    print(f"Downloading repository: {url}")
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        output_path = os.path.join(output_dir, f"{repo}-{branch}.zip")
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Repository downloaded to: {output_path}")
    else:
        print(f"❌ Failed to download repository: {response.status_code} - {response.reason}")

def download_file(file_url, output_dir="."):
    """Download a single file from a raw GitHub URL."""
    if "raw.githubusercontent.com" not in file_url:
        print("❌ Use the 'Raw' link from GitHub for individual files.")
        return

    filename = file_url.split("/")[-1]
    output_path = os.path.join(output_dir, filename)

    print(f"Downloading file: {file_url}")
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ File downloaded to: {output_path}")
    else:
        print(f"❌ Failed to download file: {response.status_code} - {response.reason}")

if __name__ == "__main__":
    print("=== GitHub Downloader ===")
    print("1. Download a repository")
    print("2. Download a single file")
    choice = input("Choose option (1/2): ")

    if choice == "1":
        owner = input("Enter repo owner (e.g. torvalds): ")
        repo = input("Enter repo name (e.g. linux): ")
        branch = input("Branch (default: main): ") or "main"
        download_repo(owner, repo, branch)
    elif choice == "2":
        file_url = input("Enter GitHub raw file URL: ")
        download_file(file_url)
    else:
        print("Invalid choice.")
