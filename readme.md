This software is created with ClaudeAI. It started as a quick way to restart a chat when working with project with many files, and have turn into a bit of an experiment. Many of the added features are ClaudeAIs idea of what could be helpful for an LLM. It also wrote most of this readme after this paragraph. It might be overselling it a little.

![00005-81533553](https://github.com/JonTheisNilsson/LLMBridge/assets/14968184/afeb0948-e615-493e-806b-f67ecc03fb47)
# LLMBridge

LLMBridge is a comprehensive, language-agnostic code analysis tool designed to prepare project codebases for analysis by Large Language Models (LLMs). It provides deep insights into your project structure, code complexity, and potential areas for improvement.

## Features

- **Language Agnostic**: Analyzes projects in multiple programming languages.
- **Comprehensive Analysis**: Provides insights on language distribution, file sizes, code complexity, and more.
- **TODO/FIXME Tracking**: Identifies and collates all TODO and FIXME comments across your project.
- **Code Duplication Detection**: Highlights potential areas of code duplication.
- **Complexity Analysis**: For Python files, calculates complexity metrics for functions and classes.
- **User-Friendly GUI**: Easy-to-use graphical interface for selecting projects and configuring analysis.
- **Command-Line Interface**: Supports running analysis from the command line for automation and integration into other tools.
- **Gitignore Support**: Respects .gitignore files in your project, excluding ignored files and directories from analysis.
- **Dot Folder Exclusion**: Automatically skips folders that start with a dot (hidden folders).

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/YourUsername/llmbridge.git
   cd llmbridge
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (GUI)

To run the application with the graphical user interface:

```
python main.py
```

Use the GUI to select your project folder or enter a GitHub URL, specify an output file, and click "Analyze Project" to start the analysis.

### Command-Line Interface (CLI)

To run the application from the command line:

```
python main.py --cli --project_path /path/to/your/project --output_file /path/to/output.txt
```

Replace `/path/to/your/project` with the path to the project you want to analyze, and `/path/to/output.txt` with the desired location for the output file.

## Project Structure

```
llmbridge/
│
├── main.py                 # Entry point, handles both GUI and CLI modes
├── gui/
│   ├── __init__.py
│   └── application.py      # GUI-related code (Application class)
├── analysis/
│   ├── __init__.py
│   ├── code_analyzer.py    # Main analysis logic
│   ├── language_detection.py   # Language detection functions
│   ├── complexity.py           # Code complexity analysis
│   ├── duplication.py          # Code duplication detection
│   └── todo_scanner.py         # TODO/FIXME comment scanner
├── utils/
│   ├── __init__.py
│   ├── file_operations.py  # File-related utility functions
│   └── github_utils.py     # GitHub-related utility functions
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## How It Works

LLMBridge walks through your project directory, analyzing each file it encounters. It uses various techniques to extract meaningful information:

- **Language Detection**: Uses Pygments to identify the programming language of each file.
- **Code Parsing**: For supported languages (currently Python), it parses the code to extract structural information.
- **Text Analysis**: Searches for specific patterns like TODO/FIXME comments.
- **Metrics Calculation**: Computes various metrics like file sizes and code complexity.
- **Gitignore Handling**: Respects your project's .gitignore file, skipping ignored files and directories.
- **Hidden Folder Exclusion**: Automatically skips folders starting with a dot.

The collected information is then formatted into a comprehensive report, designed to provide context and insights for LLMs to perform further analysis.

## Contributing

Contributions to LLMBridge are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was developed as a collaborative effort with AI assistance.
- Special thanks to the open-source communities behind Pygments, chardet, and GitPython.

---

*Note: Remember to update this README with your specific project details, such as the correct GitHub repository URL.*