import subprocess
import os
import argparse

from api_profiler.cache import cache
from api_profiler.cache.cache_keys import CACHE_KEYS
from api_profiler.discover_app import DiscoverApp


def run_django_with_profiler(port=8000):
    target_path = os.getcwd()
    app_name = DiscoverApp().get_app_name()
    target_settings = os.environ.get("DJANGO_SETTINGS_MODULE", f"{app_name}.settings")

    env = os.environ.copy()
    env["ORIGINAL_DJANGO_SETTINGS_MODULE"] = target_settings
    env["DJANGO_SETTINGS_MODULE"] = "api_profiler.patch_settings"

    subprocess.run(
        ["python", "manage.py", "runserver", str(port)], cwd=target_path, env=env
    )


def set_cli_environment(commands):
    for command in commands:
        print(f"Setting environment variable: API_PROFILER_{command.upper()}")
        cache.set(
            CACHE_KEYS[command.upper()],
            "True",
            None,
        )

def unset_cli_environment(commands):
    for command in commands:
        print(f"Unsetting environment variable: API_PROFILER_{command.upper()}")
        cache.set(
            CACHE_KEYS[command.upper()],
            "False",
            0,
        )


def main():
    toggels = [
        "sql",
        "headers",
        "params",
        "body",
        "response",
        "time",
        "status",
    ]
    parser = argparse.ArgumentParser(prog="Django api profiler")
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument(
        "--set",
        choices=toggels,
        nargs="+",
        help="Set the profiler options. Available options: sql, headers, params, body, response, time, status",
    )
    parser.add_argument(
        "--unset",
        choices=toggels,
        nargs="+",
        help="Unset the profiler options. Available options: sql, headers, params, body, response, time, status",
    )
    parser.add_argument(
        "--limit-sql-queries",
        type=int,
        default=10,
        help="Limit the number of SQL queries to show in the profiler output",
    )
    parser.add_argument("--run",action="store_true", help="Run the Django server with the profiler")
    args = parser.parse_args()
    if args.set:
        set_cli_environment(args.set)
    if args.unset:
        unset_cli_environment(args.unset)
    if args.run:
        run_django_with_profiler(args.port)  


if __name__ == "__main__":
    main()
