from django.shortcuts import render
from django.http.response import Http404, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from .forms import *
from .models import *
import json
import numpy_financial as npf
import numpy as np
from datetime import datetime
import pvlib.iotools
import pvlib
from django.conf import settings
from django.contrib.sessions.models import Session

# Create your views here
# App level
# annual degardation aprox. 0.5%. After 25 years degradation almost 12.5%
annual_degradation_production = 1 + 0.005
cumulative_degradation  = 1.125
performance_degradation = 0.75

# Dictionary mapping PVGIS names to pvlib names
VARIABLE_MAP = {
    'G(h)': 'ghi',
    'Gb(n)': 'dni',
    'Gd(h)': 'dhi',
    'G(i)': 'poa_global',
    'Gb(i)': 'poa_direct',
    'Gd(i)': 'poa_sky_diffuse',
    'Gr(i)': 'poa_ground_diffuse',
    'H_sun': 'solar_elevation',
    'T2m': 'temp_air',
    'RH': 'relative_humidity',
    'SP': 'pressure',
    'WS10m': 'wind_speed',
    'WD10m': 'wind_direction',
}

# function using PVGIS API to get the solar data
def get_solar_data(latitude_value, longitude_value, inclination_value, azimuth_value):

    print(latitude_value,longitude_value, inclination_value, "Azimuth: ", azimuth_value)

    poa_data_2020, meta, input = pvlib.iotools.get_pvgis_hourly(latitude=latitude_value, longitude=longitude_value, 
                    start=2020, end=2020, raddatabase= 'PVGIS-SARAH2', components=True, 
                    surface_tilt=inclination_value, surface_azimuth=azimuth_value, outputformat='json', 
                    usehorizon=True, userhorizon=None, pvcalculation=False, 
                    peakpower=None, pvtechchoice='crystSi', mountingplace='free', 
                    loss=0, trackingtype=0, optimal_surface_tilt=False, optimalangles=False, 
                    url='https://re.jrc.ec.europa.eu/api/v5_2/', map_variables=True, timeout=30)


    poa_data_2020['poa_diffuse'] = poa_data_2020['poa_sky_diffuse'] + poa_data_2020['poa_ground_diffuse']
    poa_data_2020['poa_global'] = poa_data_2020['poa_direct'] + poa_data_2020['poa_diffuse']

    # Convert the index (time) to a separate column named 'time'
    poa_data_2020['time'] = poa_data_2020.index.strftime('%Y-%m-%d-%H:%M:%S')

    # Resample the data to monthly frequency and calculate the sum
    monthly_irradiance = round(poa_data_2020['poa_global'].resample('M').sum())

      # Calculate the annual solar irradiance
    annual_irradiance = round(monthly_irradiance.sum())

    # Convert the monthly irradiance Series to an array, annual as a sum and divide them by 1000 to convert from Wh/m2 to kWh/m2
    monthly_irradiance_array = np.array(monthly_irradiance / 1000)
    annual_irradiance = float(annual_irradiance / 1000)

    # Convert the NumPy array to a nested Python list
    monthly_irradiance_list = monthly_irradiance_array.tolist()

    # Print the list of monthly irradiance
    print(f"Monthly irradiance: {monthly_irradiance_list}, Annual irradiance:  {annual_irradiance}")

    # Convert the list to JSON format
    monthly_irradiance_json = json.dumps(monthly_irradiance_list)

    return monthly_irradiance_json, annual_irradiance, monthly_irradiance_list

