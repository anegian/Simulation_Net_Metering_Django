
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from .forms import CustomerForm, MyForm

# Create your views here
# App level

def calculator(request):     # simulation/templates/calculator.html

    if request.method == 'POST':
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form = CustomerForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse('simulation:calculator'))  # redirect to function calculator

    else:
        form = CustomerForm()
    return render(request, 'simulation/calculator.html', context={'form': form})


def dashboard(request):      # simulation/templates/dashboard.html
    try:
        result = 'simulation/dashboard.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

def regulations(request):    # simulation/templates/regulations.html

    if request.method == 'POST':
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form = MyForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse('simulation:regulations'))  # redirect to function calculator

    else:
        form = MyForm()
    return render(request, 'simulation/regulations.html', context={'form': form})


def info(request):           # simulation/templates/info.html
    try:
        result = 'simulation/info.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

# FUNCTION FOR THE CALCULATOR FORM SUBMIT
def submit_form(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # perform any necessary actions with the form data
            return HttpResponse('Form submitted successfully')
        else:
            # handle form errors
            return HttpResponse('There was an error in the form')
    else:
        form = MyForm()
        return render(request, 'simulation/regulations.html', {'form': form})
