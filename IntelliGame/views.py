from django.shortcuts import render_to_response
from django.template import RequestContext



def home(request):
    return render_to_response("base.xhtml",
                              {"title" : "Welcome"},
                              context_instance = RequestContext(request));
                              
                              

def successful_v(request):
    return render_to_response('base.xhtml',
                              {"title" : "Success"},
                              context_instance = RequestContext(request));