def dashboard_results(request):   # simulation/templates/dashboard.html
    # Retrieving Data from Session
    if 'annual_consumption' and 'PV_kWp' in request.session:
        latitude_coords = float(request.session.get('latitude_coords'))
        longitude_coords = float(request.session.get('longitude_coords'))
        place_of_installment = request.session.get('place_of_installment')
        inclination_PV = float(request.session.get('inclination_PV'))
        shadings_slider_value = int(request.session.get('shadings_slider_value'))
        # azimuth type is already float
        azimuth_value = request.session.get('azimuth_value')
        userPower_profile = request.session.get('userPower_profile')
        phase_load = request.session.get('phase_load')
        phase_loadkVA = int(request.session.get('phase_loadkVA'))
        energy_cost = float(request.session.get('energy_cost'))
        annual_consumption = int(request.session.get('annual_consumption'))
        # panel_kWp & panel_efficiency are already float
        panel_kWp = request.session.get('panel_kWp')
        panel_efficiency = request.session.get('panel_efficiency')
        panel_cost = int(request.session.get('panel_cost'))
        panel_area = float(request.session.get('panel_area'))
        inverter_cost = int(request.session.get('inverter_cost'))
        installation_cost = int(request.session.get('installation_cost'))

        power_kWp_method = request.session.get('power_kWp_method')
        PV_kWp = float(request.session.get('PV_kWp'))
        slider_max_value = request.session.get('slider_max_value')
        has_storage = request.session.get('has_storage')
        battery_capacity_kwh = float(request.session.get('battery_capacity_kwh'))
        battery_cost = request.session.get('battery_cost')
        discount_PV = request.session.get('discount_PV')
        discount_battery = request.session.get('discount_battery')
        shadings_percentage = calculate_shade_percentage(shadings_slider_value)
        request.session['shadings_percentage'] = shadings_percentage

        # important check if the power is auto calculated
        if power_kWp_method == 'auto-power':
            try:
                monthly_irradiance_json = request.session.get('monthly_irradiance_json')
                annual_irradiance = request.session.get('annual_irradiance')
                monthly_irradiance_list = request.session.get('monthly_irradiance_list')
                monthly_panel_energy_produced_list = request.session.get('monthly_panel_energy_produced_list')
                monthly_panel_energy_produced_json = request.session.get('monthly_panel_energy_produced_json')
                number_of_panels_required = request.session.get('minimum_PV_panels')
                annual_PV_energy_produced = request.session.get('annual_production')
                special_production_per_panel = request.session.get('special_production_per_panel')
                total_panel_area = request.session.get('total_panel_area')

                print ("Annual PV energy produced calculated with request", annual_PV_energy_produced)
                print("****************")
                print("\nThe PV power was auto generated with ajax request!!!!!!\n")
                print(f"annual_irradiance: {annual_irradiance} and panels needed:{number_of_panels_required}")
                print(f"shadings_slider_value: {shadings_slider_value} and shadings_percentage:{shadings_percentage}")
                print("****************")

            except KeyError as e:
                    return HttpResponse(f"Error while retrieving session data: {str(e)}")
            except ValueError as e:
                return HttpResponse(f"Error while converting data: {str(e)}")
        else:  
            # PV kWp was manually given -> get data from PVGIS  
            monthly_irradiance_json, annual_irradiance, monthly_irradiance_list = get_solar_data(latitude_coords, longitude_coords, inclination_PV, azimuth_value)
            request.session['monthly_irradiance_list'] = monthly_irradiance_list
            request.session['annual_irradiance'] = annual_irradiance
            special_production_per_panel = round(annual_irradiance * panel_area * panel_efficiency * performance_degradation * shadings_percentage )
            number_of_panels_required = round(PV_kWp / panel_kWp )
            request.session['minimum_PV_panels'] = number_of_panels_required
            total_panel_area = round(number_of_panels_required * panel_area, 1)
            request.session['total_panel_area'] = total_panel_area
            # In manual mode, the rounded number of panel, must give us a ne kWp value for our system
            PV_kWp = round(number_of_panels_required * panel_kWp,1)
            annual_PV_energy_produced, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list = calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production_per_panel, number_of_panels_required, total_panel_area)
            request.session['monthly_panel_energy_produced_list'] = monthly_panel_energy_produced_list
            
            # two times self_consumption ratio??
            print ("annual_PV_energy_produced calculated after submit", annual_PV_energy_produced, "special_production_per_panel: ", special_production_per_panel)
            print("****************")
            print("\nThe PV power was manually given!!!!!!\n")
            print(f"annual_irradiance: {annual_irradiance} and number of panels calculated after submit: {PV_kWp} / {panel_kWp} = {number_of_panels_required}")
            print("****************")

        # Calculate the rest variables
        print(f"BATTERY VALUE: {battery_cost}, BATTERY VALUE TYPE: {type(battery_cost)}")
        print(f"PANEL PARAMETERS: kWp={panel_kWp}, efficiency={panel_efficiency}, cost={panel_cost}, area={panel_area}")
        print(f"INVERTER COST: {inverter_cost}, INSTALLATION COST: {installation_cost}")
        # two times self_consumption ratio??
        self_consumption_ratio = calculate_self_consumption_ratio(userPower_profile, annual_PV_energy_produced, has_storage, battery_capacity_kwh, annual_consumption)
        request.session['self_consumption_ratio'] = self_consumption_ratio
        total_investment, inverter_cost, battery_cost = calculate_total_investment(PV_kWp, phase_load, has_storage, battery_capacity_kwh, battery_cost, panel_cost, discount_PV, discount_battery, number_of_panels_required, inverter_cost, installation_cost)
        request.session['total_investment'] = total_investment
        request.session['inverter_cost'] = inverter_cost
        consumption_total_charges = calculate_consumption_total_charges(annual_consumption, phase_loadkVA, energy_cost)
        request.session['consumption_total_charges'] = consumption_total_charges
        self_consumed_energy, potential_self_consumed_energy, exported_energy = calculate_self_consumed_energy(annual_PV_energy_produced, annual_consumption, self_consumption_ratio)
        
        total_avoided_charges = calculate_total_avoided_charges(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, phase_loadkVA, energy_cost, consumption_total_charges, exported_energy)
        profitPercent, total_savings_potential, potential_kwh = calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, consumption_total_charges, total_avoided_charges, phase_loadkVA, energy_cost)
        total_savings, total_savings_array = calculate_total_savings(total_savings_potential)
        total_savings_array_json = json.dumps(total_savings_array)
        total_production_kwh_array, total_production_kwh = calculate_total_production_kwh(annual_PV_energy_produced, shadings_percentage)
        total_production_kwh_array_json = json.dumps(total_production_kwh_array)
        payback_period, payback_year_float = calculate_payback_period(total_investment, total_savings_potential,consumption_total_charges) #in months
        
        net_present_value = calculate_npv(total_investment, total_savings)
        maintenance_cost = calculate_maintenance_cost(total_investment)
        lcoe = calculate_lcoe(total_investment, maintenance_cost , total_production_kwh)
        roi, annualized_roi = calculate_roi(net_present_value, total_investment, total_savings)
        irr = calculate_irr(total_investment, total_savings_array)
        average_CO2 = round(calculate_CO2_emissions_reduced(annual_PV_energy_produced))
        trees_planted = round(calculate_equivalent_trees_planted(annual_PV_energy_produced))

        request.session['net_present_value'] = net_present_value
        request.session['maintenance_cost'] = maintenance_cost
        request.session['lcoe'] = lcoe
        request.session['roi'] = roi
        request.session['annualized_roi'] = annualized_roi
        request.session['irr'] = irr
        request.session['average_CO2'] = average_CO2
        request.session['trees_planted'] = trees_planted
        

        azimuth_text = transform_azimuth_text(int(azimuth_value))

        # dictionary with rendered variables
        context = {
            # form values
            'latitude_coords': latitude_coords,
            'longitude_coords': longitude_coords,
            'place_of_installment': place_of_installment,
            'panel_kWp': panel_kWp,
            'panel_efficiency': panel_efficiency,
            'panel_area': panel_area,
            'panel_cost': panel_cost,
            'azimuth_value': azimuth_value,
            'inclination_PV': int(inclination_PV),
            'azimuth_text': azimuth_text,
            'userPower_profile': userPower_profile,
            'phase_load': phase_load,
            'phase_loadkVA': phase_loadkVA,
            'annual_consumption': annual_consumption,
            'PV_kWp': PV_kWp,
            'slider_max_value': slider_max_value,
            'has_storage': has_storage,
            'battery_capacity_kwh': battery_capacity_kwh,
            'discount_PV': discount_PV,
            'discount_battery': discount_battery,
            'battery_cost': battery_cost,

            # calculated values
            'total_investment': total_investment,
            'number_of_panels_required': number_of_panels_required,
            'total_panel_area': total_panel_area,
            'payback_period': payback_period,
            'payback_year_float': payback_year_float,
            'profitPercent': profitPercent,
            'consumption_total_charges': consumption_total_charges,
            'total_avoided_charges': total_avoided_charges,
            'total_savings_potential': round(total_savings_potential),
            'potential_kwh': potential_kwh,
            'has_storage': has_storage,
            'total_savings': total_savings,
            'total_savings_array': total_savings_array,
            'total_savings_array_json': total_savings_array_json,
            'total_production_kwh': total_production_kwh, 
            'total_production_kwh_array': total_production_kwh_array,
            'total_production_kwh_array_json': total_production_kwh_array_json,
            'monthly_panel_energy_produced_list': monthly_panel_energy_produced_list,
            'monthly_irradiance_json': monthly_irradiance_json,
            'annual_irradiance': annual_irradiance,
            'annual_PV_energy_produced': annual_PV_energy_produced,
            'monthly_panel_energy_produced_json': monthly_panel_energy_produced_json,

            # economic models values
            'net_present_value': net_present_value,
            'lcoe': lcoe,
            'roi': roi,
            'annualized_roi': annualized_roi,
            'irr': irr,
            'average_CO2': average_CO2,
            'trees_planted': trees_planted,
        }

        try:
            result = 'simulation/dashboard.html'

            print('Total Investment:', total_investment,"euro", '& Περίοδος Απόσβεσης:', payback_period, "Έτη:", payback_year_float) 
            print(f"self_consumed_energy: {self_consumed_energy}, self_consumption_ratio: {self_consumption_ratio}")
            print(f'Total savings for 25 years: {total_savings}, NPV is: {total_savings} - {total_investment} = {net_present_value}')
            print("Αποφυγέν κόστος ρεύματος: ", total_avoided_charges, "& Ετήσιο Όφελος έως: ", total_savings_potential)
            print("Ολικές χρεώσεις για ετήσια κατανάλωση: ", consumption_total_charges)
            print(f"Annual Irradiance: {annual_irradiance}, Μέση Ετήσια Παραγωγή:: {annual_PV_energy_produced}")
            print(f"Each Panel monthly produced energy{monthly_panel_energy_produced_list}")
            print(f"Discount passed in dashboard: {discount_PV}% & {discount_battery}%.")
           
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

