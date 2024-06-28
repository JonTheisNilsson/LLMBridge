import os
import pathlib
from datetime import datetime

class FileUtils:
    @staticmethod
    def normalize_path(path: str) -> str:
        return str(pathlib.Path(path).resolve())

    @staticmethod
    def get_file_size(file_path: str) -> int:
        print(f"trying to get file size of: {file_path}")
        try:
            return os.path.getsize(file_path)
        except OSError as e:
            print(f"Warning: Unable to get file size for {file_path}: {str(e)}")
            return 0

    @staticmethod
    def read_file_content(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except OSError as e:
            print(f"Warning: Unable to read file {file_path}: {str(e)}")
            return f"[Unable to read file: {file_path}]"
        except UnicodeDecodeError:
            return "[Binary content]"

    @staticmethod
    def get_project_name(folder_path: str) -> str:
        return os.path.basename(folder_path)

    @staticmethod
    def get_default_output_path(folder_path: str, project_name: str) -> str:
        return os.path.join(folder_path, f"{project_name}_analysis.txt")

    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        return os.path.relpath(file_path, base_path)
    
    @staticmethod
    def get_current_datetime() -> str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.isfile(file_path)

    @staticmethod
    def join_paths(base_path: str, *paths: str) -> str:
        return os.path.join(base_path, *paths)