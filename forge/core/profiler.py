"""Performance profiling tools for FORGE."""

import cProfile
import pstats
import io
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import functools

from rich.console import Console
from rich.table import Table

console = Console()


class Profiler:
    """Code performance profiling."""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.results = {}
    
    def start(self):
        """Start profiling."""
        self.profiler.enable()
    
    def stop(self) -> Dict[str, Any]:
        """Stop profiling and return results."""
        self.profiler.disable()
        
        stream = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)
        
        results = {
            "raw": stream.getvalue(),
            "functions": [],
            "total_time": 0,
        }
        
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            filename, lineno, func_name = func
            results["functions"].append({
                "file": filename,
                "line": lineno,
                "function": func_name,
                "calls": nc,
                "total_time": ct,
            })
            results["total_time"] += ct
        
        self.results = results
        return results
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.start()
            result = func(*args, **kwargs)
            stats = self.stop()
            self.display_stats(stats)
            return result
        return wrapper
    
    def display_stats(self, stats: Dict[str, Any] = None):
        """Display profiling statistics."""
        if stats is None:
            stats = self.results
        
        if not stats.get("functions"):
            console.print("[yellow]No profiling data available[/yellow]")
            return
        
        table = Table(title="Performance Profile", show_header=True, header_style="bold cyan")
        table.add_column("Function", style="cyan")
        table.add_column("File", style="dim")
        table.add_column("Calls", justify="right")
        table.add_column("Time (s)", justify="right")
        
        for func in sorted(stats["functions"], key=lambda x: x["total_time"], reverse=True)[:15]:
            table.add_row(
                func["function"],
                Path(func["file"]).name,
                str(func["calls"]),
                f"{func['total_time']:.3f}"
            )
        
        console.print(table)
