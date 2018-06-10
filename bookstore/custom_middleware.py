import json
from bookstore.models import HttpRequest


def simple_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        if request.method == "POST":
            request_info = request.POST
        elif request.method == "GET":
            request_info = request.GET
        request_obj = HttpRequest(request_path=request.path, request_method=request.method,
                                  request_info=json.dumps(request_info), request_cookies=request.COOKIES)
        request_obj.save()
        return response

    return middleware