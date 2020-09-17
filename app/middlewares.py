from werkzeug.wrappers import Request, Response, ResponseStream

class CounterMiddleware():
    '''
    WSGI middleware to keep track of the number of requests processed by the Flask app
    '''
    def __init__(self, app):
        self.app = app
        self._request_count = 0

    def __call__(self, environ, start_response):
        self._request_count += 1
        # print(f"Request count {self._request_count}")
        return self.app(environ, start_response)

    def get_count(self):
        return self._request_count

    def reset_count(self):
        self._request_count = 0