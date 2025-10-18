import customtkinter as ctk
from tkinter import messagebox
from github_downloader import download_repo, download_file

APP_NAME = "Projects Downloader"
APP_VERSION = "0.1"
APP_AUTHOR = "coltonsr77"
APP_GITHUB = "https://github.com/coltonsr77/projects-downloader-P3WS"

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
        "This tool allows users to easily download GitHub projects or single files.\n"
        "Compatible with all public repositories."
    )
    messagebox.showinfo("About", about_text)

# Initialize the app window
app = ctk.CTk()
app.title(f"{APP_NAME} v{APP_VERSION}")
app.geometry("500x420")

# Title
ctk.CTkLabel(app, text=APP_NAME, font=("Arial", 24, "bold")).pack(pady=10)

# Mode selection
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
