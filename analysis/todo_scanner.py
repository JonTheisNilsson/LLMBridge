import re
from typing import List, Tuple

class TodoScanner:
    @staticmethod
    def scan_todos(file_path: str) -> List[Tuple[int, str]]:
        todos = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file, 1):
                    if re.search(r'\b(TODO|FIXME)\b', line, re.IGNORECASE):
                        todos.append((i, line.strip()))
        except UnicodeDecodeError:
            pass
        return todos