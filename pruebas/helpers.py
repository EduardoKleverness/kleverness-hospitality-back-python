import psycopg2


def get_token_sb():
    try:
        # obtener nuevo token en la bd
        connection = psycopg2.connect(user="kl_administrator",
                                      password="9e55MEMmhtUz",
                                      host="dev-db-kleverness.ctzqpizhk2fp.us-west-2.rds.amazonaws.com",
                                      port="47305",
                                      database="KlevernessDB")

        cursor = connection.cursor()
        query = """select token from \"SwitchUpp_Core\".oauth_sb order by id desc limit 1;"""
        # print(query)
        # Print PostgreSQL version insert into "SwitchUpp_Core".oauth_sb (token) values (ptoken) \
        cursor.execute(query)
        # connection.commit()
        record = cursor.fetchone()
        # print(record)
        for row in record:
            accesstoken = row
        if accesstoken is not None:
            return accesstoken
        else:
            return None
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

