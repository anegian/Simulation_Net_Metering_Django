
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse
from .forms import *
from .models import *

# Create your views here
# App level

def dashboard_results(request):   # simulation/templates/dashboard.html
 
    if 'district_irradiance' in request.session:
        try:
            district_irradiance = int(request.session.get('district_irradiance'))
            district_value = request.session.get('district_value')
            place_of_installment = request.session.get('place_of_installment')
            inclination_PV = request.session.get('inclination_PV')
            azimuth_value = request.session.get('azimuth_value')
            userPower_profile = request.session.get('userPower_profile')
            phase_load = request.session.get('phase_load')
            phase_loadkVA = int(request.session.get('phase_loadkVA'))
            recommended_PV_in_Kwp = request.session.get('recommended_PV_in_Kwp')
            annual_kwh = int(request.session.get('annual_kwh'))
            PV_kWp = int(request.session.get('PV_kWp'))
            has_storage = request.session.get('has_storage')
            storage_kW = int(request.session.get('storage_kW'))

            total_investment = calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kW)
            average_annual_production, total_loss_percentage, percentage_production_loss, inclination_percentage, production_per_KW = calculate_average_annual_production(PV_kWp, district_irradiance, azimuth_value, inclination_PV)
            average_annual_savings, profitPercent, total_annual_cost, regulated_charges = calculate_annual_savings(annual_kwh, phase_loadkVA, has_storage, userPower_profile, average_annual_production)
            payback_period = calculate_payback_period(total_investment, average_annual_savings)

            # dictionary with rendered variables
            context = {
            'district_irradiance': district_irradiance,
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
            'total_annual_cost': total_annual_cost,
            'regulated_charges': regulated_charges,
            'has_storage': has_storage,
            'average_annual_production': average_annual_production,
            }

            result = 'simulation/dashboard.html'

            print('Total Investment:', total_investment,"euro", '& Περίοδος Απόσβεσης:', payback_period) 
            print("Ετήσιο κόστος ρεύματος, μαζί με ρυθμιζόμενες χρεώσεις, χωρίς δημοτικούς φόρους: ", total_annual_cost, "& Ετήσιο Όφελος: ", average_annual_savings)
            print("Ρυθμιζόμενες χρεώσεις: ", regulated_charges, "Μέση Ετήσια Παραγωγή:", average_annual_production)  # Add this line for debugging
            print('ideal Production kWh per kWp: ', production_per_KW)
            print("Total production loss '%' due azimuth and inclination: ", total_loss_percentage, 'Inclination percent: ', inclination_percentage, 'Azimuth percent:', percentage_production_loss)
            
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
                district_irradiance = request.POST.get('select_district')
                district_value = dict(PlaceOfInstallationForm.DISTRICT_CHOICES).get(district_irradiance)
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
                print(f"District key: {district_irradiance}")
                print(f"District value: {district_value}")
                print(f"The selected phase load is: {phase_load}")
                print(f"Agreed kVA is: {phase_loadkVA}")
                print(f"Annual kWh is: {annual_kwh}")
                print(f"Recommended Kwp is: {recommended_PV_in_Kwp}" )
                print(f"Place of installment is: {place_of_installment}")
                print(f"Azimuth of PV: {azimuth_value}")
                print(f"Degrees of PV inclination: {inclination_PV}" )
                print(f"Users use profile: {userPower_profile}" )
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

            request.session['district_irradiance'] = district_irradiance
            request.session['place_of_installment'] = place_of_installment
            request.session['inclination_PV'] = inclination_PV
            request.session['azimuth_value'] = azimuth_value
            request.session['userPower_profile'] = userPower_profile
            request.session['recommended_PV_in_Kwp'] = recommended_PV_in_Kwp
            request.session['annual_kwh'] = annual_kwh
            request.session['PV_kWp'] = PV_kWp
            request.session['has_storage'] = has_storage
            request.session['storage_kW'] = storage_kW
            request.session['phase_loadkVA'] = phase_loadkVA
            request.session['phase_load'] = phase_load

        return redirect(reverse('simulation:dashboard'))  # redirect to function calculator

    else:
        form_district = PlaceOfInstallationForm()
        form_annual_kwh = EnergyConsumptionForm()
        form_phase_load = PhaseLoad()
    return render(request, 'simulation/calculator.html', context={'form_district': form_district, 
         'form_annual_kwh': form_annual_kwh,'form_phase_load': form_phase_load,})


# Calculation functions

