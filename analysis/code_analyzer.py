import os
import shutil
import tempfile
from typing import Dict, Any
from .language_detection import LanguageDetector
from .complexity import ComplexityAnalyzer
from .duplication import DuplicationDetector
from .todo_scanner import TodoScanner
from utils.file_operations import FileUtils
from config import Config


class CodeAnalyzer:
    def __init__(self, folder_path: str):
        self.folder_path = FileUtils.normalize_path(folder_path)
        self.is_temp = folder_path.startswith(tempfile.gettempdir())

    def analyze(self, output_file: str) -> int:
        try:
            results = self._collect_data()
            self._write_report(FileUtils.normalize_path(output_file), results)
            return results['file_count']
        finally:
            if self.is_temp:
                shutil.rmtree(self.folder_path, ignore_errors=True)

    def _collect_data(self) -> Dict[str, Any]:
        file_count = 0
        language_counter = {}
        large_files = []
        all_todos = []
        all_complexities = []
        files_content = []

        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                file_path = FileUtils.normalize_path(os.path.join(root, filename))
                try:
                    language = LanguageDetector.guess_language(file_path)
                    
                    if language not in ["Unknown", "Binary"]:
                        file_count += 1
                        language_counter[language] = language_counter.get(language, 0) + 1
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
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

        duplicates = DuplicationDetector.detect_code_duplication(files_content)

        return {
            'file_count': file_count,
            'language_counter': language_counter,
            'large_files': large_files,
            'todos': all_todos,
            'complexities': all_complexities,
            'duplicates': duplicates,
            'files_content': files_content
        }

    def _write_report(self, output_file: str, results: Dict[str, Any]):
        with open(output_file, 'w', encoding='utf-8') as outfile:
            self._write_header(outfile)
            self._write_file_analysis(outfile, results['files_content'], results['language_counter'])
            self._write_summary(outfile, results)
            self._write_conclusion(outfile)

    def _write_header(self, outfile):
        outfile.write(f"Project Name: {os.path.basename(os.path.normpath(self.folder_path))}\n")
        outfile.write(f"Date of Analysis: {FileUtils.get_current_datetime()}\n\n")
        outfile.write("Analysis Report:\n\n")

    def _write_file_analysis(self, outfile, files_content, language_counter):
        for file_path, content in files_content:
            outfile.write(f"Filename: {file_path}\n")
            outfile.write(f"Language: {LanguageDetector.guess_language(file_path)}\n")
            outfile.write(f"File Size: {FileUtils.get_file_size(file_path)} bytes\n")
            outfile.write("Content:\n")
            outfile.write(content)
            outfile.write("\n\n")

    def _write_summary(self, outfile, results):
        outfile.write(f"Total number of code files: {results['file_count']}\n\n")
        
        outfile.write("Language Statistics:\n")
        for lang, count in results['language_counter'].items():
            percentage = (count / results['file_count']) * 100
            outfile.write(f"{lang}: {count} files ({percentage:.2f}%)\n")
        outfile.write("\n")

        if results['large_files']:
            outfile.write("Large Files (>100KB):\n")
            for file_path, size in sorted(results['large_files'], key=lambda x: x[1], reverse=True):
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)}: {size/1024:.2f} KB\n")
            outfile.write("\n")

        if results['todos']:
            outfile.write("All TODO/FIXME Comments:\n")
            for file_path, line_num, comment in results['todos']:
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)} (Line {line_num}): {comment}\n")
            outfile.write("\n")

        if results['complexities']:
            outfile.write(f"Top {Config.TOP_COMPLEX_FUNCTIONS} Most Complex Functions:\n")
            for file_path, func, complexity in sorted(results['complexities'], key=lambda x: x[2], reverse=True)[:Config.TOP_COMPLEX_FUNCTIONS]:
                outfile.write(f"{file_path} - {func}: Complexity {complexity}\n")
            outfile.write("\n")

        if results['duplicates']:
            outfile.write("Potential Code Duplications:\n")
            for file1, file2, line1, line2, chunk in results['duplicates'][:10]:
                outfile.write(f"Similar code found in:\n")
                outfile.write(f"  1. {file1} (line {line1})\n")
                outfile.write(f"  2. {file2} (line {line2})\n")
                outfile.write("Duplicated code:\n")
                outfile.write(chunk + "\n\n")
            if len(results['duplicates']) > 10:
                outfile.write(f"... and {len(results['duplicates']) - 10} more duplications\n")
            outfile.write("\n")

    def _write_conclusion(self, outfile):
        outfile.write("Conclusion and Recommendations:\n")
        outfile.write("1. Review and address TODO/FIXME comments\n")
        outfile.write("2. Consider refactoring complex functions\n")
        outfile.write("3. Investigate and resolve potential code duplications\n")
        outfile.write("4. Optimize large files if possible\n")
        outfile.write("5. Ensure consistent coding style across different languages\n")


def analyze_project(folder_path: str, output_file: str) -> int:
    analyzer = CodeAnalyzer(folder_path)
    return analyzer.analyze(output_file)
