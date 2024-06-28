import ast
from typing import List, Tuple

class ComplexityAnalyzer:
    @staticmethod
    def analyze_python_complexity(file_path: str) -> List[Tuple[str, int]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            tree = ast.parse(content)
            function_complexities = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    complexity = ComplexityAnalyzer._calculate_complexity(node)
                    function_complexities.append((node.name, complexity))
            return function_complexities
        except Exception:
            return []

    @staticmethod
    def _calculate_complexity(node: ast.AST) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.Assert)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity