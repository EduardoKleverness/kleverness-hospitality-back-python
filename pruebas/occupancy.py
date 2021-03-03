import requests
import helpers
import os

# def oauth_smart_b(event, context):

accesstoken = helpers.get_token_sb()
print("token recibido: ")
print(accesstoken)
if accesstoken is not None:
    # obtiene datos del sensor
    isOccupied = False
    urlSensors = "https://api.sb.ecobee.com/api/v1/thermostats/521755031179/sensors"
    urlSendAllOnOff = "https://d008.kleverness.com/routine/launch/allonoff"
    urlHvackModeTerm = "https://api.sb.ecobee.com/api/v1/thermostats/521755031179/hvacMode"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    # 19NV00/KH19NV002538/CMD All on/off info
    # topic = os.environ['topic']
    topic = "19NV00/KH19NV002538/CMD"
    payloadAllOnOff = {
        "topic": topic
    }

    headers.setdefault("authorization", "Bearer " + accesstoken)
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
            responseAllOnOff = requests.request("POST", urlSendAllOnOff, json=payloadAllOnOff)
            if responseAllOnOff.status_code == 200:
                print("All Off sended")
            payloadHvac = {"hvacMode": "heat"}
            responseHvac = response = requests.request("PATCH", urlHvackModeTerm, json=payloadHvac, headers=headers)
            print(responseHvac.text)
            if responseHvac.status_code == 200:
                print("heat")
        else:
            payloadHvac = {"hvacMode": "cool"}
            responseHvac = requests.request("PATCH", urlHvackModeTerm, json=payloadHvac, headers=headers)
            if responseHvac.status_code == 200:
                print("cool")
    else:
        print(responseSensors.text)