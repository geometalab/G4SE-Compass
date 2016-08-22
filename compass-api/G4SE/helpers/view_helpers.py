from netaddr import IPNetwork, IPAddress
from django.conf import settings


# Check if connection comes from internal IP range
def is_internal(client_ip):
    for ip_range in settings.INTERNAL_IP_RANGES:
        if IPAddress(client_ip) in IPNetwork(ip_range):
            return True
    return False
