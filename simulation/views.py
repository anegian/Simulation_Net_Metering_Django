
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse
from .forms import *
from .models import *

# Create your views here
# App level

def dashboard_results(request):   # simulation/templates/dashboard.html
 
    if 'district_key' in request.session:
        try:
            district_key = int(request.session.get('district_key'))
            district_value = request.session.get('district_value')
            place_of_installment = request.session.get('place_of_installment')
            inclination_PV = int(request.session.get('inclination_PV'))
            azimuth_value = request.session.get('azimuth_value')
            userPower_profile = request.session.get('userPower_profile')
            phase_load = request.session.get('phase_load')
            phase_loadkVA = int(request.session.get('phase_loadkVA'))
            recommended_PV_in_Kwp = request.session.get('recommended_PV_in_Kwp')
            annual_kwh = int(request.session.get('annual_kwh'))
            PV_kWp = int(request.session.get('PV_kWp'))
            average_annual_production = district_key * PV_kWp
            has_storage = request.session.get('has_storage')
            storage_kW = int(request.session.get('storage_kW'))
            battery_cost = storage_kW * 700

            
            total_investment = calculate_total_investment(PV_kWp, battery_cost)
            average_annual_savings, profitPercent, totalAnnualCost, otherEnergyCharges = calculate_annual_savings(annual_kwh, phase_loadkVA, battery_cost, userPower_profile, average_annual_production)
            payback_period = calculate_payback_period(total_investment, average_annual_savings)

            # dictionary with rendered variables
            context = {
            'district_key': district_key,
            'district_value': district_value,
            'place_of_installment': place_of_installment,
            'azimuth_value': azimuth_value,
            'inclination_PV': inclination_PV,
            'userPower_profile': userPower_profile,
            'phase_load': phase_load,
            'phase_loadkVA': phase_loadkVA,
            'recommended_PV_in_Kwp': recommended_PV_in_Kwp,
            'annual_kwh': annual_kwh,
            'PV_kWp': PV_kWp,
            'has_storage': has_storage,
            'storage_kW': storage_kW,
            'total_investment': total_investment,
            'payback_period': payback_period,
            'average_annual_savings': average_annual_savings,
            'profitPercent': profitPercent,
            'totalAnnualCost': totalAnnualCost,
            'otherEnergyCharges': otherEnergyCharges,
            }

            result = 'simulation/dashboard.html'
            print('Total Investment:', total_investment,"euro", '& Περίοδος Απόσβεσης:', payback_period, "Ετήσιο κόστος ρεύματος: ", totalAnnualCost, "& ετήσια μείωση: ", average_annual_savings, "Ρυθμιζόμενες χρεώσεις: ", otherEnergyCharges, )  # Add this line for debugging
            return render(request, result, context)
        except Http404:
            return Http404("404 Generic Error")
    else:
        try:
            result = 'simulation/dashboard.html'
            return render(request, result)
        except Http404:      # not use bare except
            return Http404("404 Generic Error")

    
def calculator_forms_choice(request):    # simulation/templates/calculator.html

    if request.method == 'POST':
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form_district = PlaceOfInstallationForm(request.POST)
        form_annual_kwh = EnergyConsumptionForm(request.POST)
        form_phase_load = PhaseLoad(request.POST)
        
        
        if form_district.is_valid() and form_annual_kwh.is_valid() and form_phase_load.is_valid():
            try:
                # initialization of variables
                district_key = request.POST.get('select_district')
                district_value = dict(PlaceOfInstallationForm.DISTRICT_CHOICES).get(district_key)
                place_of_installment = request.POST.get('installation')
                azimuth_value = request.POST.get('azimuth')
                inclination_PV = request.POST.get('inclination')
                userPower_profile = request.POST.get('power_option')

                phase_load = request.POST.get('select_phase')

                if phase_load == "single_phase":
                    phase_loadkVA = 8
                else:
                    phase_loadkVA = 25

                recommended_PV_in_Kwp = request.POST.get('select_kwh')
                # get the value of the energy consumption dict, where key is the kWh selected
                annual_kwh = dict(EnergyConsumptionForm.KWh_CHOICES).get(recommended_PV_in_Kwp)
                
                PV_kWp = request.POST.get('myRangeSlider')
                has_storage = request.POST.get('storage')
                storage_kW = request.POST.get('storage_kw')

                # print the variables to check
                print(f"District key: {district_key}")
                print(f"District value: {district_value}")
                print(f"The selected phase load is: {phase_load}")
                print(f"Agreed kVA is: {phase_loadkVA}")
                print(f"Annual kWh is: {annual_kwh}")
                print(f"Recommended Kwp is: {recommended_PV_in_Kwp}" )
                print(f"Place of installment is: {place_of_installment}")
                print(f"Azimuth of PV: {azimuth_value}")
                print(f"Degrees of PV inclination: {inclination_PV}" )
                print(f"Users prefer to use: {userPower_profile}" )
                print(f"kWp of PV value: {PV_kWp}")
                print(f"Did User select Battery storage: {has_storage}")

                if has_storage == 'with_storage':
                    print(f"Battery kWh value: {storage_kW}")
                else:
                    storage_kW = 0
                    print('No storage selected')
            except KeyError:
                # Handle the case where an invalid key is provided
                return HttpResponse('Invalid request parameters')

            request.session['district_key'] = district_key
            request.session['place_of_installment'] = place_of_installment
            request.session['inclination_PV'] = inclination_PV
            request.session['userPower_profile'] = userPower_profile
            request.session['recommended_PV_in_Kwp'] = recommended_PV_in_Kwp
            request.session['annual_kwh'] = annual_kwh
            request.session['PV_kWp'] = PV_kWp
            request.session['has_storage'] = has_storage
            request.session['storage_kW'] = storage_kW
            request.session['phase_loadkVA'] = phase_loadkVA

        return redirect(reverse('simulation:dashboard'))  # redirect to function calculator

    else:
        form_district = PlaceOfInstallationForm()
        form_annual_kwh = EnergyConsumptionForm()
        form_phase_load = PhaseLoad()
    return render(request, 'simulation/calculator.html', context={'form_district': form_district, 
         'form_annual_kwh': form_annual_kwh,'form_phase_load': form_phase_load,})


