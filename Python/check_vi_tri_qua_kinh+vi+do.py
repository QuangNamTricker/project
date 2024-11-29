from geopy.geocoders import Nominatim

def get_location(latitude, longitude):
    geolocator = Nominatim(user_agent="geo_tool")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.address
    else:
        return "Không tìm thấy vị trí."

if __name__ == "__main__":
    lat = float(input("Nhập vĩ độ: "))
    lon = float(input("Nhập kinh độ: "))
    address = get_location(lat, lon)
    print("Vị trí:", address)
