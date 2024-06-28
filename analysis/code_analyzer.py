"""
Code Analyzer Module for LLMBridge

This module contains the core functionality for analyzing project code.
It walks through project directories, collects various metrics, and
generates a comprehensive analysis report.
"""

import os
import shutil
import tempfile
from typing import Dict, Any, List, Tuple

from .language_detection import LanguageDetector
from .complexity import ComplexityAnalyzer
from .duplication import DuplicationDetector
from .todo_scanner import TodoScanner
from utils.file_operations import FileUtils
from config import Config

class CodeAnalyzer:
    """
    Analyzes a project directory and generates a comprehensive report.

    This class walks through a project directory, analyzing each file for various
    metrics such as language usage, complexity, TODOs, and code duplication.
    """

    def __init__(self, folder_path: str):
        """
        Initialize the CodeAnalyzer with the given project folder path.

        Args:
            folder_path (str): The path to the project directory to be analyzed.
        """
        self.folder_path = FileUtils.normalize_path(folder_path)
        self.is_temp_directory = folder_path.startswith(tempfile.gettempdir())

    def analyze(self, output_file: str) -> int:
        """
        Perform the analysis and write the report to the specified output file.

        Args:
            output_file (str): The path where the analysis report will be written.

        Returns:
            int: The number of code files analyzed.

        Raises:
            Exception: If there's an error during analysis or writing the report.
        """
        try:
            analysis_results = self._collect_data()
            self._write_report(FileUtils.normalize_path(output_file), analysis_results)
            return analysis_results['file_count']
        finally:
            if self.is_temp_directory:
                shutil.rmtree(self.folder_path, ignore_errors=True)

    def _collect_data(self) -> Dict[str, Any]:
        """
        Collect analysis data by walking through the project directory.

        Returns:
            Dict[str, Any]: A dictionary containing various analysis metrics.
        """
        file_count = 0
        language_distribution = {}
        large_files: List[Tuple[str, int]] = []
        all_todos: List[Tuple[str, int, str]] = []
        all_complexities: List[Tuple[str, str, int]] = []
        files_content: List[Tuple[str, str]] = []

        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    processed = self._process_file(file_path, language_distribution,
                                                   large_files, all_todos, all_complexities, files_content)
                    if processed:
                        file_count += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

        code_duplicates = DuplicationDetector.detect_code_duplication(files_content)

        return {
            'file_count': file_count,
            'language_distribution': language_distribution,
            'large_files': large_files,
            'todos': all_todos,
            'complexities': all_complexities,
            'duplicates': code_duplicates,
            'files_content': files_content
        }

    def _process_file(self, file_path: str, language_distribution: Dict[str, int],
                      large_files: List[Tuple[str, int]], all_todos: List[Tuple[str, int, str]],
                      all_complexities: List[Tuple[str, str, int]], files_content: List[Tuple[str, str]]) -> bool:
        """
        Process a single file, collecting various metrics.

        Args:
            file_path (str): Path to the file being processed.
            language_distribution (Dict[str, int]): Distribution of programming languages.
            large_files (List[Tuple[str, int]]): List of large files found.
            all_todos (List[Tuple[str, int, str]]): List of TODO comments found.
            all_complexities (List[Tuple[str, str, int]]): List of complexity metrics for functions.
            files_content (List[Tuple[str, str]]): List of file contents for duplication analysis.

        Returns:
            bool: True if the file was successfully processed, False otherwise.
        """
        language = LanguageDetector.guess_language(file_path)
        
        if language not in ["Unknown", "Binary"]:
            language_distribution[language] = language_distribution.get(language, 0) + 1
            
            file_size = FileUtils.get_file_size(file_path)
            if file_size > Config.LARGE_FILE_THRESHOLD:
                large_files.append((file_path, file_size))
            
            todos = TodoScanner.scan_todos(file_path)
            if todos:
                all_todos.extend([(file_path, *todo) for todo in todos])

            relative_path = FileUtils.get_relative_path(file_path, self.folder_path)
            content = FileUtils.read_file_content(file_path)
            files_content.append((relative_path, content))

            if language == "Python":
                complexities = ComplexityAnalyzer.analyze_python_complexity(file_path)
                all_complexities.extend([(relative_path, *c) for c in complexities])

            return True
        return False

    def _write_report(self, output_file: str, results: Dict[str, Any]):
        """
        Write the analysis report to the specified output file.

        Args:
            output_file (str): Path to the output file.
            results (Dict[str, Any]): Analysis results to be written.
        """
        with open(output_file, 'w', encoding='utf-8') as outfile:
            self._write_report_header(outfile)
            self._write_file_analysis(outfile, results['files_content'], results['language_distribution'])
            self._write_summary(outfile, results)
            self._write_conclusion(outfile)

    def _write_report_header(self, outfile):
        """Write the header section of the report."""
        outfile.write(f"Project Name: {os.path.basename(os.path.normpath(self.folder_path))}\n")
        outfile.write(f"Date of Analysis: {FileUtils.get_current_datetime()}\n\n")
        outfile.write("Analysis Report:\n\n")

    def _write_file_analysis(self, outfile, files_content: List[Tuple[str, str]], language_distribution: Dict[str, int]):
        """Write individual file analysis to the report."""
        for file_path, content in files_content:
            outfile.write(f"Filename: {file_path}\n")
            outfile.write(f"Language: {LanguageDetector.guess_language(file_path)}\n")
            outfile.write(f"File Size: {FileUtils.get_file_size(file_path)} bytes\n")
            outfile.write("Content:\n")
            outfile.write(content)
            outfile.write("\n\n")

    def _write_summary(self, outfile, results: Dict[str, Any]):
        """Write the summary section of the report."""
        file_count = results['file_count']
        outfile.write(f"Total number of code files: {file_count}\n\n")
        
        outfile.write("Language Statistics:\n")
        if file_count > 0:
            for lang, count in results['language_distribution'].items():
                percentage = (count / file_count) * 100
                outfile.write(f"{lang}: {count} files ({percentage:.2f}%)\n")
        else:
            outfile.write("No code files were analyzed.\n")
        outfile.write("\n")

        self._write_large_files_summary(outfile, results['large_files'])
        self._write_todos_summary(outfile, results['todos'])
        self._write_complexity_summary(outfile, results['complexities'])
        self._write_duplication_summary(outfile, results['duplicates'])

    def _write_large_files_summary(self, outfile, large_files: List[Tuple[str, int]]):
        """Write summary of large files found."""
        if large_files:
            outfile.write("Large Files (>100KB):\n")
            for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True):
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)}: {size/1024:.2f} KB\n")
            outfile.write("\n")

    def _write_todos_summary(self, outfile, todos: List[Tuple[str, int, str]]):
        """Write summary of TODO comments found."""
        if todos:
            outfile.write("All TODO/FIXME Comments:\n")
            for file_path, line_num, comment in todos:
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)} (Line {line_num}): {comment}\n")
            outfile.write("\n")

    def _write_complexity_summary(self, outfile, complexities: List[Tuple[str, str, int]]):
        """Write summary of code complexity metrics."""
        if complexities:
            outfile.write(f"Top {Config.TOP_COMPLEX_FUNCTIONS} Most Complex Functions:\n")
            for file_path, func, complexity in sorted(complexities, key=lambda x: x[2], reverse=True)[:Config.TOP_COMPLEX_FUNCTIONS]:
                outfile.write(f"{file_path} - {func}: Complexity {complexity}\n")
            outfile.write("\n")

    def _write_duplication_summary(self, outfile, duplicates: List[Tuple[str, str, int, int, str]]):
        """Write summary of code duplication found."""
        if duplicates:
            outfile.write("Potential Code Duplications:\n")
            for file1, file2, line1, line2, chunk in duplicates[:10]:
                outfile.write(f"Similar code found in:\n")
                outfile.write(f"  1. {file1} (line {line1})\n")
                outfile.write(f"  2. {file2} (line {line2})\n")
                outfile.write("Duplicated code:\n")
                outfile.write(chunk + "\n\n")
            if len(duplicates) > 10:
                outfile.write(f"... and {len(duplicates) - 10} more duplications\n")
            outfile.write("\n")

    def _write_conclusion(self, outfile):
        """Write concluding remarks and recommendations."""
        outfile.write("Conclusion and Recommendations:\n")
        outfile.write("1. Review and address TODO/FIXME comments\n")
        outfile.write("2. Consider refactoring complex functions\n")
        outfile.write("3. Investigate and resolve potential code duplications\n")
        outfile.write("4. Optimize large files if possible\n")
        outfile.write("5. Ensure consistent coding style across different languages\n")

def analyze_project(folder_path: str, output_file: str) -> int:
    """
    Analyze a project and generate a report.

    This function creates a CodeAnalyzer instance and runs the analysis.

    Args:
        folder_path (str): The path to the project directory to be analyzed.
        output_file (str): The path where the analysis report will be written.

    Returns:
        int: The number of code files analyzed.

    Raises:
        Exception: If there's an error during analysis or writing the report.
    """
    analyzer = CodeAnalyzer(folder_path)
    return analyzer.analyze(output_file)