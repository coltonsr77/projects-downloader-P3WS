import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import requests
import threading
from github_downloader import ensure_downloads_dir
import os
from packaging import version  # For version comparison

# === APP INFO ===
APP_NAME = "Projects Downloader"
APP_VERSION = "0.3"
APP_AUTHOR = "coltonsr77"
APP_GITHUB = "https://github.com/coltonsr77/projects-downloader-P3WS"
APP_RELEASES_API = "https://api.github.com/repos/coltonsr77/projects-downloader-P3WS/releases/latest"


# === Download Helpers ===
def download_repo(owner, repo, branch, progress_callback):
    url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    download_dir = ensure_downloads_dir()
    output_path = os.path.join(download_dir, f"{repo}-{branch}.zip")

    response = requests.get(url, stream=True)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to download repo: {response.status_code}")
        return

    total = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total) * 100 if total else 0
                progress_callback(percent)

    messagebox.showinfo("Download Complete", f"Repository saved to:\n{output_path}")


def download_file(file_url, owner, repo, branch, progress_callback):
    """Download a single file and update progress."""
    if not file_url:
        if not owner or not repo:
            messagebox.showerror("Error", "Owner and Repository required if no Raw URL provided.")
            return
        messagebox.showinfo("Info", "No raw URL provided. File download skipped.")
        return

    if "raw.githubusercontent.com" not in file_url:
        messagebox.showerror("Error", "Use a valid 'Raw' GitHub file URL.")
        return

    download_dir = ensure_downloads_dir()
    filename = file_url.split("/")[-1]
    output_path = os.path.join(download_dir, filename)

    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to download file: {response.status_code}")
        return

    total = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total) * 100 if total else 0
                progress_callback(percent)

    messagebox.showinfo("Download Complete", f"File saved to:\n{output_path}")


# === GUI Logic ===
def check_for_updates():
    """Check GitHub releases with reversed logic."""
    try:
        response = requests.get(APP_RELEASES_API, timeout=5)
        if response.status_code == 200:
            latest_tag = response.json().get("tag_name", "").replace("v", "")
            if latest_tag:
                current = version.parse(APP_VERSION)
                latest = version.parse(latest_tag)

                if latest < current:
                    if messagebox.askyesno(
                        "Update Available",
                        f"A new version ({latest_tag}) is available!\n\n"
                        f"Would you like to open the download page?"
                    ):
                        webbrowser.open(APP_GITHUB + "/releases/latest")
                else:
                    messagebox.showinfo(
                        "Up to Date",
                        f"You already have the latest version ({APP_VERSION})."
                    )
    except requests.exceptions.RequestException:
        pass


def start_download_thread():
    progress_bar.set(0)
    progress_label.configure(text="Preparing download...")

    def run_download():
        mode = mode_var.get()
        owner = owner_entry.get().strip()
        repo = repo_entry.get().strip()
        branch = branch_entry.get().strip() or "main"
        file_url = file_entry.get().strip()

        if mode == "Repository":
            if not owner or not repo:
                messagebox.showerror("Error", "Please enter both Owner and Repository name.")
                return
            download_repo(owner, repo, branch, update_progress)
        else:
            download_file(file_url, owner, repo, branch, update_progress)

        progress_label.configure(text="Download complete!")

    threading.Thread(target=run_download, daemon=True).start()


def update_progress(percent):
    progress_bar.set(percent / 100)
    progress_label.configure(text=f"Progress: {percent:.1f}%")


def show_about():
    about_text = (
        f"{APP_NAME} v{APP_VERSION}\n\n"
        f"Created by {APP_AUTHOR}\n"
        f"GitHub: {APP_GITHUB}\n\n"
        "A desktop tool for downloading GitHub repositories or single files.\n"
        "All downloads are saved in the 'downloads' folder."
    )
    messagebox.showinfo("About", about_text)


def update_mode_visibility(*_):
    """Arrange input fields; Raw URL under Branch with spacing in File mode."""
    if mode_var.get() == "Repository":
        owner_entry.pack(pady=5)
        repo_entry.pack(pady=5)
        branch_entry.pack(pady=5)
        file_entry.pack_forget()
    else:
        owner_entry.pack(pady=5)
        repo_entry.pack(pady=5)
        branch_entry.pack(pady=5)
        file_entry.pack(pady=10)  # Extra spacing for visual separation


# === MAIN UI ===
app = ctk.CTk()
app.title(f"{APP_NAME} v{APP_VERSION}")
app.geometry("520x550")

app.after(1200, check_for_updates)

# Title
ctk.CTkLabel(app, text=APP_NAME, font=("Arial", 24, "bold")).pack(pady=10)

# Mode selection
mode_var = ctk.StringVar(value="Repository")
ctk.CTkOptionMenu(app, variable=mode_var, values=["Repository", "File"], command=update_mode_visibility).pack(pady=5)

# Input fields
owner_entry = ctk.CTkEntry(app, placeholder_text="Owner (e.g. torvalds)")
repo_entry = ctk.CTkEntry(app, placeholder_text="Repository (e.g. linux)")
branch_entry = ctk.CTkEntry(app, placeholder_text="Branch (default: main)")
file_entry = ctk.CTkEntry(app, placeholder_text="Raw file URL")  # Now spaced below Branch

update_mode_visibility()

# Progress Bar
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)
progress_label = ctk.CTkLabel(app, text="Progress: 0%")
progress_label.pack(pady=2)

# Buttons
ctk.CTkButton(app, text="Download", command=start_download_thread).pack(pady=15)
ctk.CTkButton(app, text="About", command=show_about).pack(pady=5)

# Footer
ctk.CTkLabel(app, text=f"Version {APP_VERSION} | {APP_AUTHOR}", font=("Arial", 10)).pack(pady=10)

app.mainloop()
