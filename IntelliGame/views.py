from django.http import HttpResponse


def home(request):
    return HttpResponse("<b>Home page...</b>")