from datetime import datetime
import os
import pathlib

class FileUtils:
    @staticmethod
    def normalize_path(path: str) -> str:
        return str(pathlib.Path(path).resolve())

    @staticmethod
    def get_file_size(file_path: str) -> int:
        try:
            return os.path.getsize(FileUtils.normalize_path(file_path))
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
            return 0

    @staticmethod
    def read_file_content(file_path: str) -> str:
        try:
            with open(FileUtils.normalize_path(file_path), 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
            return f"[File not found: {file_path}]"
        except UnicodeDecodeError:
            return "[Binary content]"

    @staticmethod
    def get_project_name(folder_path: str) -> str:
        return os.path.basename(FileUtils.normalize_path(folder_path))

    @staticmethod
    def get_default_output_path(folder_path: str, project_name: str) -> str:
        return FileUtils.normalize_path(os.path.join(folder_path, f"{project_name}_analysis.txt"))

    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        return os.path.relpath(FileUtils.normalize_path(file_path), FileUtils.normalize_path(base_path))
    
    @staticmethod
    def get_current_datetime() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')