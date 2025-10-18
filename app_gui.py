import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import requests
from github_downloader import download_repo, download_file

# === APP INFO ===
APP_NAME = "Projects Downloader"
APP_VERSION = "0.3"
APP_AUTHOR = "coltonsr77"
APP_GITHUB = "https://github.com/coltonsr77/projects-downloader-P3WS"
APP_RELEASES_API = "https://api.github.com/repos/coltonsr77/projects-downloader-P3WS/releases/latest"


# === FUNCTIONS ===
def check_for_updates():
    """Check GitHub for new releases."""
    try:
        response = requests.get(APP_RELEASES_API, timeout=5)
        if response.status_code == 200:
            latest = response.json().get("tag_name", "").replace("v", "")
            if latest and latest != APP_VERSION:
                if messagebox.askyesno(
                    "Update Available",
                    f"A new version ({latest}) is available!\n\n"
                    f"Would you like to open the download page?"
                ):
                    webbrowser.open(APP_GITHUB + "/releases/latest")
    except requests.exceptions.RequestException:
        pass  # Skip silently if offline


def start_download():
    """Start repo or file download based on selected mode."""
    mode = mode_var.get()
    if mode == "Repository":
        owner = owner_entry.get().strip()
        repo = repo_entry.get().strip()
        branch = branch_entry.get().strip() or "main"

        if not owner or not repo:
            messagebox.showerror("Error", "Please enter both Owner and Repository name.")
            return

        download_repo(owner, repo, branch)
        messagebox.showinfo("Download Started", f"Repository '{repo}' download started.")
    else:
        file_url = file_entry.get().strip()
        if not file_url:
            messagebox.showerror("Error", "Please enter a valid Raw file URL.")
            return

        download_file(file_url)
        messagebox.showinfo("Download Started", "File download started.")


def show_about():
    about_text = (
        f"{APP_NAME} v{APP_VERSION}\n\n"
        f"Created by {APP_AUTHOR}\n"
        f"GitHub: {APP_GITHUB}\n\n"
        "A desktop tool for downloading GitHub repositories or single files.\n"
        "Compatible with all public projects."
    )
    messagebox.showinfo("About", about_text)


def open_update_page():
    """Open the GitHub releases page."""
    webbrowser.open(APP_GITHUB + "/releases/latest")


def update_mode_visibility(*_):
    """Hide or show input fields based on selected mode."""
    if mode_var.get() == "Repository":
        owner_entry.pack(pady=5)
        repo_entry.pack(pady=5)
        branch_entry.pack(pady=5)
        file_entry.pack_forget()
    else:
        file_entry.pack(pady=5)
        owner_entry.pack_forget()
        repo_entry.pack_forget()
        branch_entry.pack_forget()


# === UI SETUP ===
app = ctk.CTk()
app.title(f"{APP_NAME} v{APP_VERSION}")
app.geometry("500x450")

# Auto-check for updates after startup
app.after(1200, check_for_updates)

# Header
ctk.CTkLabel(app, text=APP_NAME, font=("Arial", 24, "bold")).pack(pady=10)

# Mode selection
mode_var = ctk.StringVar(value="Repository")
mode_menu = ctk.CTkOptionMenu(app, variable=mode_var, values=["Repository", "File"], command=update_mode_visibility)
mode_menu.pack(pady=5)

# Input fields
owner_entry = ctk.CTkEntry(app, placeholder_text="Owner (e.g. torvalds)")
repo_entry = ctk.CTkEntry(app, placeholder_text="Repository (e.g. linux)")
branch_entry = ctk.CTkEntry(app, placeholder_text="Branch (default: main)")
file_entry = ctk.CTkEntry(app, placeholder_text="Raw file URL")

# Default mode setup (Repo mode)
update_mode_visibility()

# Buttons
ctk.CTkButton(app, text="Download", command=start_download).pack(pady=20)
ctk.CTkButton(app, text="About", command=show_about).pack(pady=5)
ctk.CTkButton(app, text="Update Now", command=open_update_page).pack(pady=5)

# Footer
ctk.CTkLabel(app, text=f"Version {APP_VERSION} | {APP_AUTHOR}", font=("Arial", 10)).pack(pady=10)

app.mainloop()

