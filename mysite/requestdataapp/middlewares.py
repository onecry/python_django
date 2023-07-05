import time

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


def setup_useragent_on_request_middleware(get_response):

    print('initial call')

    def middleware(request: HttpRequest):
        print('before get response')
        if 'HTTP_USER_AGENT' in request.META:
            request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print('requests count', self.request_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time.time()
        self.time_now = 0
        self.time_diff = 0

    def __call__(self, request: HttpRequest):
        info_dict = {}
        ip = request.META.get('REMOTE_ADDR')
        info_dict[ip] = info_dict.get(ip, {})

        if 'start' not in info_dict[ip]:
            info_dict[ip]['start'] = self.start_time
            info_dict[ip]['count_requests'] = 0

        self.time_now = time.time()
        self.time_diff = self.time_now - info_dict[ip]['start']
        if self.time_diff > 5:
            self.time_now = 0
            self.start_time = time.time()
            info_dict[ip]['start'] = self.start_time
            raise PermissionDenied('Too many requests. Wait a bit')

        self.time_diff = 0

        response = self.get_response(request)
        return response
