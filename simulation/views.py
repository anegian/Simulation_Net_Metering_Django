from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import Http404, HttpResponse
from django.http import JsonResponse
from .forms import *
from .models import *
import json
import numpy_financial as npf
from datetime import datetime

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
            annual_kwh = int(request.session.get('annual_kwh'))
            PV_kWp = float(request.session.get('PV_kWp'))
            has_storage = request.session.get('has_storage')
            storage_kw = float(request.session.get('storage_kw'))

            total_investment, inverter_cost = calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kw)
            average_annual_production, total_loss_percentage, percentage_production_loss, inclination_percentage, production_per_KW = calculate_average_annual_production(PV_kWp, district_irradiance, azimuth_value, inclination_PV)
            average_annual_savings, profitPercent, total_annual_cost, regulated_charges = calculate_annual_savings(annual_kwh, phase_loadkVA, has_storage, userPower_profile, average_annual_production)
            
            
            total_savings, total_savings_array = calculate_total_savings(average_annual_savings)
            total_savings_array_json = json.dumps(total_savings_array)
            total_production_kwh_array, total_production_kwh = calculate_total_production_kwh(average_annual_production)
            total_production_kwh_array_json = json.dumps(total_production_kwh_array)
            month_production_array = calculate_month_production(average_annual_production)
            month_production_array_json = json.dumps(month_production_array)

            payback_period = calculate_payback_period(total_investment, average_annual_savings)

            net_present_value = calculate_npv(total_investment, total_savings)
            maintenance_cost = calculate_maintenance_cost(total_investment, inverter_cost)
            lcoe = calculate_lcoe(total_investment, maintenance_cost , total_production_kwh)
            roi, annualized_roi = calculate_roi(net_present_value, total_investment, total_savings)
            irr = calculate_irr(total_investment, total_savings_array)
            average_CO2 = round(calculate_CO2_emissions_reduced(average_annual_production))
            trees_planted = round(calculate_equivalent_trees_planted(average_annual_production))

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
            'annual_kwh': annual_kwh,
            'PV_kWp': PV_kWp,
            'has_storage': has_storage,
            'storage_kw': storage_kw,
            'total_investment': total_investment,
            'payback_period': payback_period,
            'average_annual_savings': average_annual_savings,
            'profitPercent': profitPercent,
            'total_annual_cost': total_annual_cost,
            'regulated_charges': regulated_charges,
            'has_storage': has_storage,
            'average_annual_production': average_annual_production,  
            'total_savings': total_savings,
            'total_savings_array': total_savings_array,
            'total_savings_array_json': total_savings_array_json,
            'total_production_kwh': total_production_kwh, 
            'total_production_kwh_array': total_production_kwh_array,
            'total_production_kwh_array_json': total_production_kwh_array_json,
            'month_production_array': month_production_array,
            'month_production_array_json': month_production_array_json,
            'net_present_value': net_present_value,
            'lcoe': lcoe,
            'roi': roi,
            'annualized_roi': annualized_roi,
            'irr': irr,
            'average_CO2': average_CO2,
            'trees_planted': trees_planted,
            }

            result = 'simulation/dashboard.html'

            print('Total Investment:', total_investment,"euro", 'Average annual Savings: ', average_annual_savings, '& Περίοδος Απόσβεσης:', payback_period) 
            print(f'Total savings for 25 years: {total_savings}, NPV is: {total_savings} - {total_investment} = {net_present_value}')
            print("Ετήσιο κόστος ρεύματος, μαζί με ρυθμιζόμενες χρεώσεις, χωρίς δημοτικούς φόρους: ", total_annual_cost, "& Ετήσιο Όφελος: ", average_annual_savings)
            print("Ρυθμιζόμενες χρεώσεις: ", regulated_charges, "Μέση Ετήσια Παραγωγή:", average_annual_production)  # Add this line for debugging
            print('ideal Production kWh per kWp: ', production_per_KW)
            print("Total production loss percent, calculating azimuth and inclination: ", total_loss_percentage, 'Inclination percent: ', inclination_percentage, 'Azimuth percent:', percentage_production_loss, '\n')
            now = datetime.now()
            print("######### End time of this session: ", now, "#########\n")
            return render(request, result, context)
        except Http404:
            return Http404("404 Generic Error")
    else:
        try:
            result = 'simulation/dashboard_empty.html'
            return render(request, result)
        except Http404:      # not use bare except
            return Http404("404 Generic Error")

    
