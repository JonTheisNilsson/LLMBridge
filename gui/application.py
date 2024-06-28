import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_operations import FileUtils
from utils.github_utils import GitHubUtils
from config import Config

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("LLMBridge: Comprehensive Code Analyzer")
        self.master.geometry("600x350")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.folder_label = tk.Label(self, text="Project Folder or GitHub URL:")
        self.folder_label.pack(pady=(20,0))

        self.folder_entry = tk.Entry(self, width=60)
        self.folder_entry.pack()

        self.browse_folder_button = tk.Button(self, text="Browse Local Folder", command=self.browse_folder)
        self.browse_folder_button.pack(pady=(5,0))

        self.output_label = tk.Label(self, text="Output File:")
        self.output_label.pack(pady=(20,0))

        self.output_entry = tk.Entry(self, width=60)
        self.output_entry.pack()

        self.browse_output_button = tk.Button(self, text="Browse", command=self.browse_output)
        self.browse_output_button.pack(pady=(5,0))

        self.analyze_button = tk.Button(self, text="Analyze Project", command=self.analyze_project)
        self.analyze_button.pack(pady=(20,0))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_path = FileUtils.normalize_path(folder_path)
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)
            self.update_output_path(folder_path)

    def browse_output(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            output_file = FileUtils.normalize_path(output_file)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

    def update_output_path(self, project_path):
        if not self.output_entry.get():
            project_name = FileUtils.get_project_name(project_path)
            default_output = FileUtils.get_default_output_path(project_path, project_name)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, default_output)

    def analyze_project(self):
        project_path = self.folder_entry.get()
        output_file = self.output_entry.get()

        if not project_path:
            messagebox.showerror("Error", "Please select a project folder or enter a GitHub URL.")
            return

        if not output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return

        try:
            if GitHubUtils.is_github_url(project_path):
                project_path = GitHubUtils.clone_repository(project_path)
                self.update_output_path(project_path)
                output_file = self.output_entry.get()

            from analysis.code_analyzer import analyze_project
            file_count = analyze_project(project_path, output_file)
            messagebox.showinfo("Success", f"Analysis complete. {file_count} code files processed.\nOutput written to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")