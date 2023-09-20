from django.shortcuts import render, redirect
from django.urls import reverse
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
        power_kWp_method = request.session.get('power_kWp_method')
        PV_kWp = float(request.session.get('PV_kWp'))
        has_storage = request.session.get('has_storage')
        storage_kw = float(request.session.get('storage_kw'))
        discount_PV = request.session.get('discount_PV')
        discount_battery = request.session.get('discount_battery')
        shadings_percentage = calculate_shade_percentage(shadings_slider_value)

        # important check if the power is auto calculated
        if power_kWp_method == 'auto-power':
            try:
                monthly_irradiance_json = request.session.get('monthly_irradiance_json')
                annual_irradiance = request.session.get('annual_irradiance')
                monthly_irradiance_list = request.session.get('monthly_irradiance_list')
                number_of_panels_required = request.session.get('minimumPanels')
                annual_PV_energy_produced = request.session.get('annual_production')
                print ("Annual PV energy produced calculated with request", annual_PV_energy_produced)
                print("****************")
                print("\nThe PV power was auto generated with ajax request!!!!!!\n")
                print(f"annual_irradiance: {annual_irradiance} and panels needed:{number_of_panels_required}")
                print("****************")

            except KeyError as e:
                    return HttpResponse(f"Error while retrieving session data: {str(e)}")
            except ValueError as e:
                return HttpResponse(f"Error while converting data: {str(e)}")
        else:  
            # PV kWp was manually given -> get data from PVGIS  
            monthly_irradiance_json, annual_irradiance, monthly_irradiance_list = get_solar_data(latitude_coords, longitude_coords, inclination_PV, azimuth_value)
            special_production = annual_irradiance * panel_area * panel_efficiency * 0.75
            diminishing_factors = cumulative_degradation / shadings_percentage
            number_of_panels_required = round((PV_kWp / panel_kWp) * diminishing_factors )
            annual_PV_energy_produced, _, _ = calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production, number_of_panels_required, diminishing_factors)
            self_consumption_ratio = calculate_self_consumption_ratio(has_storage, userPower_profile, annual_PV_energy_produced, annual_consumption)
            print ("annual_PV_energy_produced calculated after submit", annual_PV_energy_produced)
            print("****************")
            print("\nThe PV power was manually given!!!!!!\n")
            print(f"annual_irradiance: {annual_irradiance} and number of panels calculated after submit: {number_of_panels_required}")
            print("****************")

        # Calculate the rest variables
        self_consumption_ratio = calculate_self_consumption_ratio(has_storage, userPower_profile, annual_PV_energy_produced, annual_consumption)
        total_investment, inverter_cost = calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kw, panel_cost, discount_PV, discount_battery, number_of_panels_required)
        consumption_total_charges = calculate_consumption_total_charges(annual_consumption, phase_loadkVA, energy_cost)
        self_consumed_energy = calculate_self_consumed_energy(annual_PV_energy_produced, self_consumption_ratio)
        _, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list = calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, panel_area, panel_efficiency, number_of_panels_required)
        total_avoided_charges, total_charges_for_exported_energy = calculate_total_avoided_charges(annual_consumption, annual_PV_energy_produced, self_consumed_energy, phase_loadkVA, energy_cost, consumption_total_charges)
        average_annual_savings, profitPercent, total_savings_potential, potential_kwh = calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, consumption_total_charges, total_avoided_charges, total_charges_for_exported_energy, phase_loadkVA, energy_cost)
        total_savings, total_savings_array = calculate_total_savings(average_annual_savings)
        total_savings_array_json = json.dumps(total_savings_array)
        total_production_kwh_array, total_production_kwh = calculate_total_production_kwh(annual_PV_energy_produced, shadings_percentage)
        total_production_kwh_array_json = json.dumps(total_production_kwh_array)
        payback_period, payback_year_float = calculate_payback_period(total_investment, average_annual_savings) #in months

        net_present_value = calculate_npv(total_investment, total_savings)
        maintenance_cost = calculate_maintenance_cost(total_investment, inverter_cost)
        lcoe = calculate_lcoe(total_investment, maintenance_cost , total_production_kwh)
        roi, annualized_roi = calculate_roi(net_present_value, total_investment, total_savings)
        irr = calculate_irr(total_investment, total_savings_array)
        average_CO2 = round(calculate_CO2_emissions_reduced(annual_PV_energy_produced))
        trees_planted = round(calculate_equivalent_trees_planted(annual_PV_energy_produced))
        total_panel_area = round(number_of_panels_required * panel_area, 1)
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
            'has_storage': has_storage,
            'storage_kw': storage_kw,
            'discount_PV': discount_PV,
            'discount_battery': discount_battery,

            # calculated values
            'total_investment': total_investment,
            'number_of_panels_required': number_of_panels_required,
            'total_panel_area': total_panel_area,
            'payback_period': payback_period,
            'payback_year_float': payback_year_float,
            'average_annual_savings': average_annual_savings,
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

            print('Total Investment:', total_investment,"euro", 'Average annual Savings: ', average_annual_savings, '& Περίοδος Απόσβεσης:', payback_period, "Έτη:", payback_year_float) 
            print(f'Total savings for 25 years: {total_savings}, NPV is: {total_savings} - {total_investment} = {net_present_value}')
            print("Αποφυγέν κόστος ρεύματος: ", total_avoided_charges, "& Ετήσιο Όφελος: ", average_annual_savings)
            print("Ολικές χρεώσεις για ετήσια κατανάλωση: ", consumption_total_charges, "Πιθανό επιπλέον όφελος", total_savings_potential)
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