def calculator_forms_choice(request):    # simulation/templates/calculator.html

    if request.method == 'POST':
        print(request.POST)
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form_district = PlaceOfInstallationForm(request.POST)
        form_phase_load = PhaseLoad(request.POST)
        
        
        if form_district.is_valid() and form_phase_load.is_valid():
            try:
                # initialization of variables
                district_irradiance = request.POST.get('select_district')
                district_value = dict(PlaceOfInstallationForm.DISTRICT_CHOICES).get(district_irradiance)
                place_of_installment = request.POST.get('installation')
                azimuth_value = request.POST.get('azimuth')
                inclination_PV = request.POST.get('inclination')
                userPower_profile = request.POST.get('power_option')
                annual_kwh = request.POST.get('annual_kwh')

                phase_load = request.POST.get('select_phase')

                if phase_load == "single_phase":
                    phase_loadkVA = 8
                else:
                    phase_loadkVA = 15

                PV_kWp = request.POST.get('myRangeSlider')
                has_storage = request.POST.get('storage')
                storage_kw = request.POST.get('storage_kw')

                # print the variables to check
                now = datetime.now()
                print("\n ######### Start of session of USER'S form: ", now, "#########")
                print(f"District key: {district_irradiance}")
                print(f"District value: {district_value}")
                print(f"The selected phase load is: {phase_load}")
                print(f"Agreed kVA is: {phase_loadkVA}")
                print(f"Annual kWh is: {annual_kwh}")
                print(f"Place of installment is: {place_of_installment}")
                print(f"Azimuth of PV: {azimuth_value}")
                print(f"Degrees of PV inclination: {inclination_PV}" )
                print(f"Users use profile: {userPower_profile}" )
                print(f"kWp of PV value: {PV_kWp}")
                print(f"Did User select Battery storage: {has_storage}")

                if has_storage == 'with_storage':
                    print(f"Battery kWh value: {storage_kw}")
                else:
                    storage_kw = 0
                    print('No storage selected')
            except KeyError:
                # Handle the case where an invalid key is provided
                return HttpResponse('Invalid request parameters')

            request.session['district_irradiance'] = district_irradiance
            request.session['place_of_installment'] = place_of_installment
            request.session['inclination_PV'] = inclination_PV
            request.session['azimuth_value'] = azimuth_value
            request.session['userPower_profile'] = userPower_profile
            request.session['annual_kwh'] = annual_kwh
            request.session['PV_kWp'] = PV_kWp
            request.session['has_storage'] = has_storage
            request.session['storage_kw'] = storage_kw
            request.session['phase_loadkVA'] = phase_loadkVA
            request.session['phase_load'] = phase_load

        return redirect(reverse('simulation:dashboard'))  # redirect to function calculator

    else:
        form_district = PlaceOfInstallationForm()
        form_phase_load = PhaseLoad()
    return render(request, 'simulation/calculator.html', context={'form_district': form_district, 
        'form_phase_load': form_phase_load,})


# Calculation functions

def calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kw):
    installation_cost = 400 # average cost in €

    each_panel_kW = 0.4  # average 400W each panel
    each_panel_average_cost = 250  # average in € for 400W panel
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
            inverter_cost = ( PV_kWp * 200 ) + ( (5 - PV_kWp) * 100 )  # 1-phase hybrid inverter for battery support
            battery_cost = storage_kw * average_battery_cost_per_kW
        else:
            inverter_cost = ( PV_kWp * 100 ) + ( (5 - PV_kWp) * 100 )# simple 1-phase PV inverter
            battery_cost = 0
    # for 2 - 10 kWp
    elif phase_load == "3_phase":
        if has_storage == "with_storage":
            inverter_cost = (PV_kWp * 250 ) + ( (10 - PV_kWp) * 100 )  # 3-phase hybrid inverter for battery support
            battery_cost = storage_kw * average_battery_cost_per_kW
        else:
            inverter_cost = ( PV_kWp * 150 )+ ( (10 - PV_kWp) * 100 ) # simple 3-phase PV inverter
            battery_cost = 0
    else:
        battery_cost = 0

    print(f"Inverter: {inverter_cost}")
    print(f"Battery Cost: {battery_cost}")
    print(f"Required Pv panels: {number_of_panels_required}")
    print(f"PV panels' Cost: {Pv_cost}")

    total_investment = Pv_cost + installation_cost + battery_cost + inverter_cost + panel_bases_cost + electric_materials

    return total_investment, inverter_cost

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
        print('\n^^^ User must pick a larger pv system in kWp, in order to reduce annual electricity costs!!! ^^^\n')
    else:
        annual_kWh_difference_cost = (average_annual_production - annual_consumption) * (0.0213 * 0.00844)
        difference_savings = (average_annual_production - annual_consumption) * energy_cost
        average_annual_savings = round(annual_kWh_cost + discount_regulated_charges + difference_savings - annual_kWh_difference_cost)
        total_annual_cost = annual_kWh_cost + regulated_charges
        

    profitPercent =  round(average_annual_savings / total_annual_cost * 100, 1)

    return average_annual_savings, profitPercent, total_annual_cost, regulated_charges

