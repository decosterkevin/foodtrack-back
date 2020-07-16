from django.shortcuts import render
from django.conf import settings

def serve_frontend_view(request):
    # return render(request, settings.INDEX_FILE, {'CDN_ENDPOINT': settings.CDN_ENDPOINT})
    return render(request, settings.INDEX_FILE)