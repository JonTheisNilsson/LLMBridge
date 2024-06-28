import hashlib
from typing import List, Tuple
from collections import defaultdict

class DuplicationDetector:
    CHUNK_SIZE = 6
    
    @staticmethod
    def detect_code_duplication(files_content: List[Tuple[str, str, str, int]]) -> List[Tuple[str, str, int, int, str]]:
        print("start of duplicate detection")
        
        chunk_hashes = defaultdict(list)
        duplicates = []

        try:
            for file_path, content, _, _ in files_content:  # Ignore language and file_size
                lines = content.splitlines()
                for i in range(len(lines) - DuplicationDetector.CHUNK_SIZE + 1):
                    chunk = '\n'.join(lines[i:i+DuplicationDetector.CHUNK_SIZE])
                    chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
                    
                    for other_file, other_line in chunk_hashes[chunk_hash]:
                        if other_file != file_path:
                            duplicates.append((file_path, other_file, i+1, other_line+1, chunk))
                            break
                    
                    chunk_hashes[chunk_hash].append((file_path, i))

        except Exception as e:
            print(f"Error in duplicate detection: {str(e)}")
            # You might want to log this error or handle it in a way that's appropriate for your application
        
        print(f"end of duplicate detection. Found {len(duplicates)} potential duplicates.")
        return duplicates