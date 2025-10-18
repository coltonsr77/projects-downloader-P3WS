import customtkinter as ctk
from github_downloader import download_repo, download_file

def start_download():
    mode = mode_var.get()
    if mode == "Repository":
        download_repo(owner_entry.get(), repo_entry.get(), branch_entry.get() or "main")
    else:
        download_file(file_entry.get())

app = ctk.CTk()
app.title("GitHub Downloader")
app.geometry("500x400")

ctk.CTkLabel(app, text="GitHub Downloader", font=("Arial", 24, "bold")).pack(pady=10)

mode_var = ctk.StringVar(value="Repository")
ctk.CTkOptionMenu(app, variable=mode_var, values=["Repository", "File"]).pack(pady=5)

owner_entry = ctk.CTkEntry(app, placeholder_text="Owner (e.g. torvalds)")
repo_entry = ctk.CTkEntry(app, placeholder_text="Repository (e.g. linux)")
branch_entry = ctk.CTkEntry(app, placeholder_text="Branch (default: main)")
file_entry = ctk.CTkEntry(app, placeholder_text="Raw file URL")

owner_entry.pack(pady=5)
repo_entry.pack(pady=5)
branch_entry.pack(pady=5)
file_entry.pack(pady=5)

ctk.CTkButton(app, text="Download", command=start_download).pack(pady=20)

app.mainloop()
