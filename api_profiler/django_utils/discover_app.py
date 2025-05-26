from pathlib import Path

from api_profiler.logging.log_sql import LogColors


class AppDiscoveryError(Exception):
    """Custom exception for app discovery errors."""

    pass


class DiscoverApp:
    app_name = None

    @classmethod
    def find_app_name(cls):
        for entry in Path(".").iterdir():
            if entry.is_dir() and (entry / "wsgi.py").exists():
                cls.app_name = entry.name
                return
        # Use logger here instead of print if available
        raise AppDiscoveryError("No Django app found in the current directory.")

    @classmethod
    def get_app_name(cls):
        if cls.app_name is None:
            cls.find_app_name()
        return cls.app_name
