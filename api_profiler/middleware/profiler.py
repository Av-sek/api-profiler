import time

from api_profiler.utils.logger import logger, silence_django_server_logs
from api_profiler.utils.log_sql import SqlLogging
# to persist the context variable across the request-response cycle

class Profiler:
    def __init__(self, get_response):
        self.get_response = get_response
        silence_django_server_logs()
        self.logger = logger

    def __process_request(self, request):
        # Store the request in context variable for later use
        self.logger.info(f"METHOD: {request.method}\t PATH: {request.get_full_path()}")
    
    def __process_response(self, response):
        pass

    def __call__(self, request):
        # Process the request
        start_time = time.perf_counter()
        self.__process_request(request)
        response = self.get_response(request)
        
        try:
            if True:
                msg = SqlLogging.log_sql_queries(request)
                if msg:
                    self.logger.info(msg)
        except Exception as e:
            self.logger.error(f"Error logging SQL queries: {e}")
        self.logger.info(f"Total time taken: {time.perf_counter() - start_time:.3f} seconds\n")


        return response
