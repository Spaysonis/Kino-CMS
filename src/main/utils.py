# cms/utils.py
from user_agents import parse
import geoip2.database

def get_device_type(request):
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(ua_string)

    if user_agent.is_mobile:
        return "mobile"
    elif user_agent.is_tablet:
        return "tablet"
    elif user_agent.is_pc:
        return "desktop"
    else:
        return "other"



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_country_from_ip(ip):
    try:
        reader = geoip2.database.Reader('/path/to/GeoLite2-Country.mmdb')
        response = reader.country(ip)
        return response.country.name
    except:
        return "Unknown"