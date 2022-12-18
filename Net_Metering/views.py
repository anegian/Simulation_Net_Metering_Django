from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# project level
def simple_view(request):
    return render(request, 'index2.html')
