This software is created with ClaudeAI. It started as a quick way to restart a chat when working with project with many files, and have turn into a bit of an experiment. Many of the added features are ClaudeAIs idea of what could be helpful for an LLM. It also wrote most of this readme after this paragraph. It might be overplaying it a little.

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

1. Run the program:
   ```
   python main.py
   ```

2. Use the GUI to select your project folder and specify an output file.

3. Click "Analyze Project" to start the analysis.

4. Once complete, the program will generate a detailed report in the specified output file.

## Project Structure

```
llmbridge/
│
├── main.py                 # Entry point, runs the GUI
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
│   └── file_operations.py  # File-related utility functions
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

The collected information is then formatted into a comprehensive report, designed to provide context and insights for LLMs to perform further analysis.

## Contributing

Contributions to LLMBridge are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was developed as a collaborative effort with AI assistance.
- Special thanks to the open-source communities behind Pygments and chardet.

---

*Note: Remember to update this README with your specific project details, such as the correct GitHub repository URL.*