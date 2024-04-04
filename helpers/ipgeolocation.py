from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance

from requests import get

def getCoords():
    ip = get('https://api.ipify.org').content.decode('utf8')
    res = DbIpCity.get(ip, api_key="free")
    return res

