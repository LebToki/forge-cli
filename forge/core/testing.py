"""Automated test generation and testing tools for FORGE."""

import os
import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import tempfile

from rich.console import Console

console = Console()


class TestGenerator:
    """Generate tests for code using AI."""
    
    def __init__(self):
        from ..core.llm import DeepSeekClient
        self.client = DeepSeekClient()
    
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code to understand its structure for test generation."""
        analysis = {
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": "unknown"
        }
        
        if language == "python":
            try:
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        analysis["functions"].append({
                            "name": node.name,
                            "args": [arg.arg for arg in node.args.args],
                            "returns": node.returns.id if node.returns and isinstance(node.returns, ast.Name) else None,
                        })
                    elif isinstance(node, ast.ClassDef):
                        methods = []
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                methods.append(item.name)
                        analysis["classes"].append({
                            "name": node.name,
                            "methods": methods,
                        })
                
                # Estimate complexity
                analysis["complexity"] = "medium"
                
            except SyntaxError:
                analysis["complexity"] = "syntax_error"
        
        return analysis
    
    def generate_tests(self, 
                      code: str, 
                      language: str = "python",
                      framework: str = "pytest") -> str:
        """Generate tests using AI."""
        
        analysis = self.analyze_code(code, language)
        
        prompt = f"""Generate pytest tests for this {language} code.

Code:
```{language}
{code}
```

Functions to test: {len(analysis['functions'])}
Classes to test: {len(analysis['classes'])}

Generate comprehensive pytest tests with proper assertions."""
        
        try:
            messages = [
                {"role": "system", "content": "You are an expert at writing tests."},
                {"role": "user", "content": prompt}
            ]
            
            tests = self.client.chat(messages)
            return self._extract_code(tests, language)
        except Exception as e:
            return f"# Error generating tests: {e}"
    
    def _extract_code(self, text: str, language: str) -> str:
        """Extract code from AI response."""
        pattern = f"```{language}(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Try generic code block
        pattern = "```(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return text.strip()
    
    def save_tests(self, tests: str, original_file: Path, test_file: Optional[Path] = None) -> Path:
        """Save generated tests to file."""
        if not test_file:
            original_name = original_file.stem
            if original_name.startswith('test_'):
                test_file = original_file
            else:
                test_file = original_file.parent / f"test_{original_file.name}"
        
        test_file.write_text(tests)
        return test_file
