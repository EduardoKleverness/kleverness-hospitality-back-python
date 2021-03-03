import requests
import os


def lambda_handler(event, context):
    urlAuth = "https://api.sb.ecobee.com/token"
    urlSensors = "https://api.sb.ecobee.com/api/v1/thermostats/521755031179/sensors"
    urlSendAllOnOff = "https://d008.kleverness.com/routine/launch/allonoff"

    payload = {
        "audience": "https://api.sb.ecobee.com",
        "client_id": "46uaepWROkJZTen8tSXxb19EecVoWNiP",
        "client_secret": "bCl2Zx3C1xSBrpl0GnvCV3pSXGg5cA2JbOXukqDqkVphzwUMpvzXbZ860yRsKH8N",
        "grant_type": "client_credentials"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    isOccupied = False

    # Ecobee AUTH
    response = requests.request("POST", urlAuth, json=payload, headers=headers)

    if response.status_code == 200:
        responseJson = response.json()
        print(responseJson["access_token"])
        accessToken = responseJson["access_token"]

        # obtiene datos del sensor
        headers.setdefault("authorization", "Bearer " + accessToken)
        responseSensors = requests.request("GET", urlSensors, headers=headers)
        if responseSensors.status_code == 200:
            print(responseSensors.json())
            responseSensorsJson = responseSensors.json()
            print(len(responseSensorsJson["data"]["items"]))
            for item in responseSensorsJson["data"]["items"]:
                print(item["name"])

                # obtiene la ocupación
                for capability in item["capability"]:
                    if capability["type"] == "occupancy":
                        print("capability data")
                        print(capability["type"])
                        print(capability["value"])

                        # si alguno esta ocupado se habilita una bandera
                        if capability["value"] == "true":
                            isOccupied = True

            # si la bandera esta habilitada no se envia el all off
            if isOccupied is False:
                # 19NV00/KH19NV002538/CMD
                topic = os.environ['topic']
                payloadAllOnOff = {
                    "topic": topic,
                }
                responseAllOnOff = requests.request("POST", urlSendAllOnOff, json=payloadAllOnOff)
                if responseAllOnOff.status_code == 200:
                    print("All On/Off sended")
