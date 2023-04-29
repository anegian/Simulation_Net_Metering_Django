
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse
from .forms import *
from .models import *

# Create your views here
# App level

def regulations(request):     # simulation/templates/regulations.html
    try:
        result = 'simulation/regulations.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")


def dashboard(request):      # simulation/templates/dashboard.html
    try:
        result = 'simulation/dashboard.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

def calculator(request):    # simulation/templates/calculator.html

    if request.method == 'POST':
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form1 = PlaceOfInstallationForm(request.POST)
        form2 = EnergyConsumptionForm(request.POST)
        slider_value = request.POST.get('myRangeSlider')
        radio_value = request.POST.get('radio_option')
        storage_kW = request.POST.get('storage_kw')

        if form1.is_valid() and form2.is_valid():
            print(f"District value: {form1.cleaned_data}")
            print(f"kW of PV value: {slider_value}")
            print(f"Did User select Battery storage: {radio_value}")
            print(f"kWh value: {form2.cleaned_data}")
            if storage_kW:
                print(f"Battery kWh value: {storage_kW}")
            else:
                print('No storage selected')

        return redirect(reverse('simulation:calculator'))  # redirect to function calculator

    else:
        form1 = PlaceOfInstallationForm()
        form2 = EnergyConsumptionForm()
    return render(request, 'simulation/calculator.html', context={'form1': form1, 'form2': form2})

def info(request):           # simulation/templates/info.html
    try:
        result = 'simulation/info.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

# FUNCTION FOR THE CALCULATOR FORM SUBMIT
def submit_form(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)
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
        form = CustomerForm()
        return render(request, 'simulation/calculator.html', {'form': form})


# Getting results after submitting the form
def calculatorResults(request):
    if request.method == 'POST':
        district = request.POST.get('district')
        phase = request.POST.get('phase')
        profile = request.POST.get('profile')
        usage = request.POST.get('usage')
        battery = request.POST.get('battery')
        inclination = request.POST.get('inclination')
        system = PVSystem.objects.get(district=district, phase=phase)

        total_cost = calculate_total_cost(system, profile, usage, battery, inclination)
        payoff = calculate_payoff(total_cost, usage)
        production = calculate_production(system, inclination)
        total_profit = calculate_total_profit(production)
        npv = calculate_npv(total_profit, total_cost)
        roi = calculate_roi(payoff, total_cost)
        lcoe = calculate_lcoe(total_cost, production, usage)

        return render(request, 'dashboard.html', {'total_cost': total_cost, 'payoff': payoff, 'production': production, 'total_profit': total_profit, 'npv': npv, 'roi': roi, 'lcoe': lcoe})
    else:
        return render(request, 'calculator.html')
    pass;

# Calculations with the results
def calculate_total_cost(system, profile, usage, battery, inclination):
    # Calculate the total cost of the PV system
    # based on the user's inputs
    # Return the result

    def calculate_payoff(total_cost, usage):
    # Calculate the payoff period in years
    # based on the total cost and the user's annual usage
    # Return the result
        pass;

    def calculate_production(system, inclination):
        # Calculate the annual production of the PV system
        # based on the system's specifications and the inclination
        # Return the result
        pass;

    def calculate_total_profit(production):
        # Calculate the total profit over 25 years
        # based on the annual production
        # Return the result
        pass;

    def calculate_npv(total_profit, total_cost):
        # Calculate the net present value
        # based on the total profit and the total cost
        # Return the result
        pass;

    def calculate_roi(payoff, total_cost):
        # Calculate the return on investment
        # based on the payoff period and the total cost
        # Return the result
        pass;

    def calculate_lcoe(total_cost, production, usage):
        # Calculate the levelized cost of electricity
        # based on the total cost, the annual production, and the user's annual usage
        # Return the result
        pass;

def signup(request):
    try:
        result = 'simulation/signup.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")
    
def signupJsonResponse(request):
    if request.method == 'POST':
        # Get form data from request.POST
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        # Check if passwords match
        if password != repeat_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'})

        # Check if user with same email already exists
        if MyUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'User with this email already exists'})

        # Create user account
        user = MyUser.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        # Return success response
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
