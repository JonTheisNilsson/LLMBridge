import os
import fnmatch
from typing import Dict, Any, List, Tuple
from .language_detection import LanguageDetector
from .complexity import ComplexityAnalyzer
from .duplication import DuplicationDetector
from .todo_scanner import TodoScanner
from utils.file_operations import FileUtils
from config import Config

class CodeAnalyzer:
    def __init__(self, folder_path: str):
        self.folder_path = FileUtils.normalize_path(folder_path)
        self.is_temp_directory = self.folder_path.startswith(FileUtils.normalize_path(os.path.join(os.getcwd(), 'temp')))
        self.gitignore_patterns = self._load_gitignore()

    def _load_gitignore(self) -> List[str]:
        gitignore_path = os.path.join(self.folder_path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return []

    def _should_ignore(self, path: str) -> bool:
        relative_path = os.path.relpath(path, self.folder_path)
        
        # Ignore folders starting with a dot
        if any(part.startswith('.') for part in relative_path.split(os.sep)):
            return True
        
        # Check against gitignore patterns
        for pattern in self.gitignore_patterns:
            if fnmatch.fnmatch(relative_path, pattern):
                return True
        
        return False
    
    def analyze(self, output_file: str) -> int:
        try:
            analysis_results = self._collect_data()
            self._write_report(FileUtils.normalize_path(output_file), analysis_results)
            return analysis_results['file_count']
        finally:
            if self.is_temp_directory:
                import shutil
                shutil.rmtree(self.folder_path, ignore_errors=True)

    def _collect_data(self) -> Dict[str, Any]:
        file_count = 0
        language_distribution = {}
        large_files: List[Tuple[str, int]] = []
        all_todos: List[Tuple[str, int, str]] = []
        all_complexities: List[Tuple[str, str, int]] = []
        files_content: List[Tuple[str, str, str, int]] = []

        for root, dirs, files in os.walk(self.folder_path):
            # Remove directories that should be ignored
            dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]

            for filename in files:
                file_path = FileUtils.join_paths(root, filename)
                if self._should_ignore(file_path):
                    continue
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
                      all_complexities: List[Tuple[str, str, int]], files_content: List[Tuple[str, str, str, int]]) -> bool:
        if not FileUtils.file_exists(file_path):
            print(f"Warning: File not found: {file_path}")
            return False

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
            files_content.append((relative_path, content, language, file_size))  # Added language and file_size

            if language == "Python":
                complexities = ComplexityAnalyzer.analyze_python_complexity(file_path)
                all_complexities.extend([(relative_path, *c) for c in complexities])

            return True
        return False

    def _write_report(self, output_file: str, results: Dict[str, Any]):
        with open(output_file, 'w', encoding='utf-8') as outfile:
            self._write_report_header(outfile)
            self._write_file_analysis(outfile, results['files_content'])
            self._write_summary(outfile, results)
            self._write_conclusion(outfile,results)

    def _write_report_header(self, outfile):
        outfile.write(f"Project Name: {os.path.basename(os.path.normpath(self.folder_path))}\n")
        outfile.write(f"Date of Analysis: {FileUtils.get_current_datetime()}\n\n")
        outfile.write("Analysis Report:\n\n")

    def _write_file_analysis(self, outfile, files_content: List[Tuple[str, str, str, int]]):
        for file_path, content, language, file_size in files_content:
            outfile.write(f"Filename: {file_path}\n")
            outfile.write(f"Language: {language}\n")
            outfile.write(f"File Size: {file_size} bytes\n")
            outfile.write("Content:\n")
            outfile.write(content)
            outfile.write("\n\n")

    def _write_summary(self, outfile, results: Dict[str, Any]):
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
        if large_files:
            outfile.write("Large Files (>100KB):\n")
            for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True):
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)}: {size/1024:.2f} KB\n")
            outfile.write("\n")

    def _write_todos_summary(self, outfile, todos: List[Tuple[str, int, str]]):
        if todos:
            outfile.write("All TODO/FIXME Comments:\n")
            for file_path, line_num, comment in todos:
                outfile.write(f"{os.path.relpath(file_path, self.folder_path)} (Line {line_num}): {comment}\n")
            outfile.write("\n")

    def _write_complexity_summary(self, outfile, complexities: List[Tuple[str, str, int]]):
        if complexities:
            outfile.write(f"Top {Config.TOP_COMPLEX_FUNCTIONS} Most Complex Functions:\n")
            for file_path, func, complexity in sorted(complexities, key=lambda x: x[2], reverse=True)[:Config.TOP_COMPLEX_FUNCTIONS]:
                outfile.write(f"{file_path} - {func}: Complexity {complexity}\n")
            outfile.write("\n")

    def _write_duplication_summary(self, outfile, duplicates: List[Tuple[str, str, int, int, str]]):
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
    
    def _write_conclusion(self, outfile, results: Dict[str, Any]):
        outfile.write("Conclusion and Recommendations:\n")
        
        # Language distribution analysis
        primary_language = max(results['language_distribution'], key=results['language_distribution'].get)
        language_count = len(results['language_distribution'])
        outfile.write(f"1. Language Distribution: The project primarily uses {primary_language} ")
        outfile.write(f"({results['language_distribution'][primary_language]} files) ")
        outfile.write(f"out of {results['file_count']} total files. ")
        if language_count > 1:
            outfile.write(f"The project is multilingual, using {language_count} different languages. ")
            outfile.write("Consider standardizing on fewer languages if possible to improve maintainability.\n")
        else:
            outfile.write("The project consistently uses a single language, which is good for maintainability.\n")

        # TODO/FIXME analysis
        todo_count = len(results['todos'])
        if todo_count > 0:
            outfile.write(f"2. TODO/FIXME Comments: There are {todo_count} TODO/FIXME comments in the project. ")
            outfile.write("Consider addressing these issues to improve code quality and completeness.\n")
        else:
            outfile.write("2. TODO/FIXME Comments: No TODO/FIXME comments found. Good job keeping the codebase clean!\n")

        # Complexity analysis
        if results['complexities']:
            max_complexity = max(results['complexities'], key=lambda x: x[2])
            outfile.write(f"3. Code Complexity: The most complex function is '{max_complexity[1]}' ")
            outfile.write(f"in file '{max_complexity[0]}' with a complexity of {max_complexity[2]}. ")
            outfile.write("Consider refactoring complex functions to improve readability and maintainability.\n")
        else:
            outfile.write("3. Code Complexity: No complexity issues detected in the analyzed files.\n")

        # Duplication analysis
        duplication_count = len(results['duplicates'])
        if duplication_count > 0:
            outfile.write(f"4. Code Duplication: Detected {duplication_count} instances of potential code duplication. ")
            outfile.write("Review and refactor these areas to improve code maintainability and reduce redundancy.\n")
        else:
            outfile.write("4. Code Duplication: No significant code duplication detected. Great job keeping the code DRY!\n")

        # Large files analysis
        large_file_count = len(results['large_files'])
        if large_file_count > 0:
            outfile.write(f"5. Large Files: Identified {large_file_count} large files (>100KB). ")
            outfile.write("Consider breaking down large files into smaller, more manageable modules.\n")
        else:
            outfile.write("5. Large Files: No excessively large files detected. Good job keeping file sizes manageable.\n")

        # General recommendations
        outfile.write("6. General Recommendations:\n")
        outfile.write("   - Regularly review and update dependencies to ensure security and performance.\n")
        outfile.write("   - Implement or improve unit testing to maintain code quality.\n")
        outfile.write("   - Consider using static code analysis tools for ongoing code quality checks.\n")
        outfile.write("   - Maintain up-to-date documentation for better project understanding and onboarding.\n")

def analyze_project(folder_path: str, output_file: str) -> int:
    analyzer = CodeAnalyzer(folder_path)
    return analyzer.analyze(output_file)