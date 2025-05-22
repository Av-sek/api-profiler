import subprocess
import os
import argparse
import sys
import logging

from api_profiler.cache import cache, features, FLAGS
from api_profiler.cache.cache_keys import LIMIT_SQL_QUERIES
from api_profiler.django_utils.discover_app import DiscoverApp


class App:

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="profile")
        self.parser.description = "API Profiler CLI"

    def run_django_with_profiler(self,unknown:list[str]=()) -> bool:
        """Run Django server with profiler settings. Returns True on success, False on failure."""
        target_path = os.getcwd()
        app_name = DiscoverApp.get_app_name()
        target_settings = os.environ.get(
            "DJANGO_SETTINGS_MODULE", f"{app_name}.settings"
        )

        env = os.environ.copy()
        env["ORIGINAL_DJANGO_SETTINGS_MODULE"] = target_settings
        env["DJANGO_SETTINGS_MODULE"] = "api_profiler.patch_settings"

        result = subprocess.run(
            ["python", "manage.py", "runserver", *unknown],
            cwd=target_path,
            text=True,
            stderr=subprocess.PIPE,
            env=env,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()
            logging.error(f"Error: {stderr}")
            return False
        return True

    def set_cli_environment(self, commands:list[str])-> None:
        for command in commands:
            logging.info(
                f"Setting environment variable: API_PROFILER_{command.upper()}"
            )
            cache.set(
                FLAGS[command.upper()],
                "True",
                None,
            )

    def unset_cli_environment(self, commands:list[str])-> None:
        for command in commands:
            logging.info(
                f"Unsetting environment variable: API_PROFILER_{command.upper()}"
            )
            cache.set(
                FLAGS[command.upper()],
                "False",
                0,
            )

    def add_arguemnts(self) -> None:
        """Add arguments to the parser."""
        self.parser.add_argument(
            "--set",
            choices=features,
            nargs="+",
            help="Set the profiler options. Available options: sql, headers, params, body, response, time, status",
        )
        self.parser.add_argument(
            "--unset",
            choices=features,
            nargs="+",
            help="Unset the profiler options. Available options: sql, headers, params, body, response, time, status",
        )
        self.parser.add_argument(
            "--limit-sql-queries",
            type=int,
            default=10,
            help="Limit the number of SQL queries to show in the profiler output",
        )
        self.parser.add_argument(
            "run",
            default=None,
            help="Run the Django server with the profiler",
            nargs="?",
        )

    def handle_argument(self, args, django_args)-> None:
        """
        Handle the command line arguments and set/unset the profiler options.
        """
        if args.set:
            self.set_cli_environment(args.set)
        if args.unset:
            self.unset_cli_environment(args.unset)
        if args.limit_sql_queries:
            logging.info(f"Setting limit for SQL queries to: {args.limit_sql_queries}")
            cache.set(
                LIMIT_SQL_QUERIES,
                str(args.limit_sql_queries),
                None,
            )
        if args.run:
            if not self.run_django_with_profiler(django_args):
                logging.error("Failed to run Django with profiler.")
                self.parser.print_usage()
                sys.exit(1)

    def main(self)-> None:
        """Entry point for the profiler CLI."""
        self.add_arguemnts()
        args, django_args = self.parser.parse_known_args()
        if not any([args.set, args.unset, args.run]):
            self.parser.print_usage()
            sys.exit(1)
        self.handle_argument(args, django_args)


def entry_point()-> None:
    """
    Entry point for the script.
    """
    app = App()
    app.main()