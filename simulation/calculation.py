import math

def pv_net_metering(angle=30, kw=5, irradiance=700, sunlight_hours=6, price=0.12, used_kWh=100, investment=8000):

    # Calculate the monthly energy generation
    energy = kw * irradiance * math.sin(math.radians(angle)) * sunlight_hours * 30 / 1000  # kWh
    # Calculate the monthly savings
    savings = energy * price
    # Calculate the payback period
    payback = investment / savings

    # Calculate the monthly savings
    net_savings = savings - (used_kWh * price)

    # Print the results
    print(f"Monthly energy generation: {energy:.1f} kWh")
    print(f"Monthly savings: {savings:.2f} €")
    print(f"Payback period: {payback:.1f} years")


pv_net_metering()
