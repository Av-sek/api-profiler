
from pathlib import Path

from api_profiler.utils.log_sql import LogColors


class DiscoverApp:
    app_name = None
    
    @classmethod
    def find_app_name(cls):
        for entry in Path(".").iterdir():
            if entry.is_dir() and (entry / "wsgi.py").exists():
                cls.app_name =entry.name
                return
        print(f"{LogColors.MAGENTA}ERROR {LogColors.RESET}:No Django app found in the current directory.")
        exit(1)

    @classmethod
    def get_app_name(cls):
        if cls.app_name is None:
            cls.find_app_name()
        return cls.app_name