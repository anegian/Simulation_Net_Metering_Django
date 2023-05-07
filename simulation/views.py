
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

def dashboardResults(request):   # simulation/templates/dashboard.html
    try:
        district_key = int(request.session.get('district_key', 'N/A'))
        district_value = request.session.get('district_value', 'N/A')
        placeOfInstallment = request.session.get('placeOfInstallment', 'N/A')
        inclinationPV = request.session.get('inclinationPV', 'N/A')
        azimuthValue = request.session.get('azimuthValue', 'N/A')
        userPowerProfile = request.session.get('userPowerProfile', 'N/A')
        phaseLoad = request.session.get('phaseLoad', 'N/A')
        phaseLoadkVA = request.session.get('phaseLoadkVA', 'N/A')
        recommendedPVinKwp = request.session.get('recommendedPVinKwp', 'N/A')
        annualKwh = int(request.session.get('annualKwh', 'N/A'))
        PV_kWp = int(request.session.get('PV_kWp', 'N/A'))
        averageAnnualProduction = district_key * PV_kWp
        hasStorage = request.session.get('hasStorage', 'N/A')
        storage_kW = int(request.session.get('storage_kW', 'N/A'))
        batteryCost = storage_kW * 700

           
        totalInvestment = calculateTotalInvestment(PV_kWp, batteryCost)
        averageAnnualSavings, profitPercent, totalAnnualCost, otherEnergyCharges = calculateAnnualSavings(annualKwh, phaseLoadkVA, batteryCost, userPowerProfile, averageAnnualProduction)
        payBackPeriod = calculatePayBackPeriod(totalInvestment, averageAnnualSavings)

        # dictionary with rendered variables
        context = {
        'district_key': district_key,
        'district_value': district_value,
        'placeOfInstallment': placeOfInstallment,
        'azimuthValue': azimuthValue,
        'inclinationPV': inclinationPV,
        'userPowerProfile': userPowerProfile,
        'phaseLoad': phaseLoad,
        'phaseLoadkVA': phaseLoadkVA,
        'recommendedPVinKwp': recommendedPVinKwp,
        'annualKwh': annualKwh,
        'PV_kWp': PV_kWp,
        'hasStorage': hasStorage,
        'storage_kW': storage_kW,
        'totalInvestment': totalInvestment,
        'payBackPeriod': payBackPeriod,
        'averageAnnualSavings': averageAnnualSavings,
        'profitPercent': profitPercent,
        'totalAnnualCost': totalAnnualCost,
        'otherEnergyCharges': otherEnergyCharges,
        }

        result = 'simulation/dashboard.html'
        print('Total Investment:', totalInvestment,"euro", '& Περίοδος Απόσβεσης:', payBackPeriod, "Ετήσιο κόστος ρεύματος: ", totalAnnualCost, "& ετήσια μείωση: ", averageAnnualSavings, "Ρυθμιζόμενες χρεώσεις: ", otherEnergyCharges, )  # Add this line for debugging
        return render(request, result, context)

    except Http404:
        return Http404("404 Generic Error")
    
