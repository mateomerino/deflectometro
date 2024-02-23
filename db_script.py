import mysql.connector
from mysql.connector import errorcode 
import json
import random
from time import sleep

# script que inserta mediciones en la base de datos cada x tiempo (para cambiar el intervalo modificar el número de sleep())

if __name__ == "__main__":
    config_file = open('config.json', 'r')
    config = json.load(config_file)

    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Bad name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
    if conn is not None:
        cursor = conn.cursor(buffered=True, dictionary=True)

        cursor.execute('SELECT nro_puesto, nro_ciclo FROM ciclo ORDER BY fecha_hora_inicio DESC LIMIT 1;')
        print("Cursor:\n")
        print(cursor)
        conn.commit()

        # Resultado 
        result = cursor.fetchone()
        print("Result:", result)
        # print("nro_puesto",result[0]['nro_puesto'])
        # print("nro_ciclo",result[0]['nro_ciclo'])

        nro_ciclo = result['nro_ciclo'] + 1
        print("nro_ciclo:", nro_ciclo)
        nro_puesto = result['nro_puesto']
        print("nro_puesto:", nro_puesto)

        for i in range(0, 25):
            print("Insertando datos en la base de datos con puesto:", nro_puesto)
            cursor.execute('INSERT INTO ciclo VALUES(%(nro_puesto)s,%(nro_ciclo)s,800,NOW(),NOW(),200,200,"1","TARDE",1,"1","1")', {'nro_puesto' : nro_puesto, 'nro_ciclo':nro_ciclo})
            print("Inserte el nro de ciclo:", nro_ciclo)
            print("Inserción nro:", i)
            counter = 1
            for n in range(1, 5):
                ran = round(random.uniform(40, 55), 4)
                cursor.execute('INSERT INTO mediciones_ciclo VALUES(%s,%s,%s,%s)', (nro_puesto, nro_ciclo, counter, ran))
                print("Inserte el dato:", ran)
                counter += 1
            nro_ciclo += 1
            sleep(1.3)
            conn.commit()

        cursor.close()
        conn.close()
    else:
        print("No se pudo establecer una conexión a la base de datos. Verifica la configuración y los permisos de acceso.")

    # nro_ciclo=1
    # nro_puesto=nro_puesto+1

    # for i in range (0,2):
    #     print("Insertando datos en la base de datos con puesto:",nro_puesto)
    #     cursor.execute('INSERT INTO ciclo VALUES(%(nro_puesto)s,%(nro_ciclo)s,800,NOW(),NOW(),200,200,"1","TARDE",1,"1","1")',{'nro_puesto' : nro_puesto,'nro_ciclo':nro_ciclo})
    #     print("Inserte el nro de ciclo:",nro_ciclo)
    #     print("Insercion nro:",i)
    #     counter = 1
    #     for n in range(1,5):
    #         ran = round(random.uniform(40,55),4)
    #         cursor.execute('INSERT INTO mediciones_ciclo VALUES(%s,%s,%s,%s)',(nro_puesto,nro_ciclo,counter,ran))
    #         print("Inserte el dato:",ran)
    #         counter += 1
    #     nro_ciclo += 1
    #     sleep(1)
    #     conn.commit()

   