def calculator_forms_choice(request):    # simulation/templates/calculator.html
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
                inclination_PV = request.POST.get('inclination')
                userPower_profile = request.POST.get('power_option')
                energy_cost = int(request.POST.get('price_kwh'))
                # to become decimal
                if energy_cost >= 100:
                    energy_cost /= 1000
                else:
                    energy_cost /= 100

                annual_consumption = request.POST.get('annual_consumption')
                panel_kWp = float(request.POST.get('panel_kWp')) 
                # from Wp to kWp
                panel_kWp /= 1000 
                panel_efficiency = float(request.POST.get('panel_efficiency'))
                # from xx % to 0,xx %
                panel_efficiency /= 100
                panel_area = request.POST.get('panel_area')
                panel_cost = request.POST.get('panel_cost')
                phase_load = request.POST.get('select_phase')

                if phase_load == "single_phase":
                    phase_loadkVA = 8
                else:
                    phase_loadkVA = 15

                power_kWp_method = request.POST.get('power_kWp_method')
                PV_kWp = request.POST.get('myRangeSliderHidden')
                has_storage = request.POST.get('storage')
                storage_kw = request.POST.get('storage_kw')
                number_of_panels_required = int(request.POST.get('minimumPanels'))
                noDiscountRadio = request.POST.get('discount')

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
                print(f"Panel parameters are: {panel_kWp}Wp, {panel_area}m², {panel_efficiency}(%) & {panel_cost}€") 
                print(f"The selected phase load is: {phase_load}")
                print(f"Agreed kVA is: {phase_loadkVA}")
                print(f"Annual kWh consumed is: {annual_consumption}")
                print(f"Place of installment is: {place_of_installment}")
                print(f"Azimuth of PV: {azimuth_value}")
                print(f"Degrees of PV inclination: {inclination_PV}" )
                print(f"Users use profile: {userPower_profile}" )
                print(f"kWp of PV value: {PV_kWp}")
                print(f"Did User select Battery storage: {has_storage}")
                print(f"Number of panels in session: {number_of_panels_required}")
                print(f"Τιμή κιλοβατώρας: {energy_cost}")
                
                if has_storage == 'with_storage':
                    print(f"Battery kWh value: {storage_kw}")
                else:
                    storage_kw = 0
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
            request.session['storage_kw'] = storage_kw
            request.session['phase_loadkVA'] = phase_loadkVA
            request.session['phase_load'] = phase_load
            request.session['energy_cost'] = energy_cost
            request.session['panel_kWp'] = panel_kWp
            request.session['panel_efficiency'] = panel_efficiency
            request.session['panel_cost'] = panel_cost
            request.session['panel_area'] = panel_area
            request.session['minimumPanels'] = number_of_panels_required
            request.session['discount_PV'] = discount_PV
            request.session['discount_battery'] = discount_battery
            request.session['power_kWp_method'] = power_kWp_method

            print(f"DISCOUNTS in session\n PV:{discount_PV}%, Battery:{discount_battery}%")

            # return redirect(reverse('simulation:dashboard'))  # redirect to dashboard html
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
            azimuth_value += 180
            panel_area = data.get('panel_area')
            panel_efficiency = data.get('panel_efficiency')
            energy_consumption = data.get('annual_Kwh_value')
            panel_Wp_value = data.get('panel_Wp_value')
            place_instalment_value = data.get('place_instalment_value')
            shading_value = data.get('shading_value')
            shadings_percentage = calculate_shade_percentage(shading_value)
            consumption_profile_value = data.get('consumption_profile')
            print(f"consumption_profile_value in calculate power: {consumption_profile_value}")
            

            # να προστεθεί το ποσοστό ιδιοκατατανάλωσης

            print("PARAMETERS FOR CALCULATING THE REQUEST:", data)
            print(f"Σκίαση επίπεδο: {shading_value}, Ποσοστό σκίασης: {shadings_percentage}, Προφίλ Κατανάλωσης{consumption_profile_value}")

        
            # Call the get_solar_data function and retrieve the results
            monthly_irradiance_json, annual_irradiance, monthly_irradiance_list = get_solar_data(latitude_value, longitude_value, inclination_value, azimuth_value)

            # Store the monthly_irradiance_list in the session
            request.session['monthly_irradiance_json'] = monthly_irradiance_json
            request.session['annual_irradiance'] = annual_irradiance
            request.session['monthly_irradiance_list'] = monthly_irradiance_list

            print("\n!! The power is generated in the calculate_power function !!") #test print

            # kWh/m2 * m2 -> kWh
            special_production = annual_irradiance * panel_area * panel_efficiency * 0.75
            total_consumption = energy_consumption * 25 
            total_production = 0
            minimum_PV_panels = 0
            annual_production = 0

