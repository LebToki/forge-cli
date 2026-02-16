"""Command execution engine for FORGE."""

import subprocess
import shlex
import signal
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
import tempfile
import os
import time


class CommandExecutor:
    """Execute commands and capture output with real-time streaming."""
    
    def __init__(self, workspace: Optional[Path] = None, timeout: int = 60):
        """Initialize executor with workspace and timeout."""
        self.workspace = workspace or Path.cwd()
        self.timeout = timeout
        self.process = None
    
    def run(self, 
            command: str, 
            stream: bool = True,
            env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Run a command and return result."""
        # Merge environment
        cmd_env = os.environ.copy()
        if env:
            cmd_env.update(env)
        
        # Prepare command
        if sys.platform == "win32":
            # Windows needs different handling
            process = subprocess.Popen(
                command,
                cwd=str(self.workspace),
                env=cmd_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        else:
            # Unix-like systems
            process = subprocess.Popen(
                command,
                cwd=str(self.workspace),
                env=cmd_env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                preexec_fn=os.setsid  # Create process group for killing children
            )
        
        self.process = process
        
        stdout_lines = []
        stderr_lines = []
        
        try:
            if stream:
                # Stream output in real-time
                while True:
                    # Check if process has ended
                    if process.poll() is not None:
                        # Read any remaining output
                        stdout, stderr = process.communicate()
                        if stdout:
                            stdout_lines.extend(stdout.splitlines())
                        if stderr:
                            stderr_lines.extend(stderr.splitlines())
                        break
                    
                    # Read lines if available
                    if process.stdout:
                        line = process.stdout.readline()
                        if line:
                            line = line.rstrip()
                            stdout_lines.append(line)
                            yield {"type": "stdout", "line": line}
                    
                    if process.stderr:
                        line = process.stderr.readline()
                        if line:
                            line = line.rstrip()
                            stderr_lines.append(line)
                            yield {"type": "stderr", "line": line}
                    
                    time.sleep(0.01)
            else:
                # Just capture output
                stdout, stderr = process.communicate(timeout=self.timeout)
                stdout_lines = stdout.splitlines() if stdout else []
                stderr_lines = stderr.splitlines() if stderr else []
                
        except subprocess.TimeoutExpired:
            self.kill_process()
            raise TimeoutError(f"Command timed out after {self.timeout} seconds")
        except KeyboardInterrupt:
            self.kill_process()
            raise
        
        return {
            "command": command,
            "stdout": stdout_lines,
            "stderr": stderr_lines,
            "returncode": process.returncode,
            "success": process.returncode == 0
        }
    
    def kill_process(self):
        """Kill the running process and its children."""
        if self.process:
            if sys.platform == "win32":
                self.process.kill()
            else:
                try:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                except:
                    self.process.kill()
    
    def run_command(self, command: str, stream: bool = True) -> Dict[str, Any]:
        """Simple wrapper for running commands."""
        result = {}
        for output in self.run(command, stream=stream):
            if isinstance(output, dict):
                # This is a streaming chunk
                continue
            result = output
        return result


class CodeRunner:
    """Run code in various languages."""
    
    LANGUAGE_CONFIGS = {
        "python": {
            "extension": ".py",
            "run_cmd": "python {file}",
            "version_cmd": "python --version"
        },
        "javascript": {
            "extension": ".js",
            "run_cmd": "node {file}",
            "version_cmd": "node --version"
        },
        "typescript": {
            "extension": ".ts",
            "run_cmd": "ts-node {file}",
            "version_cmd": "ts-node --version"
        },
        "ruby": {
            "extension": ".rb",
            "run_cmd": "ruby {file}",
            "version_cmd": "ruby --version"
        },
        "go": {
            "extension": ".go",
            "run_cmd": "go run {file}",
            "version_cmd": "go version"
        },
        "rust": {
            "extension": ".rs",
            "run_cmd": "rustc {file} -o /tmp/rust_temp && /tmp/rust_temp",
            "version_cmd": "rustc --version"
        },
        "bash": {
            "extension": ".sh",
            "run_cmd": "bash {file}",
            "version_cmd": "bash --version"
        },
        "c": {
            "extension": ".c",
            "run_cmd": "gcc {file} -o /tmp/c_temp && /tmp/c_temp",
            "version_cmd": "gcc --version"
        },
        "cpp": {
            "extension": ".cpp",
            "run_cmd": "g++ {file} -o /tmp/cpp_temp && /tmp/cpp_temp",
            "version_cmd": "g++ --version"
        },
    }
    
    def __init__(self, workspace: Optional[Path] = None):
        self.workspace = workspace or Path.cwd()
        self.executor = CommandExecutor(workspace)
    
    def detect_language(self, code: str, filename: str = None, language: str = None) -> Tuple[str, dict]:
        """Detect programming language from code or filename."""
        if language and language in self.LANGUAGE_CONFIGS:
            return language, self.LANGUAGE_CONFIGS[language]
        
        if filename:
            ext = Path(filename).suffix
            for lang, config in self.LANGUAGE_CONFIGS.items():
                if config["extension"] == ext:
                    return lang, config
        
        # Try to detect from code
        code_lower = code.lower()
        if 'def ' in code and 'import ' in code:
            return "python", self.LANGUAGE_CONFIGS["python"]
        elif 'function' in code and 'console.log' in code:
            return "javascript", self.LANGUAGE_CONFIGS["javascript"]
        elif 'package main' in code and 'func main' in code:
            return "go", self.LANGUAGE_CONFIGS["go"]
        elif 'fn main' in code:
            return "rust", self.LANGUAGE_CONFIGS["rust"]
        elif '#include' in code:
            if 'cout' in code or 'cin' in code:
                return "cpp", self.LANGUAGE_CONFIGS["cpp"]
            return "c", self.LANGUAGE_CONFIGS["c"]
        
        return "python", self.LANGUAGE_CONFIGS["python"]  # Default to Python
    
    def check_dependencies(self, language: str) -> Tuple[bool, str]:
        """Check if required runtime is installed."""
        config = self.LANGUAGE_CONFIGS.get(language)
        if not config:
            return False, f"No configuration for {language}"
        
        try:
            result = self.executor.run_command(config["version_cmd"], stream=False)
            if result["success"]:
                version = result["stdout"][0] if result["stdout"] else "Unknown"
                return True, version
            else:
                return False, f"{language} not found in PATH"
        except Exception as e:
            return False, str(e)
    
    def run_code(self, 
                 code: str, 
                 language: str = None,
                 filename: str = None,
                 args: List[str] = None,
                 stream: bool = True) -> Dict[str, Any]:
        """Run code in specified language."""
        # Detect language
        lang, config = self.detect_language(code, filename, language)
        
        # Check dependencies
        has_deps, version = self.check_dependencies(lang)
        if not has_deps:
            return {
                "success": False,
                "error": f"Missing dependency: {version}",
                "language": lang,
                "stdout": [],
                "stderr": [f"Error: {lang} is not installed or not in PATH"]
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=config["extension"],
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Build command
            cmd = config["run_cmd"].format(file=temp_file)
            if args:
                cmd += " " + " ".join(shlex.quote(arg) for arg in args)
            
            # Run code
            if stream:
                for output in self.executor.run(cmd, stream=True):
                    yield output
            else:
                result = self.executor.run_command(cmd, stream=False)
                result["language"] = lang
                result["version"] = version
                return result
                
        finally:
            # Clean up temp file
            try:
                Path(temp_file).unlink()
            except:
                pass
    
    def run_file(self, 
                 filepath: str,
                 args: List[str] = None,
                 stream: bool = True) -> Dict[str, Any]:
        """Run a code file."""
        path = Path(filepath)
        if not path.exists():
            return {
                "success": False,
                "error": f"File not found: {filepath}",
                "stdout": [],
                "stderr": [f"Error: {filepath} does not exist"]
            }
        
        code = path.read_text(encoding='utf-8')
        return self.run_code(
            code=code,
            filename=filepath,
            args=args,
            stream=stream
        )
