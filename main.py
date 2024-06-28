import argparse
import sys
from analysis.code_analyzer import analyze_project
from gui.application import Application
import tkinter as tk

def run_cli(args):
    try:
        file_count = analyze_project(args.project_path, args.output_file)
        print(f"Analysis complete. {file_count} code files processed.")
        print(f"Output written to {args.output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def run_gui():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

def main():
    parser = argparse.ArgumentParser(description="LLMBridge: Comprehensive Code Analyzer")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--project_path", help="Path to the project folder or GitHub URL")
    parser.add_argument("--output_file", help="Path to the output file")

    args = parser.parse_args()

    if args.cli:
        if not args.project_path or not args.output_file:
            parser.error("--project_path and --output_file are required in CLI mode")
        run_cli(args)
    else:
        run_gui()

if __name__ == "__main__":
    main()