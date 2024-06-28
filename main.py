"""
LLMBridge: Comprehensive Code Analyzer

This is the entry point for the LLMBridge application. It initializes and runs
the graphical user interface for the code analysis tool.

The tool allows users to analyze both local projects and GitHub repositories,
providing insights into code structure, complexity, and potential improvements.
"""

import tkinter as tk
from gui.application import Application

def main():
    """
    Initialize and run the L
    This function creates the main Tkinter window and starts the application's
    event loop.
    """
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()