import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import tempfile
import shutil
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
from collections import Counter
import re

def guess_language(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        lexer = guess_lexer_for_filename(file_path, content)
        return lexer.name
    except ClassNotFound:
        return "Unknown"
    except UnicodeDecodeError:
        return "Binary"

def get_file_size(file_path):
    return os.path.getsize(file_path)

def scan_todos(file_path):
    todos = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                if re.search(r'\b(TODO|FIXME)\b', line, re.IGNORECASE):
                    todos.append((i, line.strip()))
    except UnicodeDecodeError:
        pass
    return todos

def combine_code_files_to_txt(folder_path, output_file):
    temp_output = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8')
    try:
        with temp_output as outfile:
            outfile.write(f"Project Name: {os.path.basename(os.path.normpath(folder_path))}\n")
            outfile.write(f"Date of Analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            outfile.write("You are an AI assistant specialized in analyzing and explaining code. Below you'll find the contents of multiple code files from a project, along with additional analysis information. For each file:\n")
            outfile.write("1. Identify the programming language used.\n")
            outfile.write("2. Summarize its purpose and main functionality.\n")
            outfile.write("3. Highlight any important functions, classes, or variables.\n")
            outfile.write("4. Note any potential improvements or best practices that could be applied.\n")
            outfile.write("5. Pay attention to any TODO or FIXME comments and their implications.\n")
            outfile.write("After analyzing all files, provide an overall summary of the project structure and purpose.\n\n")
            outfile.write("Here are the files and analysis information:\n\n")

            file_count = 0
            language_counter = Counter()
            large_files = []
            all_todos = []

            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if os.path.abspath(file_path) == os.path.abspath(output_file):
                        continue  # Skip the output file itself
                    
                    language = guess_language(file_path)
                    if language not in ["Unknown", "Binary"]:
                        file_count += 1
                        language_counter[language] += 1
                        file_size = get_file_size(file_path)
                        if file_size > 100000:  # Files larger than 100KB
                            large_files.append((file_path, file_size))
                        
                        todos = scan_todos(file_path)
                        if todos:
                            all_todos.extend([(file_path, *todo) for todo in todos])

                        relative_path = os.path.relpath(file_path, folder_path)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            outfile.write(f"Filename: {relative_path}\n")
                            outfile.write(f"Language: {language}\n")
                            outfile.write(f"File Size: {file_size} bytes\n")
                            if todos:
                                outfile.write("TODO/FIXME comments:\n")
                                for line_num, comment in todos:
                                    outfile.write(f"  Line {line_num}: {comment}\n")
                            outfile.write("Content:\n")
                            outfile.write(infile.read())
                            outfile.write("\n\nPlease analyze the above file and provide your insights.\n\n")

            outfile.write(f"Total number of code files: {file_count}\n\n")
            
            outfile.write("Language Statistics:\n")
            for lang, count in language_counter.most_common():
                percentage = (count / file_count) * 100
                outfile.write(f"{lang}: {count} files ({percentage:.2f}%)\n")
            outfile.write("\n")

            if large_files:
                outfile.write("Large Files (>100KB):\n")
                for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True):
                    outfile.write(f"{os.path.relpath(file_path, folder_path)}: {size/1024:.2f} KB\n")
                outfile.write("\n")

            if all_todos:
                outfile.write("All TODO/FIXME Comments:\n")
                for file_path, line_num, comment in all_todos:
                    outfile.write(f"{os.path.relpath(file_path, folder_path)} (Line {line_num}): {comment}\n")
                outfile.write("\n")

            outfile.write("Now that you've analyzed all the files, please provide an overall summary of the project. Consider:\n")
            outfile.write("1. The main purpose of the project\n")
            outfile.write("2. The programming languages used and their distribution in the project\n")
            outfile.write("3. How the different files interact with each other\n")
            outfile.write("4. Any overarching patterns or design principles used\n")
            outfile.write("5. The project structure, including the use of subdirectories\n")
            outfile.write("6. Insights from the language statistics, large files, and TODO/FIXME comments\n")
            outfile.write("7. Suggestions for overall improvement or optimization\n")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Move the temporary file to the desired output location
        shutil.move(temp_output.name, output_file)
        return file_count
    except Exception as e:
        os.unlink(temp_output.name)
        raise e

def normalize_path(path):
    return path.replace('\\', '/') if isinstance(path, str) else path

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("LLMBridge: Enhanced Code Analyzer")
        self.master.geometry("500x250")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.folder_label = tk.Label(self, text="Project Folder:")
        self.folder_label.pack(pady=(20,0))

        self.folder_entry = tk.Entry(self, width=50)
        self.folder_entry.pack()

        self.browse_folder_button = tk.Button(self, text="Browse", command=self.browse_folder)
        self.browse_folder_button.pack(pady=(5,0))

        self.output_label = tk.Label(self, text="Output File:")
        self.output_label.pack(pady=(20,0))

        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.pack()

        self.browse_output_button = tk.Button(self, text="Browse", command=self.browse_output)
        self.browse_output_button.pack(pady=(5,0))

        self.analyze_button = tk.Button(self, text="Analyze Project", command=self.analyze_project)
        self.analyze_button.pack(pady=(20,0))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_path = normalize_path(folder_path)
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)
            if not self.output_entry.get():
                project_name = os.path.basename(os.path.normpath(folder_path))
                default_output = os.path.join(folder_path, f"{project_name}_analysis.txt")
                default_output = normalize_path(default_output)
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, default_output)

    def browse_output(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if output_file:
            output_file = normalize_path(output_file)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file)

    def analyze_project(self):
        folder_path = self.folder_entry.get()
        output_file = self.output_entry.get()

        if not folder_path:
            messagebox.showerror("Error", "Please select a project folder.")
            return

        if not output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return

        try:
            file_count = combine_code_files_to_txt(folder_path, output_file)
            messagebox.showinfo("Success", f"Analysis complete. {file_count} code files processed.\nOutput written to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()