def calculator_form_fields_handler(request):    # simulation/templates/calculator.html
    if request.method == 'POST':
        print(request.POST)
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        form_phase_load = PhaseLoad(request.POST)

        if form_phase_load.is_valid(): # form_district.is_valid() and
            try:
                # initialization of variables
                latitude_coords = request.POST.get('latitude')
                longitude_coords = request.POST.get('longitude')
                place_of_installment = request.POST.get('installation')
                shadings_slider_value = request.POST.get('shadings_slider')
                # from now on pvlib has an 180 offset for azimuth aspect
                azimuth_value = float(request.POST.get('azimuth'))
                azimuth_value += 180
                inclination_PV = int(request.POST.get('inclination'))
                userPower_profile = request.POST.get('profile_consumption')
                energy_cost = float(request.POST.get('price_kwh'))
                annual_consumption = request.POST.get('annual_consumption')
                panel_kWp = float(request.POST.get('panel_kWp')) 
                # from Wp to kWp
                panel_kWp /= 1000 
                panel_efficiency = float(request.POST.get('panel_efficiency'))
                # from xx % to 0,xx %
                panel_efficiency = round(panel_efficiency / 100, 3)
                panel_area = request.POST.get('panel_area')
                panel_cost = request.POST.get('panel_cost')
                inverter_cost = request.POST.get('inverter_cost')
                installation_cost = request.POST.get('installation_cost')
                phase_load = request.POST.get('select_phase')

                if phase_load == "single_phase":
                    phase_loadkVA = 8
                    slider_max_value = 5
                else:
                    phase_loadkVA = 15
                    slider_max_value = 10.8

                power_kWp_method = request.POST.get('power_kWp_method')
                PV_kWp = request.POST.get('myRangeSliderHidden')
                has_storage = request.POST.get('storage')
                battery_capacity_kwh = request.POST.get('battery_capacity_kwh')
                battery_cost = request.POST.get('battery_cost')
                noDiscountRadio = request.POST.get('discount')

                if request.POST.get('battery_cost') is None or battery_cost == 'NaN' or battery_cost == 'αυτόματα' :
                    battery_cost = 0
                else:
                    battery_cost = int(battery_cost)

                if noDiscountRadio == 'no' or request.POST.get('discount_percent') is None and request.POST.get('discount_percent_battery') is None:
                    # The "no" radio button is selected
                    discount_PV = 0
                    discount_battery = 0
                elif request.POST.get('discount_percent') is None:
                    discount_PV = 0
                    discount_battery = int(request.POST.get('discount_percent_battery'))
                elif request.POST.get('discount_percent_battery') is None:
                    discount_battery = 0 
                    discount_PV = int(request.POST.get('discount_percent'))  
                else:
                    # The "yes" discount radio button is selected
                    discount_PV = int(request.POST.get('discount_percent'))
                    discount_battery = int(request.POST.get('discount_percent_battery'))
                
                # print the variables to check
                now = datetime.now()
                print("\n ######### Start of session of USER'S form: ", now, "#########")
                # print(f"District key: {district_irradiance}")
                # print(f"District value: {district_value}")
                print(f"Latitude: {latitude_coords}")
                print(f"Longitude: {longitude_coords}")
                print(f"Σκίαση επίπεδο: {shadings_slider_value}")
                print(f"Panel parameters are: {panel_kWp}Wp, {panel_area}m², {panel_efficiency}(%) & {panel_cost}€") 
                print(f"The selected phase load is: {phase_load}")
                print(f"Agreed kVA is: {phase_loadkVA}")
                print(f"Annual kWh consumed is: {annual_consumption}")
                print(f"Place of installment is: {place_of_installment}")
                print(f"Azimuth of PV: {azimuth_value}")
                print(f"Degrees of PV inclination: {inclination_PV}" )
                print(f"User's consumption profile: {userPower_profile}" )
                print(f"kWp of PV value: {PV_kWp}")
                print(f"Did User select Battery storage: {has_storage}")
                print(f"Τιμή κιλοβατώρας: {energy_cost}")
                
                if has_storage == 'with_storage':
                    print(f"Battery kWh value: {battery_capacity_kwh}")
                else:
                    battery_capacity_kwh = 0
                    print('No storage selected')
            except KeyError:
                # Handle the case where an invalid key is provided
                return HttpResponse('Invalid request parameters')

            # Storing Data in Session
            request.session['latitude_coords'] = latitude_coords
            request.session['longitude_coords'] = longitude_coords
            request.session['place_of_installment'] = place_of_installment
            request.session['shadings_slider_value'] = shadings_slider_value
            request.session['inclination_PV'] = inclination_PV 
            # adding the pvlib azimuth offset
            request.session['azimuth_value'] = azimuth_value
            request.session['userPower_profile'] = userPower_profile
            request.session['annual_consumption'] = annual_consumption
            request.session['PV_kWp'] = PV_kWp
            request.session['has_storage'] = has_storage
            request.session['battery_capacity_kwh'] = battery_capacity_kwh
            request.session['phase_loadkVA'] = phase_loadkVA
            request.session['phase_load'] = phase_load
            request.session['energy_cost'] = energy_cost
            request.session['panel_kWp'] = panel_kWp
            request.session['panel_efficiency'] = panel_efficiency
            request.session['panel_cost'] = panel_cost
            request.session['panel_area'] = panel_area
            request.session['inverter_cost'] = inverter_cost
            request.session['installation_cost'] = installation_cost
            request.session['discount_PV'] = discount_PV
            request.session['discount_battery'] = discount_battery
            request.session['power_kWp_method'] = power_kWp_method
            request.session['slider_max_value'] = slider_max_value
            request.session['battery_cost'] = battery_cost

            print(f"DISCOUNTS in session\n PV:{discount_PV}%, Battery:{discount_battery}%")

            return dashboard_results(request)
        else:
            # Form is not valid, handle the error or display a message
            return render(request, 'simulation/calculator.html', context={'form_phase_load': form_phase_load})
    else:
        # form_district = PlaceOfInstallationForm()
        form_phase_load = PhaseLoad()
    return render(request, 'simulation/calculator.html', context={'form_phase_load': form_phase_load,}) 
    #'form_district': form_district, 

