from importlib import import_module
import os


original_settings = os.environ.get("ORIGINAL_DJANGO_SETTINGS_MODULE")


print(original_settings)

"""
while importing original module setting django settings module to original module so that 
django settings is loaded properly as expected
"""
os.environ["DJANGO_SETTINGS_MODULE"]=original_settings
settings = import_module(original_settings)

globals().update({k: getattr(settings, k) for k in dir(settings) if k.isupper()})


#Inject middleware 
middleware_path = "api_profiler.middleware.Profiler"
if middleware_path not in MIDDLEWARE: # type: ignore
    MIDDLEWARE.append(middleware_path) # type: ignore

from api_profiler.django_utils.discover_app import DiscoverApp 
project_name = DiscoverApp.get_app_name()
if not project_name:
    raise RuntimeError("Run this script from the project root directory.")
WSGI_APPLICATION = f"{project_name}.wsgi.application"
