import customtkinter as ctk
from tkinter import messagebox
from github_downloader import download_repo, download_file
import requests

APP_NAME = "Projects Downloader"
APP_VERSION = "0.3"
APP_AUTHOR = "coltonsr77"
APP_GITHUB = "https://github.com/coltonsr77/projects-downloader-P3WS"
APP_RELEASES_API = "https://api.github.com/repos/coltonsr77/projects-downloader-P3WS/releases/latest"

def check_for_updates():
    """Check the latest release on GitHub and compare with current version."""
    try:
        response = requests.get(APP_RELEASES_API, timeout=5)
        if response.status_code == 200:
            latest = response.json().get("tag_name", "").replace("v", "")
            if latest and latest != APP_VERSION:
                messagebox.showinfo(
                    "Update Available",
                    f"A new version ({latest}) is available!\n\n"
                    f"Visit the GitHub page to download it:\n{APP_GITHUB}"
                )
    except requests.exceptions.RequestException:
        # Ignore connection errors — just skip silently
        pass

def start_download():
    mode = mode_var.get()
    if mode == "Repository":
        if not owner_entry.get() or not repo_entry.get():
            messagebox.showerror("Error", "Please enter both Owner and Repository name.")
            return
        download_repo(owner_entry.get(), repo_entry.get(), branch_entry.get() or "main")
        messagebox.showinfo("Success", "Repository download started.")
    else:
        if not file_entry.get():
            messagebox.showerror("Error", "Please enter a valid Raw file URL.")
            return
        download_file(file_entry.get())
        messagebox.showinfo("Success", "File download started.")

def show_about():
    about_text = (
        f"{APP_NAME} v{APP_VERSION}\n\n"
        f"Created by {APP_AUTHOR}\n"
        f"GitHub: {APP_GITHUB}\n\n"
        "A tool to easily download GitHub repositories or single files.\n"
        "Compatible with all public projects."
    )
    messagebox.showinfo("About", about_text)

# --- GUI SETUP ---
app = ctk.CTk()
app.title(f"{APP_NAME} v{APP_VERSION}")
app.geometry("500x420")

# Check for updates on startup
app.after(1000, check_for_updates)

ctk.CTkLabel(app, text=APP_NAME, font=("Arial", 24, "bold")).pack(pady=10)

# Mode selector
mode_var = ctk.StringVar(value="Repository")
ctk.CTkOptionMenu(app, variable=mode_var, values=["Repository", "File"]).pack(pady=5)

# Input fields
owner_entry = ctk.CTkEntry(app, placeholder_text="Owner (e.g. torvalds)")
repo_entry = ctk.CTkEntry(app, placeholder_text="Repository (e.g. linux)")
branch_entry = ctk.CTkEntry(app, placeholder_text="Branch (default: main)")
file_entry = ctk.CTkEntry(app, placeholder_text="Raw file URL")

owner_entry.pack(pady=5)
repo_entry.pack(pady=5)
branch_entry.pack(pady=5)
file_entry.pack(pady=5)

# Buttons
ctk.CTkButton(app, text="Download", command=start_download).pack(pady=20)
ctk.CTkButton(app, text="About", command=show_about).pack(pady=5)

# Footer
ctk.CTkLabel(app, text=f"Version {APP_VERSION} | {APP_AUTHOR}", font=("Arial", 10)).pack(pady=10)

app.mainloop()
