from logging import Logger
import time
from typing import Any

from api_profiler.cache import cache
from api_profiler.cache.cache_keys import FLAGS, LIMIT_SQL_QUERIES
from api_profiler.logging.logger import logger, silence_django_server_logs
from api_profiler.logging.log_sql import LogColors, SqlLogging

class Profiler:
    def __init__(self, get_response):
        self.get_response = get_response
        silence_django_server_logs()
        self.logger: Logger = logger

    def __process_request(self, request)-> None:
        # Store the request in context variable for later use
        self.logger.info(f"METHOD: {request.method}\t PATH: {request.get_full_path()}")
    
    def log_dict(self, map: dict[str, Any])-> str:
        """
        Log a dict with its keys values pair in a line
        :param map: 
        """
        if not map:
            return
        message = "\n\t".join(
            f"{LogColors.BOLD}{LogColors.CYAN}{key}{LogColors.RESET}: {value}" for key, value in map.items()
        )
        return message

    def show_sql_queries(self, request, response=None) -> None:
        msg: str = SqlLogging.log_sql_queries(request, cache.get_int(LIMIT_SQL_QUERIES, 10))
        if msg:
            self.logger.info(msg)

    def show_headers(self, request, response=None) -> None:
        headers = request.headers
        msg = self.log_dict(headers)
        self.logger.info(f"{LogColors.BOLD}{LogColors.YELLOW}Headers:{LogColors.RESET}\n\t{msg}")

    def show_params(self, request, response=None) -> None:
        params = request.GET
        msg = self.log_dict(params)
        self.logger.info(f"{LogColors.BOLD}{LogColors.CYAN}Params:{LogColors.RESET}\n\t{msg}")

    def show_body(self, request, response=None) -> None:
        body = request.body.decode("utf-8")
        self.logger.info(f"{LogColors.BOLD}{LogColors.MAGENTA}Body:{LogColors.RESET} {body}\n{LogColors.YELLOW} Size: {len(body)} bytes{LogColors.RESET}")

    def show_response_body(self, request, response=None) -> None:
        if response:
            content = response.content.decode('utf-8')
            self.logger.info(f"{LogColors.BOLD}{LogColors.GREEN}Response:{LogColors.RESET} {content}\n{LogColors.YELLOW} Size: {len(response.content)} bytes{LogColors.RESET}")

    def show_response_stat(self, request, response=None) -> None:
        if response:
            bytes_len = len(response.content)
            kb = bytes_len / 1024
            mb = kb / 1024
            self.logger.info(
                f"{LogColors.BOLD}{LogColors.YELLOW}Response Size:{LogColors.RESET} {bytes_len} bytes ({kb:.2f} KB, {mb:.2f} MB) \n\t"
                f"{LogColors.BOLD}{LogColors.CYAN}Response Status:{LogColors.RESET} {response.status_code}"
            )

    def show_response_headers(self, request, response)-> None: 
        if response:
            headers = response.headers
            msg = self.log_dict(headers)
            self.logger.info(f"Response Headers:\n\t{msg}")
    
    def get_cache_key_to_function(self)-> dict[str, callable]:
        """
        Get the cache key to function mapping.
        :return: A dictionary mapping cache keys to their corresponding functions
        """
        return {
            FLAGS["PARAMS"]: self.show_params,
            FLAGS["HEADERS"]: self.show_headers,
            FLAGS["BODY"]: self.show_body,
            FLAGS["SQL"]: self.show_sql_queries,
            FLAGS["RESPONSE"]: self.show_response_stat,
            FLAGS["RESPONSE-BODY"]: self.show_response_body,
            FLAGS['RESPONSE-HEADERS']: self.show_response_headers
        }

    def __call__(self, request):
        # Process the request
        start_time = time.perf_counter()
        self.__process_request(request)
        response = self.get_response(request)
        try:
            for key, func in self.get_cache_key_to_function().items():
                if cache.get_boolean(key):
                    func(request, response)
        except Exception as e:
            self.logger.error(f"Error logging SQL queries: {e}", exc_info=True)
        self.logger.info(
            f"Status: {response.status_code} Total time taken: {time.perf_counter() - start_time:.3f} seconds\n"
        )

        return response
