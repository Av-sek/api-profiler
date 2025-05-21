from importlib import import_module
import os

from api_profiler.django_utils.discover_app import DiscoverApp 

original_settings = os.environ.get("ORIGINAL_DJANGO_SETTINGS_MODULE")


project_name = DiscoverApp.get_app_name()
if not project_name:
    raise RuntimeError("Run this script from the project root directory.")

settings = import_module(original_settings)

globals().update({k: getattr(settings, k) for k in dir(settings) if k.isupper()})

WSGI_APPLICATION = f"{project_name}.wsgi.application"

#Inject middleware 
middleware_path = "api_profiler.middleware.Profiler"
if middleware_path not in MIDDLEWARE: # type: ignore
    MIDDLEWARE.append(middleware_path) # type: ignore