# Calculate total investment
def calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kW):
    installation_cost = 400 # average cost in €

    each_panel_kW = 0.4  # average 400W each panel
    each_panel_average_cost = 300  # average in € for 400W panel
    number_of_panels_required = round(PV_kWp / each_panel_kW)
    panel_bases_cost = 90 * number_of_panels_required # bases for the panels on roof or taratsa, average cost per base
    electric_materials = 100 # average cost in €
    inverter_cost = 0
    average_battery_cost_per_kW = 850 # average in €
    Pv_cost = number_of_panels_required * each_panel_average_cost
    
    # for 2 - 5 kWp
    if phase_load == "single_phase":
        # inverters cost -> 700€-1200€ prices, hybrid inverters are expensive
        if has_storage == "with_storage":
            inverter_cost = ( PV_kWp * 250 ) + ( (5 - PV_kWp) * 100 )  # 1-phase hybrid inverter for battery support
            battery_cost = storage_kW * average_battery_cost_per_kW
        else:
            inverter_cost = ( PV_kWp * 150 ) + ( (5 - PV_kWp) * 100 )# simple 1-phase PV inverter
            battery_cost = 0
    # for 2 - 10 kWp
    elif phase_load == "3_phase":
        if has_storage == "with_storage":
            inverter_cost = (PV_kWp * 300 ) + ( (10 - PV_kWp) * 100 )  # 3-phase hybrid inverter for battery support
            battery_cost = storage_kW * average_battery_cost_per_kW
        else:
            inverter_cost = ( PV_kWp * 150 )+ ( (10 - PV_kWp) * 100 ) # simple 3-phase PV inverter
            battery_cost = 0
    else:
        battery_cost = 0


    print(f"Inverter: {inverter_cost}")
    print(f"Battery Cost: {battery_cost}")
    print(f"Required Pv panels: {number_of_panels_required}")
    print(f"PV panels' Cost: {Pv_cost}")
    return Pv_cost + installation_cost + battery_cost + inverter_cost + panel_bases_cost + electric_materials

# Calculate annual savings and percentage
def calculate_annual_savings(annual_kwh, phase_loadkVA, has_storage, userPower_profile, average_annual_production):
    annual_consumption = annual_kwh
    energy_cost = 0.19 # €/kWh today
    annual_kWh_cost = annual_consumption * energy_cost
    # Ρυθμιζόμενες Χρεώσεις
    regulated_charges = (phase_loadkVA * 0.52) + (annual_consumption * 0.0213) + (phase_loadkVA * 1) + (annual_consumption * 0.00844) + (annual_consumption*0.017) + (annual_consumption*energy_cost*0.06)
    # Συνολική Χρέωση καταναλισκόμενου ρεύματος χωρίς net metering
    total_annual_cost = annual_kWh_cost + regulated_charges

    # cases with battery storage and use profile to calculate self-consumption rate
    if has_storage == "with_storage":
        if userPower_profile == "day-power":
            self_consumption_rate = 0.9
        else:
            self_consumption_rate = 0.75
    else:
        if userPower_profile == "day-power":
            self_consumption_rate = 0.7
        else:
            self_consumption_rate = 0.5

    # Μειωμένο Ποσό Ρυθμιζόμενων Χρεώσεων
    discount_regulated_charges = regulated_charges * self_consumption_rate

    if annual_consumption > average_annual_production:
        annual_kWh_difference_cost = (annual_consumption -average_annual_production) * (energy_cost + 0.0213 + 0.00844)
        average_annual_savings = round(annual_kWh_cost + discount_regulated_charges - annual_kWh_difference_cost)
        total_annual_cost = annual_kWh_cost + regulated_charges + annual_kWh_difference_cost
    else:
        annual_kWh_difference_cost = (average_annual_production - annual_consumption) * (0.0213 * 0.00844)
        difference_savings = (average_annual_production - annual_consumption) * energy_cost
        average_annual_savings = round(annual_kWh_cost + discount_regulated_charges + difference_savings - annual_kWh_difference_cost)
        total_annual_cost = annual_kWh_cost + regulated_charges
        

    profitPercent =  round(average_annual_savings / total_annual_cost * 100, 1)

    return average_annual_savings, profitPercent, total_annual_cost, regulated_charges

# Payback Period
def calculate_payback_period(total_investment, average_annual_savings):    
    payback_period = total_investment / average_annual_savings
    years = int(payback_period)
    months = round((payback_period - years) * 12)

    return f"{years} έτη & {months} μήνες"


def calculate_average_annual_production(PV_kWp, district_irradiance, azimuth_value, inclination_PV):
    # Calculate the annual production of the PV system
    # based on the system's specifications and the inclination
    # Return the result

    if azimuth_value == '90':
        percentage_production_loss = 1.14
    elif azimuth_value == '45':
        percentage_production_loss = 1.04
    elif azimuth_value == '-90':
        percentage_production_loss = 1.13
    elif azimuth_value == '-45':
        percentage_production_loss = 1.03
    else:
        percentage_production_loss = 1 # ideal azimuth is south so no loss

    if inclination_PV == '30': # ideal inclination
        inclination_percentage = 1
    elif inclination_PV == '45':
        inclination_percentage = 1.018
    elif inclination_PV == '15':
        inclination_percentage = 1.025
    elif inclination_PV == '0':
        inclination_percentage = 1.12
    else:
        inclination_percentage = 1

    production_per_KW = district_irradiance * PV_kWp 
    total_loss_percentage = percentage_production_loss * inclination_percentage
    average_annual_production = production_per_KW / total_loss_percentage

    return average_annual_production, total_loss_percentage, percentage_production_loss, inclination_percentage,production_per_KW   # in kWh

def calculate_total_profit(average_annual_production):
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


