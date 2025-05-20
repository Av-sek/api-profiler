
from pathlib import Path


class DiscoverApp:
    app_name = None
    
    @classmethod
    def find_app_name(cls):
        for entry in Path(".").iterdir():
            if entry.is_dir() and (entry / "wsgi.py").exists():
                cls.app_name =entry.name
                return
        raise RuntimeError("Could not locate project folder with wsgi.py, please run this script from the project root directory.")
    
    @classmethod
    def get_app_name(cls):
        if cls.app_name is None:
            cls.find_app_name()
        return cls.app_name