# Ajax Request Calculation    url = simulation/ajax/
def calculate_power(request):
    print("\n!! The power is generated in the calculate_power function !!")
    # Initial assignment
    total_PV_life_years= 25
    annual_production = 0
    total_production = 0
    minimum_PV_panels = 0

    try:
        if request.method == 'POST':
            # Retrieve values from the JSON data
            data = json.loads(request.body)
        
            # Extract the values from the data object
            latitude_value = data.get('latitude')
            longitude_value = data.get('longitude')
            inclination_value = data.get('inclination')
            # from now on pvlib has an 180 offset for azimuth aspect 
            azimuth_value = data.get('azimuth')
            azimuth_value += 180 # pvlib tools subtract 180 deg from the given azimuth number
            place_instalment_value = data.get('place_instalment_value') # roof or terrace
            shading_value = data.get('shading_value') # values 1 to 3
            # Calculate the percentage of degradation due to shadings
            shadings_percentage = calculate_shade_percentage(shading_value)
            # Panel parameters
            panel_area = data.get('panel_area')
            panel_efficiency = data.get('panel_efficiency')
            panel_kWp_value = data.get('panel_kWp_value') # in kWp
            # Consumption profiles
            energy_consumption = data.get('annual_Kwh_value')
            consumption_profile_value = data.get('consumption_profile')
            slider_max_value = data.get('slider_max_value')
            print("PARAMETERS FOR CALCULATING THE REQUEST:", data)
            print(f"Σκίαση επίπεδο: {shading_value}, Ποσοστό σκίασης: {shadings_percentage}, Προφίλ Κατανάλωσης{consumption_profile_value}")

            # Call the get_solar_data function that uses the PVGIS API and retrieve the results
            monthly_irradiance_json, annual_irradiance, monthly_irradiance_list = get_solar_data(latitude_value, longitude_value, inclination_value, azimuth_value)
            # Store the monthly_irradiance_list in the session
            request.session['monthly_irradiance_json'] = monthly_irradiance_json
            request.session['annual_irradiance'] = annual_irradiance
            request.session['monthly_irradiance_list'] = monthly_irradiance_list

            # CALCULATIONS
            # Initial calculations 
            special_production_per_panel = round(annual_irradiance * panel_area * panel_efficiency * performance_degradation * shadings_percentage)
            total_consumption = energy_consumption * total_PV_life_years
            minimum_PV_panels = round((energy_consumption / special_production_per_panel) * cumulative_degradation)
            recommended_kWp  = round(minimum_PV_panels * panel_kWp_value, 1)
            annual_production  = round((minimum_PV_panels * special_production_per_panel) / cumulative_degradation)
            print("BEFORE WHILE: annual_production:", annual_production, "minimum_PV_panels:",  minimum_PV_panels)
            print(f"special_production_per_panel: {special_production_per_panel}")

            # If the production is degradated enough enlarge the PV system
            loop_passes = 0
            while annual_production <= energy_consumption:
                loop_passes +=1
                minimum_PV_panels +=1
                annual_production  = round(minimum_PV_panels * (special_production_per_panel / cumulative_degradation))
                print("IN WHILE LOOP: ADDED 1 more PV panel")

            total_production = annual_production * 25
            recommended_kWp  = round(minimum_PV_panels * panel_kWp_value, 1)
            print(f"IN CALCULATE POWER:\n recommended_kWp: {recommended_kWp}, total_production: {total_production}, annual_production: {annual_production}, minimum_PV_panels: {minimum_PV_panels}, loop_passes: {loop_passes} ")
            print('slider_max_value: ', slider_max_value)

            # check if recommended kWp is greater than house power load(slider) max value
            if recommended_kWp >= slider_max_value:
                print("@@@ The energy consumption exceeds solar production @@@")
                recommended_kWp = slider_max_value
                minimum_PV_panels = round(recommended_kWp / panel_kWp_value)
                annual_production = round(minimum_PV_panels * (special_production_per_panel / cumulative_degradation))
                print(f"--- new panel kWp: {recommended_kWp}, annual_production: {annual_production}, minimum_PV_panels: {minimum_PV_panels}")

            if place_instalment_value == 'roof':
                total_panel_area = round(minimum_PV_panels * panel_area, 1)
            else:
                # needs more space for terrace instead of roof
                total_panel_area = round(minimum_PV_panels * panel_area  * 1.5, 1)

            _, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list = calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production_per_panel, minimum_PV_panels, total_panel_area)

            request.session['monthly_panel_energy_produced_list'] = monthly_panel_energy_produced_list
            request.session['monthly_panel_energy_produced_json'] = monthly_panel_energy_produced_json
            request.session['minimum_PV_panels'] = minimum_PV_panels
            request.session['annual_production'] = annual_production
            request.session['special_production_per_panel'] = special_production_per_panel
            request.session['total_panel_area'] = total_panel_area
            print("$$ RESULTS in CALCULATE POWER: \nRecommended KWp PV system: ", recommended_kWp)
            print("Minimum Panels:", minimum_PV_panels)
            print("ANNUAL IRRADIANCE:", annual_irradiance)
            print("Monthly IRRADIANCE:", monthly_irradiance_list)
            print('Annual Consumption:', energy_consumption)
            print(f"Total area for {place_instalment_value}: {total_panel_area}" )
            print('Annual Production:', annual_production)
            
            print(f"Total production after 25 years, for {minimum_PV_panels} panels, efficiency {panel_efficiency*100}%, area {panel_area} m² and {panel_kWp_value}Wp is: {round(total_production)}")
            print(f"Total consumption after 25 years: {total_consumption}")

            response_data = {
                'special_production_per_panel': round(special_production_per_panel  / cumulative_degradation, 1),
                'recommended_kWp': recommended_kWp,
                'minimum_PV_panels': minimum_PV_panels,
                'total_panel_area': total_panel_area,
                'annual_production': annual_production,
                'monthly_panel_energy_produced_list': monthly_panel_energy_produced_list,
                'monthly_panel_energy_produced_json': monthly_panel_energy_produced_json,
            }
        
            return JsonResponse(response_data)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

