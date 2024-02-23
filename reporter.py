

import db
from time import sleep
import os, sys
import datetime
import time
class Reporter():
    def __init__(self):
        self.last_cicle = 0
        self.last_measurement_data = []
        self.puesto = 0  # Registro del puesto actual, todas las mediciones deben pertenecer al mismo puesto
        self.database = db.Database()
        self.puesto_changed = 0
        self.hora_inicio = None
        self.minutos_inicio=None
        # self.start()

    def start(self):
        hora_actual = datetime.datetime.now().strftime("%H:%M")
        hora, minutos = hora_actual.split(":")
        hora = hora.zfill(2)
        minutos = minutos.zfill(2)
        hora_inicio = f"{hora}:{minutos}"
        self.hora_inicio = hora_inicio
        # self.minutos_inicio = time.localtime().tm_min
        self.get_last_measurement()

    def set_puesto_change(self, value):
        self.puesto_changed=value

    def get_puesto_change(self):
        return self.puesto_changed
    
    def get_puesto(self):
        return self.puesto
    
    def get_initial_time(self):
        return self.hora_inicio

    # Método que obtiene el número de ciclo correspondiente a la medición más nueva
    def get_last_measurement(self):
        result = self.database.query('SELECT nro_puesto, nro_ciclo, TIME(fecha_hora_inicio) as last_measurement FROM ciclo ORDER BY fecha_hora_inicio DESC LIMIT 1;')
        if result:
            self.puesto = result[0]['nro_puesto']
            self.last_cicle = result[0]['nro_ciclo']
            # print("Puesto:",self.puesto)
            # print("Last cicle:",self.last_cicle)
            
    def get_last_puesto(self):
        result = self.database.query('SELECT nro_puesto, nro_ciclo, TIME(fecha_hora_inicio) as last_measurement FROM ciclo ORDER BY fecha_hora_inicio DESC LIMIT 1;')
        if result:
            last_puesto = result[0]['nro_puesto']
        return last_puesto
    

    # Método que obtiene las mediciones nuevas de la base
    def get_new_measurements(self):
        
        if(self.get_last_puesto()!=self.puesto):
            self.set_puesto_change(value=1)
            print("Cambio el puesto, realizando calculos estadísticos...\n")
            return None, None

        cicle = self.database.query('SELECT nro_ciclo FROM ciclo WHERE nro_puesto = {} ORDER BY fecha_hora_inicio DESC LIMIT 1;'.format(self.puesto))

        if cicle and cicle[0]['nro_ciclo'] > self.last_cicle:
            query = 'SELECT nro_medicion, valor FROM mediciones_ciclo WHERE nro_ciclo = {} AND nro_puesto = {};'.format(self.last_cicle, self.puesto)
            self.last_measurement_data.clear()
            self.last_measurement_data = self.database.query(query)
            self.last_cicle = cicle[0]['nro_ciclo']
            return self.last_measurement_data, self.last_cicle

        return None, None
    
    def reset_reporter(self):
        self.set_puesto_change(value=0)
        self.hora_inicio=None
        # self.start()







        


                
