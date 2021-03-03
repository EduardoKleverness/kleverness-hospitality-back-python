import requests
import helpers

token = helpers.get_token_sb()
print("token obtenido")
print(token)
if token is not None:
    headers = {
        "authorization": "Bearer "+token
    }
    urlTermstatus = "https://api.sb.ecobee.com/api/v1/thermostats/521755031179/status"
    responseSensors = requests.request("GET", urlTermstatus, headers=headers)
    print(responseSensors.json())
