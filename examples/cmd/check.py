# test_capitalize.py

from permguard_sdk.az_client import AZClient
from permguard_sdk.az_config import with_endpoint
#from permguard_sdk.az.azreq import AZRequest

az_client = AZClient(with_endpoint("localhost", 9094))