# Required PV System Size (kWp) = ( Annual Electricity Consumption (kWh) / (annual_irradiance (kWh/m²/year) × System Efficiency)) / (1 - Shading Factor) / self_consumption_ratio

            # while total_production < total_consumption:
            #     minimum_PV_panels += 1
            #     annual_production = minimum_PV_panels * special_production
            #     total_production = annual_production * 25 / cumulative_degradation
            #     print("total_production: ",total_production, "annual_production:", annual_production)
            

            # if shadings_percentage < 1:
            #     # Μείωση Παραγωγής  *  0.85
            #     annual_reduced_production = annual_production * shadings_percentage
            #     total_reduced_production = annual_reduced_production * 25 / cumulative_degradation
            #     # Διαφορά μειωμένης παραγωγής από αρχική
            #     production_required = annual_production - annual_reduced_production 
            #     minimum_PV_panels += round((production_required / shadings_percentage) / special_production)
                
            #     annual_required_production = round(minimum_PV_panels * special_production)
            #     annual_production = annual_required_production
            #     total_new_production = round((annual_required_production * 25 / cumulative_degradation) * shadings_percentage)
            #     print("If minimum_PV_panels", minimum_PV_panels, "1st total_production", total_reduced_production, "annual_reduced_production:",annual_reduced_production, "total_new_production:",total_new_production, "annual_required_production", annual_required_production)
            
            # Initial calculations 
            diminishing_factors = cumulative_degradation / shadings_percentage
            minimum_PV_panels = round((energy_consumption / special_production) * diminishing_factors)
            recommended_kWp  = minimum_PV_panels * panel_Wp_value
            annual_production  = minimum_PV_panels * special_production / diminishing_factors

            print("BEFORE WHILE: annual_production:", annual_production, "diminishing_factors: ", diminishing_factors, "minimum_PV_panels:",  minimum_PV_panels)

            i = 0
            while annual_production <= energy_consumption:
                i+=1
                minimum_PV_panels +=1
                annual_production  = minimum_PV_panels * special_production / diminishing_factors
                print("IN WHILE LOOP: ADDED 1 more PV panel")

            total_production = annual_production * 25
            print("IN CALCULATE POWER:\n total_production: ",total_production, "annual_production:", annual_production, "minimum_PV_panels:", minimum_PV_panels, "i: ", i )

            request.session['annual_production'] = annual_production

            if place_instalment_value == 'roof':
                total_area = minimum_PV_panels * panel_area    
            else:
                # needs more space for terrace instead of roof
                total_area = minimum_PV_panels * panel_area  * 1.5 

            print("ANNUAL IRRADIANCE:", annual_irradiance)
            print("Monthly IRRADIANCE:", monthly_irradiance_list)
            print('Annual Consumption:', energy_consumption)
            print("Minimum Panels:", minimum_PV_panels)
            print(f"Total area for {place_instalment_value}: {total_area}" )
            print('Annual Production:', annual_production)
            print(f"Total production after 25 years, for {minimum_PV_panels} panels, efficiency {panel_efficiency*100}%, area {panel_area} m² and {round(panel_Wp_value*1000)}Wp is: {round(total_production)}")
            print(f"Total consumption after 25 years: {total_consumption}")
            print("Recommended KWp PV system: ", recommended_kWp)

            response_data = {
                'special_production': round(special_production),
                'recommended_kWp': recommended_kWp,
                'minimum_PV_panels': round(minimum_PV_panels),
                'total_area': round(total_area, 2),
            }
        
            return JsonResponse(response_data)
    except Http404:      # not use bare except
        return Http404("404 Generic Error")