def recalculate_pv_system_properties(request):
    print("\n!! PV system proporties recalculating with ajax request !!")
    annual_consumption = int(request.session.get('annual_consumption'))
    monthly_irradiance_list = request.session.get('monthly_irradiance_list')
    annual_irradiance = request.session.get('annual_irradiance')
    self_consumption_ratio = request.session.get('self_consumption_ratio')
    phase_loadkVA = int(request.session.get('phase_loadkVA'))
    energy_cost = float(request.session.get('energy_cost'))
    consumption_total_charges = request.session.get('consumption_total_charges')
    shadings_percentage = request.session.get('shadings_percentage')
    total_panel_area = float(request.session.get('total_panel_area'))
    net_present_value = request.session.get('net_present_value')
    inverter_cost = int(request.session.get('inverter_cost'))
    
    try:
        if request.method == 'POST':
            # Retrieve values from the JSON data and the session
            data = json.loads(request.body)

            changed_number_panels = int(data.get('changed_number_panels'))

            panel_kWp_value = request.session.get('panel_kWp')
            panel_area = float(request.session.get('panel_area'))
            panel_cost = int(request.session.get('panel_cost'))
            special_production_per_panel = request.session.get('special_production_per_panel')
            total_investment = request.session.get('total_investment')
            previous_pv_panels = request.session.get('minimum_PV_panels')
            phase_load = request.session.get('phase_load')
            pv_kwp_max_value = 5 if phase_load == "single_phase" else 10.8
            
            if changed_number_panels > previous_pv_panels:
                number_panels_difference = changed_number_panels - previous_pv_panels
                added_panels_bases_cost = (number_panels_difference * 90)
                new_total_investment = total_investment + (number_panels_difference * panel_cost) + added_panels_bases_cost
                new_panel_area = round(total_panel_area + (number_panels_difference*panel_area),1)
            else:
                number_panels_difference =  previous_pv_panels - changed_number_panels
                added_panels_bases_cost = (number_panels_difference * 90)
                new_total_investment = total_investment - (number_panels_difference * panel_cost) - added_panels_bases_cost
                new_panel_area = round(total_panel_area - (number_panels_difference*panel_area),1)

            recalculated_pv = round(changed_number_panels * panel_kWp_value, 1)
            # Use a while loop to limit recalculated_pv to pv_kwp_max_value
            while recalculated_pv > pv_kwp_max_value:
                changed_number_panels -= 1
                recalculated_pv = round(changed_number_panels * panel_kWp_value, 1)

            request.session['PV_kWp'] = recalculated_pv

        annual_PV_energy_produced, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list = calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production_per_panel, changed_number_panels, new_panel_area)
        self_consumed_energy, potential_self_consumed_energy, exported_energy = calculate_self_consumed_energy(annual_PV_energy_produced, annual_consumption, self_consumption_ratio)
        total_avoided_charges = calculate_total_avoided_charges(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, phase_loadkVA, energy_cost, consumption_total_charges, exported_energy)
        annual_savings =  calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy,consumption_total_charges, total_avoided_charges, phase_loadkVA, energy_cost)
        profitPercent, total_savings_potential, potential_kwh = calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, consumption_total_charges, total_avoided_charges, phase_loadkVA, energy_cost)
        total_savings, total_savings_array = calculate_total_savings(total_savings_potential)
        payback_period, payback_year_float = calculate_payback_period(new_total_investment, total_savings_potential, consumption_total_charges)
        new_total_production_kwh_array, new_total_production_kwh = calculate_total_production_kwh(annual_PV_energy_produced, shadings_percentage)
        net_present_value = calculate_npv(new_total_investment, total_savings)
        new_maintenance_cost = calculate_maintenance_cost(new_total_investment)
        new_lcoe = calculate_lcoe(new_total_investment, new_maintenance_cost , new_total_production_kwh)
        new_roi, new_annualized_roi = calculate_roi(net_present_value, new_total_investment, total_savings)
        new_irr = calculate_irr(new_total_investment, total_savings_array)
        new_average_CO2 = round(calculate_CO2_emissions_reduced(annual_PV_energy_produced))
        new_trees_planted = round(calculate_equivalent_trees_planted(annual_PV_energy_produced))

        print(f"NEW annual_PV_energy_produced: {annual_PV_energy_produced}")
        print(f"NEW self_consumed_energy: {self_consumed_energy}")
        print(f"NEW total_savings_potential: {total_savings_potential}")
        print(f"NEW payback_period: {payback_period}")
  
        response_data = {
            'recalculated_pv': recalculated_pv,
            'changed_number_panels': changed_number_panels,
            'total_investment': new_total_investment,
            'new_panel_area': new_panel_area,
            'annual_savings': annual_savings,
            'profitPercent': profitPercent,
            'total_savings_potential': total_savings_potential,
            'potential_kwh': potential_kwh,
            'total_savings': total_savings,
            'total_savings_array': total_savings_array,
            'payback_period': payback_period,
            'payback_year_float': payback_year_float,
            'new_total_production_kwh_array': new_total_production_kwh_array,
            'annual_PV_energy_produced': annual_PV_energy_produced,
            'monthly_panel_energy_produced_list': monthly_panel_energy_produced_list,
            'annual_consumption': annual_consumption,
            'pv_kwp_max_value': pv_kwp_max_value,
            'consumption_total_charges': consumption_total_charges,
            'net_present_value': net_present_value,
            'new_lcoe': new_lcoe,
            'new_roi': new_roi,
            'new_annualized_roi': new_annualized_roi,
            'new_irr': new_irr,
            'new_average_CO2': new_average_CO2,
            'new_trees_planted': new_trees_planted,
        }

        return JsonResponse(response_data)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")       

# Calculation functions
# OK
def calculate_total_investment(PV_kWp, phase_load, has_storage, battery_capacity_kwh, battery_cost, panel_cost, discount_PV, discount_battery, number_of_panels_required, inverter_cost, installation_cost):
    average_battery_cost_per_kW = 850 # average in €
    electric_materials = 100 # average cost in €
    initial_inverter_cost = inverter_cost

    # Cost of PV system is total panels * cost
    panel_bases_cost = 90 * number_of_panels_required # bases for the panels on roof or terrace, average cost per base
    Pv_panels_cost = round((number_of_panels_required * panel_cost) + panel_bases_cost)
    
    # for 0.1 - 5 kWp
    if phase_load == "single_phase":
        # inverters cost -> 700€-1200€ prices, hybrid inverters are expensive
        if has_storage == "with_storage" and battery_cost > 0:
            inverter_cost_auto = ( PV_kWp * 200 ) + ( (5 - PV_kWp) * 100 )  # 1-phase hybrid inverter and given battery cost 
            battery_cost = battery_cost
            print(f"total_investment 1st if" )
        elif has_storage == "with_storage" and battery_cost == 0:
            inverter_cost_auto = ( PV_kWp * 200 ) + ( (5 - PV_kWp) * 100 ) # 1-phase hybrid inverter for battery support
            battery_cost = round(battery_capacity_kwh * average_battery_cost_per_kW)
            print(f"total_investment 2nd if" )
        else:
            inverter_cost_auto = ( PV_kWp * 100 ) + ( (5 - PV_kWp) * 100 )# simple 1-phase PV inverter
            battery_cost = 0
            print(f"total_investment 3rd if" )
    # for 0.1 - 10.8 kWp
    elif phase_load == "3_phase":
        if has_storage == "with_storage" and battery_cost == 0:
            inverter_cost_auto = (PV_kWp * 250 ) + ( (10 - PV_kWp) * 100 )  # 3-phase hybrid inverter for battery support
            battery_cost = round(battery_capacity_kwh * average_battery_cost_per_kW)
        elif has_storage == "with_storage" and battery_cost > 0:
            inverter_cost_auto = (PV_kWp * 250 ) + ( (10 - PV_kWp) * 100 )  # 3-phase hybrid inverter and given battery cost
            battery_cost = battery_cost
        else:
            inverter_cost_auto = ( PV_kWp * 150 )+ ( (10 - PV_kWp) * 100 ) # simple 3-phase PV inverter
            battery_cost = 0
    else:
        battery_cost = 0

    if initial_inverter_cost > 0:
        inverter_cost = round(inverter_cost)
    elif initial_inverter_cost == 0:
        inverter_cost = round(inverter_cost_auto)
    

    # How much the PV system costs without battery
    Pv_system_cost = Pv_panels_cost + installation_cost + inverter_cost + electric_materials

    # If client/user is eligible to discounts
    if discount_PV > 0:
        print(f"Starting PV system price: {Pv_system_cost}")
        Pv_system_cost -= round(Pv_system_cost * (discount_PV / 100))
        print(f'Discount {discount_PV}% has been applied to PV system.')
        print(f'New PV system price is {Pv_system_cost}€.')
    if discount_battery > 0:
        print(f"Starting battery system price: {battery_cost}")
        battery_cost -= round(battery_cost * (discount_battery / 100))
        print(f'Discount {discount_battery}% has been applied to battery.')
        print(f'New battery price is {battery_cost}€.')

    total_investment = round(Pv_system_cost + battery_cost)
    print(f"*Total investment: {total_investment}\n PV total cost: {Pv_system_cost}\n PV panels' Cost: {Pv_panels_cost},\n Battery Cost: {battery_cost},\n Inverter: {inverter_cost} and PV kWp: {PV_kWp},")
   
    return total_investment, inverter_cost, battery_cost
