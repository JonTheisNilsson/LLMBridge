from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
import chardet

class LanguageDetector:
    @staticmethod
    def guess_language(file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                raw_content = file.read()
            encoding = chardet.detect(raw_content)['encoding']
            content = raw_content.decode(encoding)
            lexer = guess_lexer_for_filename(file_path, content)
            return lexer.name
        except ClassNotFound:
            return "Unknown"
        except Exception:
            return "Binary"