def calculate_payback_period(total_investment, average_annual_savings): 
    annual_production_degradation = 0.06   
    years = 0
    minimum_savings_needed = 0
    element_index = 0

    while total_investment >= minimum_savings_needed and element_index < 26:
        minimum_savings_needed += average_annual_savings / ( ( 1 + annual_production_degradation ) ** element_index)
        element_index+=1
        print(minimum_savings_needed, years, element_index)

    payback_period = element_index
    print('Period simple division:', total_investment / average_annual_savings)

    return f"{payback_period} έτη"

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

def calculate_total_production_kwh(average_annual_production):

    total_production_kwh = 0
    total_production_kwh_array =[]
    annual_production_degradation = 0.006

    for i in range(1, 26):
        total_production_kwh += average_annual_production / ( ( 1+annual_production_degradation) ** i)
        total_production_kwh_array.append(total_production_kwh)

    print("Total kWh production after 25 years: ", total_production_kwh)

    return total_production_kwh_array, total_production_kwh

def calculate_month_production(average_annual_production):
    month_production_array = []
    monthly_percentages = [5.2, 6, 8.1, 9.5, 10.5, 10.7, 11.6, 10.9, 9.8, 7.8, 5.4, 4.5]
    
    for percentage in monthly_percentages:
        monthly_production = round((percentage / 100) * average_annual_production)
        month_production_array.append(monthly_production)

    print('Each month production: ', month_production_array)
    
    return month_production_array 
   
def calculate_total_savings(average_annual_savings):
    # Calculate the total profit over 25 years
    # based on the annual production
    # Return the result
    total_savings_array = []
    total_savings = 0
    annual_production_degradation = 0.006
    
    for i in range(1, 26):
        total_savings += average_annual_savings / ( ( 1 + annual_production_degradation ) ** i)
        total_savings_array.append(total_savings)

    return total_savings, total_savings_array
   
def calculate_maintenance_cost(total_investment, inverter_cost):
    cost_rate = (1.5 / 100) * 25 # 1.5% της συνολικής επένδυσης ανά έτος

    return total_investment * cost_rate

def calculate_npv(total_investment, total_savings):
    # Calculate the net present value without cash flow, only logistics
    # based on the total savings and the total investment
    # annual_value_discount_rate = 0.3, annual_electricity_inflation = 0.2
    # Return the result
    
    return total_savings - total_investment

def calculate_roi(net_present_value, total_investment, total_savings):
    # Calculate the return on investment
    # Return the result
    roi = round(net_present_value / total_investment * 100, 2)
    annualized_roi = round(((total_savings / total_investment) ** (1/25) -1) *100, 2)
    
    print('Return On Investment: ', roi)
    print('Annualized Return On Investment: ', annualized_roi)

    return roi, annualized_roi

def calculate_lcoe(total_investment, maintenance_cost, total_production_kwh):
    # Calculate the levelized cost of electricity
    # based on the total cost, and the user's annual usage
    # Return the result

    lcoe = round(( total_investment + maintenance_cost ) / total_production_kwh, 3)
    
    print('Levelized Cost of Electricity: ', lcoe)

    return lcoe
   
def calculate_irr(total_investment, total_savings_array):
    # Calculate the return on investment
    # Return the result
    initial_investment = -total_investment
    saving_flows = total_savings_array.copy()  # Create a copy of the total_savings_array
    
    saving_flows.insert(0, initial_investment)  # Insert the initial investment at index 0
    
    irr = round(npf.irr(saving_flows), 25)

    print('Internal Rate: ', irr)
    
    return irr   
   
def calculate_CO2_emissions_reduced(average_annual_production):
   # Calculate the equivalent CO2 emissions, reduced due to solar production
   average_CO2 = 0.04 # ~ 40 g CO2 eq/kWh for a year
   
   return average_CO2 * average_annual_production # kg per year
  
def calculate_equivalent_trees_planted(average_annual_production):
   percentage_trees_per_kWh = 0.02
   
   return average_annual_production * percentage_trees_per_kWh 

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
    
# simulation/templates/about.html    
def about(request):          
    try:
        result = 'simulation/about.html'
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


