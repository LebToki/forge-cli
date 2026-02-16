"""File system operations for FORGE."""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
import difflib


class FileSystemTool:
    """Tools for interacting with the file system."""
    
    def __init__(self, workspace: Optional[Path] = None):
        """Initialize with optional workspace restriction."""
        self.workspace = workspace or Path.cwd()
    
    def read_file(self, path: str) -> Tuple[str, str]:
        """Read a file and return its content with syntax hint."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if not full_path.is_file():
            raise IsADirectoryError(f"Path is a directory: {path}")
        
        content = full_path.read_text(encoding='utf-8')
        extension = full_path.suffix.lstrip('.')
        
        return content, extension
    
    def write_file(self, path: str, content: str, force: bool = False) -> bool:
        """Write content to a file."""
        full_path = self._resolve_path(path)
        
        # Check if file exists and we're not forcing
        if full_path.exists() and not force:
            raise FileExistsError(f"File already exists: {path} (use force=True to overwrite)")
        
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_path.write_text(content, encoding='utf-8')
        return True
    
    def list_directory(self, path: str = ".", recursive: bool = False) -> List[Path]:
        """List contents of a directory."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        if not full_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        
        if recursive:
            return list(full_path.rglob("*"))
        else:
            return list(full_path.iterdir())
    
    def get_file_info(self, path: str) -> dict:
        """Get information about a file or directory."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        stat = full_path.stat()
        info = {
            "path": str(full_path),
            "name": full_path.name,
            "type": "directory" if full_path.is_dir() else "file",
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:],
        }
        
        if full_path.is_file():
            info["extension"] = full_path.suffix.lstrip('.')
        
        return info
    
    def delete_file(self, path: str, force: bool = False) -> bool:
        """Delete a file or empty directory."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        if full_path.is_file():
            full_path.unlink()
        elif full_path.is_dir():
            if not force:
                # Check if directory is empty
                if any(full_path.iterdir()):
                    raise OSError(f"Directory not empty: {path} (use force=True to delete non-empty)")
            shutil.rmtree(full_path)
        
        return True
    
    def move_file(self, source: str, destination: str) -> bool:
        """Move or rename a file/directory."""
        src_path = self._resolve_path(source)
        dst_path = self._resolve_path(destination)
        
        if not src_path.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        
        # Create destination directory if needed
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(src_path), str(dst_path))
        return True
    
    def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file/directory."""
        src_path = self._resolve_path(source)
        dst_path = self._resolve_path(destination)
        
        if not src_path.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        
        # Create destination directory if needed
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        if src_path.is_file():
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path)
        
        return True
    
    def search_files(self, pattern: str, path: str = ".", content_search: bool = False) -> List[Path]:
        """Search for files matching pattern."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        results = []
        for file_path in full_path.rglob(pattern):
            if file_path.is_file():
                results.append(file_path)
        
        return results
    
    def diff_files(self, file1: str, file2: str) -> str:
        """Generate diff between two files."""
        path1 = self._resolve_path(file1)
        path2 = self._resolve_path(file2)
        
        if not path1.exists() or not path2.exists():
            raise FileNotFoundError("One or both files not found")
        
        content1 = path1.read_text(encoding='utf-8').splitlines()
        content2 = path2.read_text(encoding='utf-8').splitlines()
        
        diff = difflib.unified_diff(
            content1, content2,
            fromfile=str(path1),
            tofile=str(path2),
            lineterm=''
        )
        
        return '\n'.join(diff)
    
    def _resolve_path(self, path: str) -> Path:
        """Resolve a path relative to workspace."""
        # Handle absolute paths
        if Path(path).is_absolute():
            return Path(path)
        
        # Handle paths with ~ (home directory)
        if path.startswith('~'):
            return Path(path).expanduser()
        
        # Handle paths with . and ..
        return (self.workspace / path).resolve()