# OK
def calculate_shade_percentage(shadings_slider_value):
    # solar production reduction percentage due to shadings
    if shadings_slider_value == 2:
        shadings_percentage = 0.85
    elif shadings_slider_value == 3:
        shadings_percentage = 0.6
    else:
        shadings_percentage = 1
    
    return shadings_percentage
# OK
def calculate_self_consumption_ratio(userPower_profile, annual_PV_energy_produced, has_storage, battery_capacity_kwh, annual_consumption):
    depth_battery_discharge = 0.8 #80% dod for lithium batteries
    solar_production_hours = 12
    self_consumption_hours = 0
    
    if userPower_profile == "day-power":
        print("1st condition day-power")
        self_consumption_hours = 10
    elif userPower_profile == "high-day-evening":
        print("2nd condition high-day-evening")
        self_consumption_hours = 8
    elif userPower_profile == "evening-power":
        print("3rd condition evening-power")
        self_consumption_hours = 4
    elif userPower_profile == "night-power":
        print("4th condition night-power")
        self_consumption_hours = 0

    self_consumption_ratio = round(self_consumption_hours / solar_production_hours,2) 

    print(f"self_consumption_ratio without battery is: {self_consumption_ratio}")

    if has_storage == "with_storage":
        daily_energy_production = round((annual_PV_energy_produced / 365) * self_consumption_ratio,2)
        daily_energy_consumption = round(annual_consumption / 365,2)
        if daily_energy_production == 0.0:
            battery_stored_energy = round(battery_capacity_kwh * depth_battery_discharge,2)
            self_consumption_hours = (12 * battery_stored_energy) / daily_energy_consumption
            print(f"daily_energy_production: {daily_energy_production}, daily_energy_consumption: {daily_energy_consumption}, self_consumption_hours: {self_consumption_hours}, battery_stored_energy: {battery_stored_energy}")
        elif daily_energy_production >= daily_energy_consumption:
            battery_stored_energy = daily_energy_production - daily_energy_consumption
            self_consumption_hours += (daily_energy_consumption + battery_stored_energy) / daily_energy_production
        else:
            battery_stored_energy = round(battery_capacity_kwh * depth_battery_discharge,2)
            self_consumption_hours += (daily_energy_consumption + battery_stored_energy) / daily_energy_production

        self_consumption_ratio = round(self_consumption_hours / solar_production_hours,2) 

        if self_consumption_ratio < 1.0:
            self_consumption_ratio = self_consumption_ratio
        else: 
            self_consumption_ratio = 1.0
        print(f"daily_energy_production: {daily_energy_production}, daily_energy_consumption: {daily_energy_consumption}, battery_stored_energy: {battery_stored_energy}")
        print(f"self_consumption_ratio with battery becomes: {self_consumption_ratio}")
        
    

    return self_consumption_ratio 
# OK
def calculate_self_consumed_energy(annual_PV_energy_produced, annual_consumption, self_consumption_ratio):

    potential_self_consumed_energy = round(annual_PV_energy_produced * self_consumption_ratio)

    # self_consumption_ratio = 0
    if potential_self_consumed_energy == 0:
        exported_energy_to_grid = annual_PV_energy_produced
        self_consumed_energy = potential_self_consumed_energy
        print(f"calculate self_consumed_energy, 1st potential_self_consumed_energy == 0")
    elif annual_PV_energy_produced > annual_consumption and potential_self_consumed_energy < annual_consumption:
        exported_energy_to_grid = annual_PV_energy_produced - potential_self_consumed_energy
        self_consumed_energy = potential_self_consumed_energy
        print(f"calculate self_consumed_energy, 2nd potential_self_consumed_energy < annual_consumption")
    elif annual_PV_energy_produced > annual_consumption and potential_self_consumed_energy >= annual_consumption:
        exported_energy_to_grid = annual_PV_energy_produced - annual_consumption
        self_consumed_energy = annual_consumption
        print(f"calculate self_consumed_energy, 3rd potential_self_consumed_energy >= annual_consumption")
    elif annual_PV_energy_produced < annual_consumption:
        exported_energy_to_grid = annual_PV_energy_produced - potential_self_consumed_energy
        self_consumed_energy = potential_self_consumed_energy
        print(f"calculate self_consumed_energy, 4th annual_PV_energy_produced < annual_consumption")
    else:
        exported_energy_to_grid = annual_PV_energy_produced - potential_self_consumed_energy
        self_consumed_energy = potential_self_consumed_energy
        print(f"calculate self_consumed_energy, else")

    print(f"4444444 in calculate self_consumed_energy: annual_PV_energy_produced:{annual_PV_energy_produced},self_consumed_energy: {self_consumed_energy} , self_consumption_ratio: {self_consumption_ratio}, exported_energy: {exported_energy_to_grid} ^^^^^^^^^")

    return self_consumed_energy, potential_self_consumed_energy, exported_energy_to_grid
# OK   
def calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production_per_panel, number_of_panels_required, total_panel_area):
    monthly_panel_energy_produced_list = []
    annual_PV_energy_produced = round( number_of_panels_required * special_production_per_panel / cumulative_degradation)
    print(f"88888888 In calculate PV energy: annual_PV_energy_produced: {annual_PV_energy_produced},special_production_per_panel:{special_production_per_panel}, number_of_panels_required: {number_of_panels_required}")
    print("annual_irradiance: ", annual_irradiance)

    for irradiance_month in monthly_irradiance_list:
        monthly_energy_produced = round(irradiance_month / (total_panel_area))
        monthly_panel_energy_produced_list.append(monthly_energy_produced)

    monthly_panel_energy_produced_json = json.dumps(monthly_panel_energy_produced_list)
    
    return annual_PV_energy_produced, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list