# Calculation functions
def calculate_total_investment(PV_kWp, phase_load, has_storage, storage_kw, panel_cost, discount_PV, discount_battery, number_of_panels_required):
    installation_cost = 500 # average cost in €
    electric_materials = 100 # average cost in €
    inverter_cost = 0
    average_battery_cost_per_kW = 850 # average in €
    # Cost of PV system is total panels * cost
    panel_bases_cost = 90 * number_of_panels_required # bases for the panels on roof or terrace, average cost per base
    Pv_panels_cost = round((number_of_panels_required * panel_cost) + panel_bases_cost)
    
    # for 0.1 - 5 kWp
    if phase_load == "single_phase":
        # inverters cost -> 700€-1200€ prices, hybrid inverters are expensive
        if has_storage == "with_storage":
            inverter_cost = ( PV_kWp * 200 ) + ( (5 - PV_kWp) * 100 )  # 1-phase hybrid inverter for battery support
            battery_cost = round(storage_kw * average_battery_cost_per_kW)
        else:
            inverter_cost = ( PV_kWp * 100 ) + ( (5 - PV_kWp) * 100 )# simple 1-phase PV inverter
            battery_cost = 0
    # for 0.1 - 10.8 kWp
    elif phase_load == "3_phase":
        if has_storage == "with_storage":
            inverter_cost = (PV_kWp * 250 ) + ( (10 - PV_kWp) * 100 )  # 3-phase hybrid inverter for battery support
            battery_cost = round(storage_kw * average_battery_cost_per_kW)
        else:
            inverter_cost = ( PV_kWp * 150 )+ ( (10 - PV_kWp) * 100 ) # simple 3-phase PV inverter
            battery_cost = 0
    else:
        battery_cost = 0

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
   
    return total_investment, inverter_cost

def calculate_shade_percentage(shadings_slider_value):
    # solar production reduction percentage due to shadings
    if shadings_slider_value == 2:
        shadings_percentage = 0.85 
    elif shadings_slider_value == 3:
        shadings_percentage = 0.6
    else:
        shadings_percentage = 1
    
    return shadings_percentage

