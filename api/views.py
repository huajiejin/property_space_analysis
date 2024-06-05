from django.http import HttpResponse
from django.views import View
from .models import PropertySpace
from django.core import serializers

class PropertySpaceView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('id'):
            space = serializers.serialize('json', [PropertySpace.objects.get(pk=kwargs['id'])])
        else:
            space = serializers.serialize('json', PropertySpace.objects.all())
        return HttpResponse(space, content_type='application/json')
