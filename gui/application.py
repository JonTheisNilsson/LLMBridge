"""
GUI Application for LLMBridge

This module defines the graphical user interface for the LLMBridge application.
It provides a window for users to input project locations (local or GitHub),
select output locations, and initiate the code analysis process.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_operations import FileUtils
from utils.github_utils import GitHubUtils
from config import Config

class Application(tk.Frame):
    """
    Main application window for LLMBridge.

    This class creates and manages the GUI elements for project input,
    output selection, and analysis initiation.
    """

    def __init__(self, master=None):
        """
        Initialize the Application instance.

        Args:
            master: The parent widget (usually the root window)
        """
        super().__init__(master)
        self.master = master
        self.master.title("LLMBridge: Comprehensive Code Analyzer")
        self.master.geometry("600x350")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all GUI elements in the application window."""
        self.create_project_input_widgets()
        self.create_output_selection_widgets()
        self.create_analysis_button()

    def create_project_input_widgets(self):
        """Create widgets for project input (local folder or GitHub URL)."""
        self.project_input_label = tk.Label(self, text="Project Folder or GitHub URL:")
        self.project_input_label.pack(pady=(20,0))

        self.project_input_entry = tk.Entry(self, width=60)
        self.project_input_entry.pack()

        self.browse_local_button = tk.Button(self, text="Browse Local Folder", command=self.browse_local_folder)
        self.browse_local_button.pack(pady=(5,0))

    def create_output_selection_widgets(self):
        """Create widgets for selecting the output file location."""
        self.output_label = tk.Label(self, text="Output File:")
        self.output_label.pack(pady=(20,0))

        self.output_entry = tk.Entry(self, width=60)
        self.output_entry.pack()

        self.browse_output_button = tk.Button(self, text="Browse", command=self.browse_output_location)
        self.browse_output_button.pack(pady=(5,0))

    def create_analysis_button(self):
        """Create the button to initiate the analysis process."""
        self.analyze_button = tk.Button(self, text="Analyze Project", command=self.analyze_project)
        self.analyze_button.pack(pady=(20,0))

    def browse_local_folder(self):
        """
        Open a file dialog for selecting a local project folder.

        Updates the project input entry with the selected folder path and
        sets a default output file location.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            normalized_path = FileUtils.normalize_path(folder_path)
            self.project_input_entry.delete(0, tk.END)
            self.project_input_entry.insert(0, normalized_path)
            self.update_default_output_path(normalized_path)

    def browse_output_location(self):
        """
        Open a file dialog for selecting the output file location.

        Updates the output entry with the selected file path.
        """
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            normalized_path = FileUtils.normalize_path(output_file)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, normalized_path)

    def update_default_output_path(self, project_path):
        """
        Update the output entry with a default output file path.

        Args:
            project_path (str): The path of the selected project folder.
        """
        if not self.output_entry.get():
            project_name = FileUtils.get_project_name(project_path)
            default_output = FileUtils.get_default_output_path(project_path, project_name)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, default_output)

    def analyze_project(self):
        """
        Initiate the project analysis process.

        This method validates input, handles GitHub repositories if necessary,
        and runs the analysis. It displays success or error messages to the user.
        """
        project_path = self.project_input_entry.get()
        output_file = self.output_entry.get()

        if not project_path:
            messagebox.showerror("Error", "Please select a project folder or enter a GitHub URL.")
            return

        if not output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return

        try:
            # Check if the input is a GitHub URL and clone the repository if necessary
            if GitHubUtils.is_github_url(project_path):
                project_path = GitHubUtils.clone_repository(project_path)
                self.update_default_output_path(project_path)
                output_file = self.output_entry.get()

            # Import analysis module here to avoid circular imports
            from analysis.code_analyzer import analyze_project
            file_count = analyze_project(project_path, output_file)
            
            messagebox.showinfo("Success", 
                                f"Analysis complete. {file_count} code files processed.\n"
                                f"Output written to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")