def calculate_PV_energy_produced(monthly_irradiance_list, annual_irradiance, special_production, number_of_panels_required, diminishing_factors):
    monthly_panel_energy_produced_list = []
    annual_PV_energy_produced = round( number_of_panels_required * special_production / diminishing_factors)
    print(f"88888888 In calculate PV energy: annual_PV_energy_produced: {annual_PV_energy_produced},special_production:{special_production}, number_of_panels_required: {number_of_panels_required}")

    for irradiance_month in monthly_irradiance_list:
        monthly_energy_produced = round(irradiance_month * (special_production / annual_irradiance) * diminishing_factors)
        monthly_panel_energy_produced_list.append(monthly_energy_produced)

    monthly_panel_energy_produced_json = json.dumps(monthly_panel_energy_produced_list)
    
    return annual_PV_energy_produced, monthly_panel_energy_produced_json, monthly_panel_energy_produced_list

def calculate_consumption_total_charges(annual_consumption, phase_loadkVA, energy_cost):
    # πάγιο(0.52 €/kVA), ΔΙΑΝΟΜΗ 0,0213 €/kWh, ΜΕΤΑΦΟΡΑ 0.00844€/kWh, ΕΤΜΕΑΡ 0,017€/kWh, ΦΠΑ 6% * kWh * τιμή kWh, Συνολικό κόστος κατανάλωσης
    return round((phase_loadkVA * 0.52) + (annual_consumption * 0.0213) + (phase_loadkVA * 1) + (annual_consumption * 0.00844) + (annual_consumption*0.017) + (annual_consumption*energy_cost*0.06) + ( annual_consumption*energy_cost))

def calculate_total_charges_for_exported_energy(exported_energy, phase_loadkVA, energy_cost):
    charges_for_exported_energy = round((phase_loadkVA * 0.52) + (phase_loadkVA * 1) + (exported_energy * 0.017) + (exported_energy * energy_cost*0.06) + ( exported_energy * energy_cost))
    regulated_charges = round( (exported_energy * 0.0213) + (exported_energy * 0.00844) )
     
    return charges_for_exported_energy - regulated_charges 

def calculate_self_consumed_energy(annual_PV_energy_produced, self_consumption_ratio):

    print(f"4444444 in calculate_self_consumed_energy: {annual_PV_energy_produced * self_consumption_ratio} , self_consumption_ratio: {self_consumption_ratio} ^^^^^^^^^")

    return round(annual_PV_energy_produced * self_consumption_ratio)
    
def calculate_total_avoided_charges(annual_consumption, annual_PV_energy_produced, self_consumed_energy, phase_loadkVA, energy_cost, consumption_total_charges):
    
    # Calculate solar energy regulated cost sent back and forth to the grid 
    if self_consumed_energy >= annual_consumption: 
        exported_energy = annual_PV_energy_produced - self_consumed_energy
        total_charges_for_exported_energy = calculate_total_charges_for_exported_energy(exported_energy, phase_loadkVA, energy_cost)
        total_avoided_charges = consumption_total_charges + total_charges_for_exported_energy
    elif annual_consumption > self_consumed_energy and annual_consumption < annual_PV_energy_produced :
        exported_energy = annual_consumption - self_consumed_energy
        total_charges_for_exported_energy = calculate_total_charges_for_exported_energy(exported_energy, phase_loadkVA, energy_cost)
        total_avoided_charges = consumption_total_charges + total_charges_for_exported_energy 
    else: # annual_consumption > self_consumed_energy and annual_consumption >= annual_PV_energy_produced
        additional_kWh_from_grid = (annual_consumption - annual_PV_energy_produced)
        additional_kWh_total_charges = calculate_consumption_total_charges(additional_kWh_from_grid, phase_loadkVA, energy_cost)
        exported_energy = annual_PV_energy_produced - self_consumed_energy
        total_charges_for_exported_energy = calculate_total_charges_for_exported_energy(exported_energy, phase_loadkVA, energy_cost)
        total_avoided_charges = consumption_total_charges + total_charges_for_exported_energy
    
    return total_avoided_charges, total_charges_for_exported_energy