def calculatorFormsOptions(request):    # simulation/templates/calculator.html

    if request.method == 'POST':
        # changes the name of variable to calculator_form because form was fault --> shadow name 'form' out of scope
        formDistrict = PlaceOfInstallationForm(request.POST)
        formAnnualKwh = EnergyConsumptionForm(request.POST)
        formPhaseLoad = PhaseLoad(request.POST)
        
        
        if formDistrict.is_valid() and formAnnualKwh.is_valid() and formPhaseLoad.is_valid():
            try:
                # initialization of variables
                district_key = request.POST.get('select_district')
                district_value = dict(PlaceOfInstallationForm.DISTRICT_CHOICES).get(district_key)
                placeOfInstallment = request.POST.get('installation')
                azimuthValue = request.POST.get('azimuth')
                inclinationPV = request.POST.get('inclination')
                userPowerProfile = request.POST.get('power_option')

                phaseLoad = request.POST.get('select_phase')

                if phaseLoad == "single_phase":
                    phaseLoadkVA = 8
                else:
                    phaseLoadkVA = 25

                recommendedPVinKwp = request.POST.get('select_kwh')
                # get the value of the energy consumption dict, where key is the kWh selected
                annualKwh = dict(EnergyConsumptionForm.KWh_CHOICES).get(recommendedPVinKwp) 
                
                PV_kWp = request.POST.get('myRangeSlider')
                hasStorage = request.POST.get('storage')
                storage_kW = request.POST.get('storage_kw')

                # print the variables to check
                print(f"District key: {district_key}")
                print(f"District value: {district_value}")
                print(f"The selected phase load is: {phaseLoad}")
                print(f"Agreed kVA is: {phaseLoadkVA}")
                print(f"AnnualKwh is: {annualKwh}")
                print(f"Recommended Kwp is: {recommendedPVinKwp}" )
                print(f"Place of installment is: {placeOfInstallment}")
                print(f"Azimuth of PV: {azimuthValue}")
                print(f"Degrees of PV inclination: {inclinationPV}" )
                print(f"Users prefer to use: {userPowerProfile}" )
                print(f"kWp of PV value: {PV_kWp}")
                print(f"Did User select Battery storage: {hasStorage}")

                if hasStorage == 'with_storage':
                    print(f"Battery kWh value: {storage_kW}")
                else:
                    storage_kW = 0
                    print('No storage selected')
            except KeyError:
                # Handle the case where an invalid key is provided
                return HttpResponse('Invalid request parameters')

            request.session['district_key'] = district_key
            request.session['district_value'] = district_value
            request.session['placeOfInstallment'] = placeOfInstallment
            request.session['inclinationPV'] = inclinationPV
            request.session['userPowerProfile'] = userPowerProfile
            request.session['recommendedPVinKwp'] = recommendedPVinKwp
            request.session['annualKwh'] = annualKwh
            request.session['PV_kWp'] = PV_kWp
            request.session['hasStorage'] = hasStorage
            request.session['storage_kW'] = storage_kW
            request.session['phaseLoadkVA'] = phaseLoadkVA

        return redirect(reverse('simulation:dashboard'))  # redirect to function calculator

    else:
        formDistrict = PlaceOfInstallationForm()
        formAnnualKwh = EnergyConsumptionForm()
        formPhaseLoad = PhaseLoad()
    return render(request, 'simulation/calculator.html', context={'formDistrict': formDistrict, 
         'formAnnualKwh': formAnnualKwh,'formPhaseLoad': formPhaseLoad,})


# Calculation functions

# Calculate total investment
def calculateTotalInvestment(PV_kWp, batteryCost):
    PvCost = PV_kWp * 1500
    installationCost = 400
    
    return PvCost + installationCost + batteryCost

# Calculate annual savings and percentage
def calculateAnnualSavings(annualKwh, phaseLoadkVA, batteryCost, userPowerProfile, averageAnnualProduction):
    annualConsumption = annualKwh
    energyCost = 0.19 # €/kWh today
    annualkWhCost = annualConsumption * energyCost
    # Ρυθμιζόμενες Χρεώσεις
    otherEnergyCharges = (phaseLoadkVA * 0.52) + (annualKwh * 0.0213) + (phaseLoadkVA * 1) + (annualKwh * 0.00844) + (annualKwh*0.017) + (annualKwh*energyCost*0.06)
    totalAnnualCost = annualkWhCost + otherEnergyCharges

    # cases with battery storage and use profile to calculate self-consumption rate
    if batteryCost == 0 and userPowerProfile == "day-power":
        selfConsumptionRate = 0.75
    elif batteryCost > 0 and userPowerProfile == "day-power":
        selfConsumptionRate = 0.9
    elif batteryCost == 0 and userPowerProfile == "night-power":
        selfConsumptionRate = 0.5
    elif batteryCost > 0 and userPowerProfile == "night-power":
        selfConsumptionRate = 0.7
    else:
        selfConsumptionRate = 0.5

    # Μειωμένο Ποσό Ρυθμιζόμενων Χρεώσεων
    discountOtherEnergyCharges = otherEnergyCharges * selfConsumptionRate
    
    if averageAnnualProduction >= annualKwh:
        averageAnnualSavings = round( annualkWhCost + discountOtherEnergyCharges )
    else:
        averageAnnualSavings = round( ( (annualkWhCost - (annualConsumption - averageAnnualProduction ) * energyCost) )  + discountOtherEnergyCharges)

    profitPercent =  round(averageAnnualSavings / totalAnnualCost * 100, 1)

    return averageAnnualSavings, profitPercent, totalAnnualCost, otherEnergyCharges

# Payback Period
def calculatePayBackPeriod(totalInvestment, averageAnnualSavings):    
    payBackPeriod = totalInvestment / averageAnnualSavings
    years = int(payBackPeriod)
    months = round((payBackPeriod - years) * 12)

    return f"{years} έτη & {months} μήνες"


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

    # lifetimePv = 25
    # discountRate = 0.05
    # annualreservationCost = 400 * 12
    # lcoe = ( totalInvestment + (annualreservationCost * lifetimePv) ) / discountRate
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