# OK
def calculate_consumption_total_charges(annual_consumption, phase_loadkVA, energy_cost):
    # πάγιο(0.52 €/kVA), ΔΙΑΝΟΜΗ 0,0213 €/kWh, ΜΕΤΑΦΟΡΑ 0.00844€/kWh, ΕΤΜΕΑΡ 0,017€/kWh, ΦΠΑ 6% * kWh * τιμή kWh, Συνολικό κόστος κατανάλωσης
    return round((phase_loadkVA * 0.52) + (annual_consumption * 0.0213) + (phase_loadkVA * 1) + (annual_consumption * 0.00844) + (annual_consumption*0.017) + (annual_consumption*energy_cost*0.06) + ( annual_consumption*energy_cost))
# OK
def calculate_total_charges_for_imported_energy(exported_energy, imported_energy, phase_loadkVA, energy_cost):
    # additional energy has full cost, but imported energy thas was primarily exported only has regulated charges
    if imported_energy > exported_energy:
        additional_imported_energy = imported_energy - exported_energy
        charges_for_additional_imported_energy = round(calculate_consumption_total_charges(additional_imported_energy, phase_loadkVA, energy_cost))
        regulated_charges = round( (exported_energy * 0.0213) + (exported_energy * 0.00844) )
        print(f'123 123 1st if : exported_energy: {exported_energy}, imported_energy: {imported_energy}, charges_for_additional_imported_energy: {charges_for_additional_imported_energy+regulated_charges}')
    # for night consumption and self_consumption_ratio = 0
    elif imported_energy == exported_energy:
        charges_for_additional_imported_energy = 0
        regulated_charges = round( (imported_energy * 0.0213) + (imported_energy * 0.00844) )
        print(f'123 123 2nd if : exported_energy: {exported_energy}, imported_energy: {imported_energy}, charges_for_additional_imported_energy: {charges_for_additional_imported_energy+regulated_charges}')
    elif exported_energy > imported_energy:
        regulated_charges = round( (imported_energy * 0.0213) + (imported_energy * 0.00844) )
        charges_for_additional_imported_energy = 0
        print(f'123 123 3rd if : exported_energy: {exported_energy}, imported_energy: {imported_energy}, charges_for_additional_imported_energy: {charges_for_additional_imported_energy+regulated_charges}')
    else:
        additional_imported_energy = 0
        charges_for_additional_imported_energy = 0
        new_imported_energy = exported_energy - imported_energy
        regulated_charges = round( (new_imported_energy * 0.0213) + (new_imported_energy * 0.00844) )
        print(f'123 123 else if : exported_energy: {exported_energy}, imported_energy: {imported_energy}, charges_for_additional_imported_energy: {charges_for_additional_imported_energy}')
    
     
    return charges_for_additional_imported_energy + regulated_charges 
# OK
def calculate_total_avoided_charges(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, phase_loadkVA, energy_cost, consumption_total_charges, exported_energy):

    # Calculate solar energy regulated cost sent back and forth to the grid 
    # first codition when self consumed energy can be greater than consumption, annual_consumption == self_consumed_energy
    if annual_PV_energy_produced > annual_consumption and annual_consumption == self_consumed_energy :
        imported_energy = 0
        total_charges_for_imported_energy = 0
        # Αν είναι πολύ μεγάλη η παραγωγή εξισώνεται η κατανάλωση και η ιδιοκατανάλωση σε kWh. Δημιουργείται μεγάλο περιθώριο κέρδους
        potential_energy =  potential_self_consumed_energy - annual_consumption
        total_avoided_charges = consumption_total_charges + calculate_consumption_total_charges(potential_energy, phase_loadkVA, energy_cost)
        print(f"9999 in total_avoided_charges 1st: exported_energy: {exported_energy}, imported_energy: {imported_energy}, potential_energy: {potential_energy}, total_charges_for_imported_energy: {total_charges_for_imported_energy}, total_avoided_charges: {total_avoided_charges} ")
    elif annual_PV_energy_produced > annual_consumption and self_consumed_energy < annual_consumption :  
        imported_energy = annual_consumption - self_consumed_energy
        imported_energy_charges = calculate_total_charges_for_imported_energy(exported_energy, imported_energy, phase_loadkVA, energy_cost)
        total_avoided_charges = consumption_total_charges - imported_energy_charges
        print(f"9999 in total_avoided_charges 2nd: exported_energy: {exported_energy}, imported_energy: {imported_energy}, total_avoided_charges: {total_avoided_charges} ")
    else: # annual_consumption > annual_PV_energy_produced
        # total imported
        imported_energy = annual_consumption - self_consumed_energy 
        # imported_additional_energy_charges = imported with full cost - imported with only regulated
        imported_additional_energy_charges = calculate_total_charges_for_imported_energy(exported_energy, imported_energy, phase_loadkVA, energy_cost)
        total_avoided_charges = calculate_consumption_total_charges(self_consumed_energy, phase_loadkVA, energy_cost) - imported_additional_energy_charges 
        if total_avoided_charges < 0:
            total_avoided_charges = 0
        print(f"9999 in total_avoided_charges 3rd: exported_energy: {exported_energy}, imported_energy: {imported_energy}, total_avoided_charges: {total_avoided_charges}, imported_additional_energy_charges: {imported_additional_energy_charges} ")
   
    return total_avoided_charges


# Calculate annual savings, profit Percentage, total_savings_potential
# OK
def calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy,consumption_total_charges, total_avoided_charges, phase_loadkVA, energy_cost):
    print("TEST in calculate_annual_savings\n")
    print(annual_consumption, annual_PV_energy_produced, self_consumed_energy, potential_self_consumed_energy, consumption_total_charges, total_avoided_charges, phase_loadkVA, energy_cost)
    print("TEST in calculate_annual_savings\n")

    if total_avoided_charges == 0:
        total_avoided_charges = 0
        total_savings_potential = 0
        potential_kwh = 0
    else:
        # Again self_consumed_energy >= annual_consumption, is valid when the potential self consumed is greater than consumption
        if  annual_PV_energy_produced > annual_consumption and self_consumed_energy >= annual_consumption:
            exported_energy_to_grid = potential_self_consumed_energy - annual_consumption
            total_savings_potential = round(total_avoided_charges)
            potential_kwh = round(exported_energy_to_grid)
            print(f"In calculate_annual_savings 1st if : self_consumed_energy: {self_consumed_energy}, total_savings_potential: {total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")
        elif annual_PV_energy_produced > annual_consumption and self_consumed_energy < annual_consumption:
            exported_energy_to_grid = annual_PV_energy_produced - self_consumed_energy
            total_savings_potential = round(total_avoided_charges) 
            potential_kwh = round(exported_energy_to_grid)
            print(f"In calculate_annual_savings 1st if : self_consumed_energy: {self_consumed_energy}, total_savings_potential: {total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")
        else: # annual_PV_energy_produced < annual_consumption
            exported_energy_to_grid = annual_PV_energy_produced - self_consumed_energy
            total_savings_potential = round(total_avoided_charges)
            potential_kwh = round(exported_energy_to_grid)
            print(f"In calculate_annual_savings else if : self_consumed_energy: {self_consumed_energy}, total_savings_potential: {total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")

    if total_savings_potential <= 0:
        profitPercent = 0
    else:
        profitPercent =  min(round(total_savings_potential / consumption_total_charges * 100, 1),100) 

    return profitPercent, total_savings_potential, potential_kwh