# Calculation functions

# Calculate total investment
def calculate_total_investment(PV_kWp, battery_cost):
    Pv_cost = PV_kWp * 1500
    installation_cost = 400
    
    return Pv_cost + installation_cost + battery_cost

# Calculate annual savings and percentage
def calculate_annual_savings(annual_kwh, phase_loadkVA, battery_cost, userPower_profile, average_annual_production):
    annualConsumption = annual_kwh
    energyCost = 0.19 # €/kWh today
    annual_kWhCost = annualConsumption * energyCost
    # Ρυθμιζόμενες Χρεώσεις
    otherEnergyCharges = (phase_loadkVA * 0.52) + (annual_kwh * 0.0213) + (phase_loadkVA * 1) + (annual_kwh * 0.00844) + (annual_kwh*0.017) + (annual_kwh*energyCost*0.06)
    totalAnnualCost = annual_kWhCost + otherEnergyCharges

    # cases with battery storage and use profile to calculate self-consumption rate
    if battery_cost == 0 and userPower_profile == "day-power":
        selfConsumptionRate = 0.75
    elif battery_cost > 0 and userPower_profile == "day-power":
        selfConsumptionRate = 0.9
    elif battery_cost == 0 and userPower_profile == "night-power":
        selfConsumptionRate = 0.5
    elif battery_cost > 0 and userPower_profile == "night-power":
        selfConsumptionRate = 0.7
    else:
        selfConsumptionRate = 0.5

    # Μειωμένο Ποσό Ρυθμιζόμενων Χρεώσεων
    discountOtherEnergyCharges = otherEnergyCharges * selfConsumptionRate
    
    if average_annual_production >= annual_kwh:
        average_annual_savings = round( annual_kWhCost + discountOtherEnergyCharges )
    else:
        average_annual_savings = round( ( (annual_kWhCost - (annualConsumption - average_annual_production ) * energyCost) )  + discountOtherEnergyCharges)

    profitPercent =  round(average_annual_savings / totalAnnualCost * 100, 1)

    return average_annual_savings, profitPercent, totalAnnualCost, otherEnergyCharges

# Payback Period
def calculate_payback_period(total_investment, average_annual_savings):    
    payback_period = total_investment / average_annual_savings
    years = int(payback_period)
    months = round((payback_period - years) * 12)

    return f"{years} έτη & {months} μήνες"


def calculate_production(PV_kWp, azimuth_value, inclination_PV):
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

def calculate_roi(payback_period, total_cost):
    # Calculate the return on investment
    # based on the payoff period and the total cost
    # Return the result
    pass;

def calculate_lcoe(total_investment, average_annual_production, annual_kwh):
    # Calculate the levelized cost of electricity
    # based on the total cost, the annual production, and the user's annual usage
    # Return the result

    # lifetimePv = 25
    # discountRate = 0.05
    # annualreservationCost = 400 * 12
    # lcoe = ( total_investment + (annualreservationCost * lifetimePv) ) / discountRate
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
    
# simulation/templates/regulations.html
def regulations(request):     
    try:
        result = 'simulation/regulations.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")
    
# simulation/templates/info.html    
def info(request):          
    try:
        result = 'simulation/info.html'
        return render(request, result)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

# FUNCTION FOR THE CALCULATOR FORM SUBMIT
def user_form(request):

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


