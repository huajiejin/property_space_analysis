# Gloabl exception handler middleware for non-ninja endpoints, if any
from django.http import JsonResponse, Http404
from django.core import exceptions

class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # 404
        if isinstance(exception, exceptions.ObjectDoesNotExist) \
            or isinstance(exception, Http404):
            response_data = {
                "error": "Not found",
            }
            return JsonResponse(response_data, status=404)

        # 500
        response_data = {
            "error": str(exception),
        }
        return JsonResponse(response_data, status=500)