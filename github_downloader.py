import requests
import os

# === Helper: ensure downloads directory exists ===
def ensure_downloads_dir():
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir


# === Repository Downloader ===
def download_repo(owner, repo, branch="main"):
    """Download a full GitHub repository as a ZIP file."""
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    download_dir = ensure_downloads_dir()
    output_path = os.path.join(download_dir, f"{repo}-{branch}.zip")

    print(f"📦 Downloading repository: {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total = int(response.headers.get('content-length', 0))
        with open(output_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total) * 100 if total else 0
                    print(f"\rProgress: {percent:.2f}%", end="")
        print(f"\n✅ Repository saved to: {output_path}")
    else:
        print(f"❌ Failed to download repository: {response.status_code} - {response.reason}")


# === File Downloader ===
def download_file(file_url):
    """Download a single file from a raw GitHub URL."""
    if "raw.githubusercontent.com" not in file_url:
        print("❌ Use the 'Raw' link from GitHub for individual files.")
        return

    download_dir = ensure_downloads_dir()
    filename = file_url.split("/")[-1]
    output_path = os.path.join(download_dir, filename)

    print(f"📄 Downloading file: {file_url}")
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        total = int(response.headers.get('content-length', 0))
        with open(output_path, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total) * 100 if total else 0
                    print(f"\rProgress: {percent:.2f}%", end="")
        print(f"\n✅ File saved to: {output_path}")
    else:
        print(f"❌ Failed to download file: {response.status_code} - {response.reason}")


# === CLI Mode (optional use) ===
if __name__ == "__main__":
    print("=== GitHub Downloader CLI ===")
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
