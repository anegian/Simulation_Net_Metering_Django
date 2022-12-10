
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404
from .forms import CalculatorForm

# Create your views here
# App level

def calculator(request):     # templates/simulation/calculator.html
    if request.method == 'POST':
        # changes th name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form = CalculatorForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse('simulation:calculator'))  # redirect to function calculator

    else:
        form = CalculatorForm()
    return render(request, 'simulation/calculator.html', context={'form': form})


def dashboard(request):      # templates/calculator/dashboard.html
    try:
        result = 'simulation/dashboard.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

def regulations(request):    # templates/calculator/regulations.html
    try:
        result = 'simulation/regulations.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

def info(request):           # templates/calculator/info.html
    try:
        result = 'simulation/info.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")