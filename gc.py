from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from model import Company, Address, Product, Facility
from server import app
import math

app.app_context().push()

locator = Nominatim(user_agent="thanks")
geocode = RateLimiter(locator.geocode, min_delay_seconds=5)
location = None

facilities = Facility.query.all()
with open("./data/locations.csv", "w") as file:
    file.write('"nickname","latitude","longitude"\n')
    for facility in facilities:
        address = facility.address
        addr_str = ""
        if address.address_1:
            addr_str += f"{address.address_1}"

        if address.address_2:
            addr_str += f" {address.address_2}"

        if address.suite:
            addr_str += f" {address.suite}"

        if address.postal:
            postal = math.floor(float(address.postal))
        else:
            postal = ""

        if address.city:
            addr_str += f" {address.city}"
                
        if address.state:
            addr_str += f" {address.state} {postal}"

        location = geocode(addr_str)

        print(addr_str)
        if location and hasattr(location,"latitude"):
            data = f'"{facility.nickname}",{location.latitude},{location.longitude}\n'
            file.write(data)
            file.flush()