def calculate_total_savings(total_savings_potential):
    if total_savings_potential == 0:
        total_savings_array = [0]
        total_savings = 0
    # Calculate the total profit over 25 years
    # based on the annual savings
    # 1st year the total savings is the total_savings_potential
    total_savings_array = [0, total_savings_potential]
    total_savings = total_savings_potential
    
    for i in range(1, 25):
        total_savings += round(total_savings_potential / ( ( annual_degradation_production ) ** i))
        total_savings_array.append(total_savings)

    return total_savings, total_savings_array

def calculate_payback_period(total_investment, total_savings_potential, consumption_total_charges): 
    print('6767 total_savings_potential type: ', type(total_savings_potential))
    if total_savings_potential == 0:
        payback_period = 0
        payback_year_float = 0
    else:
        years_to_overcome_investment = 0
        total_savings = []
        # starting_invest = total_investment

        # Calculate years and months independently from that point 
        if total_savings_potential > (consumption_total_charges * annual_degradation_production):
            while sum(total_savings) <= total_investment:
                savings = consumption_total_charges
                total_savings.append( savings )
                years_to_overcome_investment += 1

            subtraction = sum(total_savings) - total_investment
            monthly_savings = total_savings [years_to_overcome_investment - 2] /12
            years = years_to_overcome_investment - 1
            months = round(12 - (subtraction/monthly_savings) )
            payback_year_float  = round(years + (months / 13),2)

            if months == 1:
                payback_period = f"{years} έτη & {months} μήνας"
            else:
                payback_period = f"{years} έτη & {months} μήνες"
        else:
            total_savings_potential = total_savings_potential

            # Find the point where savings exceed investment
            while sum(total_savings) <= total_investment:
                try:
                    result = total_savings_potential / (annual_degradation_production ** years_to_overcome_investment)
                    # Check if the result is very small (close to zero)
                    if abs(result) < 1e-1:  # You can adjust the threshold as needed
                        payback_period = "0"
                        payback_year_float = 0
                        break  # Break the loop if the result is close to zero
            
                    total_savings.append( result )
                    years_to_overcome_investment += 1

                except OverflowError:
                    # Handle the overflow error here, e.g., provide an error message
                    payback_period = "Calculation error: Result too large" 
                    payback_year_float = 0

                subtraction = sum(total_savings) - total_investment
                monthly_savings = total_savings [years_to_overcome_investment - 2] /12
                years = years_to_overcome_investment - 1
                months = round(12 - (subtraction/monthly_savings) )
                payback_year_float  = round(years + (months / 13),2)

                if months == 1:
                    payback_period = f"{years} έτη & {months} μήνας"
                else:
                    payback_period = f"{years} έτη & {months} μήνες"

    return payback_period, payback_year_float  

def calculate_total_production_kwh(annual_PV_energy_produced, shadings_percentage):
    # 1st year the total production is the annual_PV_energy_produced
    total_production_kwh = annual_PV_energy_produced
    total_production_kwh_array =[0, annual_PV_energy_produced]
    print(f"3333333 in calculate_total_production_kwh, annual_PV_energy_produced {annual_PV_energy_produced}")

    for i in range(1, 25):
        total_production_kwh += annual_PV_energy_produced / ( annual_degradation_production ** i) * shadings_percentage
        total_production_kwh_array.append(round(total_production_kwh))

    print("Total kWh production after 25 years: ", round(total_production_kwh))

    return total_production_kwh_array, round(total_production_kwh)

def transform_azimuth_text(azimuth_value):
    if azimuth_value == 180:
        azimuth_text = "Νότιος Προσανατολισμός"
    elif azimuth_value == 225:
        azimuth_text = "Ν.Δ Προσανατολισμός"
    elif azimuth_value == 270:
        azimuth_text = "Δυτικός Προσανατολισμός"
    elif azimuth_value == 315:
        azimuth_text = "Β.Δ Προσανατολισμός"
    elif azimuth_value == 360:
        azimuth_text = "Βόρειος Προσανατολισμός"
    elif azimuth_value == 45:
        azimuth_text = "Β.Α Προσανατολισμός"
    elif azimuth_value == 90:
        azimuth_text = "Ανατολικός Προσανατολισμός"
    elif azimuth_value == 135:
        azimuth_text = "Ν.Α Προσανατολισμός"

    return azimuth_text

def calculate_maintenance_cost(total_investment):
    cost_rate = (1.5 / 100) * 25 # 1.5% της συνολικής επένδυσης ανά έτος

    return total_investment * cost_rate

def calculate_npv(total_investment, total_savings):
    # Calculate the net present value without cash flow, only logistics
    # based on the total savings and the total investment
    # annual_value_discount_rate = 0.3, annual_electricity_inflation = 0.2
    # Return the result
    if total_savings == 0:
        return 0
    else:
        return total_savings - total_investment

def calculate_roi(net_present_value, total_investment, total_savings):
    # Calculate the return on investment
    # Return the result
    if total_savings == 0:
        roi = 0
        annualized_roi = 0
        return roi, annualized_roi
    else:
        roi = round(net_present_value / total_investment * 100, 2)
        annualized_roi = round(((total_savings / total_investment) ** (1/25) -1) *100, 2)
        
        print('Return On Investment: ', roi)
        print('Annualized Return On Investment: ', annualized_roi)

        return roi, annualized_roi

def calculate_lcoe(total_investment, maintenance_cost, total_production_kwh):
    # Calculate the levelized cost of electricity
    # based on the total cost, and the user's annual usage
    # Return the result
    if total_production_kwh == 0:
        return 0
    else:
        lcoe = round(( total_investment + maintenance_cost ) / total_production_kwh, 3)
        
        print('Levelized Cost of Electricity: ', lcoe)

        return lcoe
   
def calculate_irr(total_investment, total_savings_array):
    # Calculate the return on investment
    # Return the result
    if sum(total_savings_array) == 0:
        return 0
    else:
        initial_investment = -total_investment
        saving_flows = total_savings_array.copy()  # Create a copy of the total_savings_array
        
        saving_flows.insert(0, initial_investment)  # Insert the initial investment at index 0
        
        irr = round(npf.irr(saving_flows)* 100, 2) 

        print('Internal Rate: ', irr)
        
        return irr   
   
def calculate_CO2_emissions_reduced(annual_PV_energy_produced):
   # Calculate the equivalent CO2 emissions, reduced due to solar production
    if annual_PV_energy_produced > 0:
        average_CO2 = 0.04 # ~ 40 g CO2 eq/kWh for a year

        return average_CO2 * annual_PV_energy_produced # kg per year
    else:
        return 0
  
def calculate_equivalent_trees_planted(annual_PV_energy_produced):
    if annual_PV_energy_produced > 0:
        percentage_trees_per_kWh = 0.02

        return annual_PV_energy_produced * percentage_trees_per_kWh 
    else:
        return 0

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
