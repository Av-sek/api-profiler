import time

from api_profiler.cache import cache
from api_profiler.cache.cache_keys import FLAGS
from api_profiler.logging.logger import logger, silence_django_server_logs
from api_profiler.logging.log_sql import SqlLogging
# to persist the context variable across the request-response cycle

class Profiler:
    def __init__(self, get_response):
        self.get_response = get_response
        silence_django_server_logs()
        self.logger = logger

    def __process_request(self, request):
        # Store the request in context variable for later use
        self.logger.info(f"METHOD: {request.method}\t PATH: {request.get_full_path()}")
    
    def show_sql_queries(self, request, response=None):
        msg = SqlLogging.log_sql_queries(request, 10)
        if msg:
            self.logger.info(msg)
    
    def show_headers(self, request, response=None):
        headers = request.headers
        header_list = [f"{key}: {value}" for key, value in headers.items()]
        self.logger.info(f"Headers: {'\n'.join(header_list)}")
    
    def show_params(self, request, response=None):
        params = request.GET
        param_list = [f"{key}: {value}" for key, value in params.items()]
        self.logger.info(f"Params: {'\n'.join(param_list)}")
    
    def show_body(self, request, response=None):
        body = request.body.decode('utf-8')
        self.logger.info(f"Body: {body}")
    
    def show_response(self, request, response=None):
        if response:
            self.logger.info(f"Response: {response.content.decode('utf-8')}")
    
    def get_cache_key_to_function(self):
        """
        Get the cache key to function mapping.
        :return: A dictionary mapping cache keys to their corresponding functions
        """
        return {
            FLAGS["PARAMS"]: self.show_params,
            FLAGS["HEADERS"]: self.show_headers,
            FLAGS["BODY"]: self.show_body,
            FLAGS["SQL"]: self.show_sql_queries,
            FLAGS["RESPONSE"]: self.show_response,
            # Add other cache keys and their corresponding functions here
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
            self.logger.error(f"Error logging SQL queries: {e}")
        self.logger.info(f"Status: {response.status_code} Total time taken: {time.perf_counter() - start_time:.3f} seconds\n")


        return response