def calculate_self_consumption_ratio(has_storage, userPower_profile, annual_PV_energy_produced, annual_consumption ):
    # # cases with battery storage and use profile to calculate self-consumption rate
    # if has_storage == "with_storage":
    #     if userPower_profile == "day-power":
    #         self_consumption_ratio = 0.9
    #     elif userPower_profile == "high-day-evening":
    #         self_consumption_ratio = 0.85
    #     elif userPower_profile == "evening-power":
    #         self_consumption_ratio = 0.80
    #     else:
    #         self_consumption_ratio = 0.75
    # else:
    #     if userPower_profile == "day-power":
    #         self_consumption_ratio = 0.8
    #     elif userPower_profile == "high-day-evening":
    #         self_consumption_ratio = 0.65
    #     elif userPower_profile == "evening-power":
    #         self_consumption_ratio = 0.6
    #     else:
    #         self_consumption_ratio = 0.5

    daily_energy_production = annual_PV_energy_produced / 365
    daily_energy_consumption = annual_consumption / 365

    if has_storage == "with_storage":
        self_consumption_ratio  = 1.0
    else:
        self_consumption_ratio  = 1.0
    
    if userPower_profile == "day-power":
        print("1st condition")
        if daily_energy_production >= daily_energy_consumption:
            exported_solar_energy = (daily_energy_consumption - daily_energy_consumption) 
            self_consumption_ratio = exported_solar_energy / daily_energy_production
            print(f"1st condition - daily_energy_production: {daily_energy_production}, daily_energy_consumption: {daily_energy_consumption} ")
        else:
            self_consumption_ratio = 1.0
            print("1st condition - default")
    elif userPower_profile == "high-day-evening":
        print("2nd condition")
        if daily_energy_production >= daily_energy_consumption:
            exported_solar_energy = (daily_energy_consumption - daily_energy_consumption) 
            self_consumption_ratio = exported_solar_energy / daily_energy_production
        else:
            self_consumption_ratio = 1.0
    elif userPower_profile == "evening-power":
        print("3rd condition")
        if daily_energy_production >= daily_energy_consumption:
            exported_solar_energy = (daily_energy_consumption - daily_energy_consumption) 
            self_consumption_ratio = exported_solar_energy / daily_energy_production
        else:
            self_consumption_ratio = 1.0
    elif userPower_profile == "night-power":
        print("4th condition")
        if daily_energy_production >= daily_energy_consumption:
            exported_solar_energy = (daily_energy_consumption - daily_energy_consumption) 
            self_consumption_ratio = exported_solar_energy / daily_energy_production
        else:
            self_consumption_ratio = 1.0

    print(f"self_consumption_ratio in calculation method is: {self_consumption_ratio}")

    return self_consumption_ratio
    
