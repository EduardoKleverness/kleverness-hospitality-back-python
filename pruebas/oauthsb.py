import psycopg2
import requests

try:
    urlAuth = "https://api.sb.ecobee.com/token"

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

    # Obtener nuevo token
    response = requests.request("POST", urlAuth, json=payload, headers=headers)

    if response.status_code == 200:
        responseJson = response.json()
        print("access_token")
        print(responseJson["access_token"])
        accessToken = responseJson["access_token"]

        # insertar nuevo token en la bd
        connection = psycopg2.connect(user="rIEwoRTE",
                                      password="UsKTMS&Jj25^",
                                      host="kleverhospitality.cvei5icxuveh.us-east-1.rds.amazonaws.com",
                                      port="6345",
                                      database="kleverhospitality")

        cursor = connection.cursor()
        query = """select * from \"public\".update_sb_token(%s)"""
        valuesQuery = (accessToken,)
        print(query)
        # Print PostgreSQL version insert into "SwitchUpp_Core".oauth_sb (token) values (ptoken) \
        cursor.execute(query, valuesQuery)
        connection.commit()
        record = cursor.fetchone()
        print(record)

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
