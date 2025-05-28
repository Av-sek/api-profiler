import logging
import subprocess
import os
import argparse
import sys
from typing import Optional

from api_profiler.cache import cache, features, FLAGS
from api_profiler.cache.cache_keys import LIMIT_SQL_QUERIES
from api_profiler.django_utils.discover_app import DiscoverApp
from api_profiler.logging.logger import logger


class App:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="profile",
            description="API Profiler CLI for Django projects.\n"
                        "Easily enable/disable profiling features for SQL, headers, params, body, and responses.\n"
                        "Example usage:\n"
                        "  profile --set sql headers --unset body\n"
                        "  profile --limit-sql-queries 5",
            formatter_class=argparse.RawTextHelpFormatter
        )

    def run_django_with_profiler(self, unknown: list[str] = ()) -> bool:
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
            logger.error(f"Error: {stderr}")
            return False
        return True

    def set_cli_environment(self, commands: list[str]) -> None:
        print(commands)
        for command in commands:
            if command == "all":
                commands = FLAGS.keys()
                self.set_cli_environment(commands)
                return
            logger.info(
                f"Setting {command.upper()}"
            )
            cache.set(
                FLAGS[command.upper()],
                "True",
                None,
            )

    def unset_cli_environment(self, commands: list[str]) -> None:
        for command in commands:
            if command == "all":
                commands = FLAGS.keys()
                self.unset_cli_environment(commands)
                return
            logger.info(
                f"Unsetting {command.upper()}"
            )
            cache.set(
                FLAGS[command.upper()],
                "False",
                0,
            )
    
    def positive_int(self, value: str) -> int:
        """
        Custom type for argparse to ensure the value is a positive integer.
        :param value: The string value to convert.
        :return: The positive integer value.
        """
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
        return ivalue

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
            type=self.positive_int,
            nargs="?",
            help="Limit the number of SQL queries to show in the profiler output",
        )
        self.parser.add_argument(
            "run",
            default=None,
            help="Run the Django server with the profiler",
            nargs="?",
        )

    def set_sql_queries_limit(self, limit: Optional[int]) -> None:
        """
        Set the limit for SQL queries to be displayed in the profiler.
        :param limit: The maximum number of SQL queries to display.
        """
        existing_limit = cache.get_int(LIMIT_SQL_QUERIES, 10)
        if limit is None and existing_limit is not None:
            limit = existing_limit
        elif limit == existing_limit:
            logging.warning(
                f"SQL queries limit is already set to {existing_limit}. No changes made."
            )
        else: 
            logger.info(f"Setting SQL queries limit to {limit}")
            cache.set(LIMIT_SQL_QUERIES, limit, None)
    
    def handle_argument(self, args, django_args) -> None:
        """
        Handle the command line arguments and set/unset the profiler options.
        """
        if args.set:
            self.set_cli_environment(args.set)
        if args.unset:
            self.unset_cli_environment(args.unset)
        self.set_sql_queries_limit(args.limit_sql_queries)
        if args.run:
            if not self.run_django_with_profiler(django_args):
                logger.error("Failed to run Django with profiler.")
                self.parser.print_usage()
                sys.exit(1)

    def main(self) -> None:
        """Entry point for the profiler CLI."""
        self.add_arguemnts()
        args, django_args = self.parser.parse_known_args()
        if not any([args.set, args.unset, args.run, args.limit_sql_queries]):
            self.parser.print_usage()
            sys.exit(1)
        self.handle_argument(args, django_args)


def entry_point() -> None:
    """
    Entry point for the script.
    """
    app = App()
    app.main()
