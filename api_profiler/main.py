import subprocess
import os
import argparse

from api_profiler.discover_app import DiscoverApp


def run_django_with_profiler(port=8000):
    # import pdb; pdb.set_trace()
    target_path = os.getcwd()
    app_name = DiscoverApp().get_app_name()
    target_settings = os.environ.get("DJANGO_SETTINGS_MODULE", f"{app_name}.settings")

    env = os.environ.copy()
    env["ORIGINAL_DJANGO_SETTINGS_MODULE"] = target_settings
    env["DJANGO_SETTINGS_MODULE"] = "api_profiler.patch_settings"

    subprocess.run(
        ["python", "manage.py", "runserver", str(port)], cwd=target_path, env=env
    )


def main():
    parser = argparse.ArgumentParser(prog="Django api profiler")
    parser.add_argument("-p", "--port", type=int, default=8000)
    args = parser.parse_args()
    run_django_with_profiler(args.port)


if __name__ == "__main__":
    main()