# Calculate annual savings, profit Percentage, total_savings_potential
def calculate_annual_savings(annual_consumption, annual_PV_energy_produced, self_consumed_energy, consumption_total_charges, total_avoided_charges, total_charges_for_exported_energy, phase_loadkVA, energy_cost):
    print("TEST in calculate_annual_savings\n")
    print(annual_consumption, annual_PV_energy_produced, self_consumed_energy, consumption_total_charges, total_avoided_charges, total_charges_for_exported_energy, phase_loadkVA, energy_cost)
    print("TEST in calculate_annual_savings\n")

    
    if  annual_PV_energy_produced > annual_consumption and self_consumed_energy > annual_consumption:
        difference_consumed = annual_PV_energy_produced - annual_consumption
        average_annual_savings = round(total_avoided_charges)
        total_savings_potential = round(calculate_consumption_total_charges(difference_consumed, phase_loadkVA, energy_cost) - total_charges_for_exported_energy + average_annual_savings)
        potential_kwh = round(difference_consumed,2)
        print(f"In calculate_annual_savings 1st if : average_annual_savings: {average_annual_savings}, total_savings_potential{total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")
    elif annual_PV_energy_produced > annual_consumption and self_consumed_energy <= annual_consumption:
        difference_consumed = annual_PV_energy_produced - annual_consumption
        average_annual_savings = round(total_avoided_charges)
        total_savings_potential = 1
        potential_kwh = round(difference_consumed,2)
        print(f"In calculate_annual_savings 2nd if : average_annual_savings: {average_annual_savings}, total_savings_potential{total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")
    else:
        difference_consumed = annual_consumption - annual_PV_energy_produced

        average_annual_savings = round(total_avoided_charges - calculate_consumption_total_charges(difference_consumed, phase_loadkVA, energy_cost))
        total_savings_potential = average_annual_savings
        potential_kwh = 0
        print(f"In calculate_annual_savings 3rd if : average_annual_savings: {average_annual_savings}, total_savings_potential{total_savings_potential}, annual_PV_energy_produced: {annual_PV_energy_produced}, annual_consumption: {annual_consumption}")
       
    profitPercent =  min(round(average_annual_savings / consumption_total_charges * 100, 1),100) 

    return average_annual_savings, profitPercent, total_savings_potential, potential_kwh

def calculate_total_savings(average_annual_savings):
    # Calculate the total profit over 25 years
    # based on the annual savings
    # 1st year the total savings is the average_annual_savings
    total_savings_array = [0, average_annual_savings]
    total_savings = average_annual_savings
    
    for i in range(1, 25):
        total_savings += round(average_annual_savings / ( ( annual_degradation_production ) ** i))
        total_savings_array.append(total_savings)

    return total_savings, total_savings_array

def calculate_payback_period(total_investment, average_annual_savings): 
    years_to_overcome_investment = 0
    total_savings = []
    starting_invest = total_investment

    # Find the point where savings exceed investment
    while sum(total_savings) <= total_investment:
        total_savings.append( average_annual_savings / ( ( annual_degradation_production ) ** years_to_overcome_investment) )
        years_to_overcome_investment += 1
        starting_invest -= float(total_savings[-1])

    # Calculate years and months independently from that point    
    subtraction = sum(total_savings) - total_investment
    monthly_savings = total_savings [years_to_overcome_investment - 2] /12
    years = years_to_overcome_investment - 1
    months = round(12 - (subtraction/monthly_savings) )

    payback_year_float  = years + (months / 13)

    if months == 1:
        payback_period = f"{years} έτη & {months} μήνας"

    else:
        payback_period = f"{years} έτη & {months} μήνες"

    return payback_period, payback_year_float    

def calculate_total_production_kwh(annual_PV_energy_produced, shadings_percentage):
    # 1st year the total production is the annual_PV_energy_produced
    total_production_kwh = annual_PV_energy_produced
    total_production_kwh_array =[0, annual_PV_energy_produced]
    print(f"3333333333 in calculate_total_production_kwh, annual_PV_energy_produced {annual_PV_energy_produced} 333333")

    for i in range(1, 25):
        total_production_kwh += annual_PV_energy_produced / ( annual_degradation_production ** i) * shadings_percentage
        total_production_kwh_array.append(round(total_production_kwh))

    print("Total kWh production after 25 years: ", total_production_kwh)

    return total_production_kwh_array, total_production_kwh

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
    
    irr = round(npf.irr(saving_flows)* 100, 2) 

    print('Internal Rate: ', irr)
    
    return irr   
   
def calculate_CO2_emissions_reduced(annual_PV_energy_produced):
   # Calculate the equivalent CO2 emissions, reduced due to solar production
   average_CO2 = 0.04 # ~ 40 g CO2 eq/kWh for a year
   
   return average_CO2 * annual_PV_energy_produced # kg per year
  
def calculate_equivalent_trees_planted(annual_PV_energy_produced):
   percentage_trees_per_kWh = 0.02
   
   return annual_PV_energy_produced * percentage_trees_per_kWh 

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
