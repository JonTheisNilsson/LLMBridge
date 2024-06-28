import hashlib
from typing import List, Tuple
from collections import defaultdict

class DuplicationDetector:
    @staticmethod
    def detect_code_duplication(files_content: List[Tuple[str, str]], chunk_size: int = 6) -> List[Tuple[str, str, int, int, str]]:
        chunk_hashes = defaultdict(list)
        duplicates = []

        for file_path, content in files_content:
            lines = content.splitlines()
            for i in range(len(lines) - chunk_size + 1):
                chunk = '\n'.join(lines[i:i+chunk_size])
                chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
                
                for other_file, other_line in chunk_hashes[chunk_hash]:
                    if other_file != file_path:
                        duplicates.append((file_path, other_file, i+1, other_line+1, chunk))
                        break
                
                chunk_hashes[chunk_hash].append((file_path, i))

        return duplicates