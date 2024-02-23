import numpy as np
import view
import math
import threading

# Clase donde se encuentran los metodos encargados de crear, mantener y actualizar las estructuras de datos
# se tienen dos grupos de mediciones, unas de derecha y otra de izquierda.
# En la inicializacion de la clase Data se crean todos los campos necesarios para interactuar con los datos
class Data():

    def __init__(self):

        
        self.data_acumulator = None # acumula todo lo que llega de la db
        self.deflexiones_acumulator = [] # acumula los valores de las deflexiones
        self.group_counter = 1 # Contador de grupos
        self.grupos=None        #Grupos seleccionados por el usuario

        # Contienen los datos del grupo actual
        self.defl_r = []
        self.defl_l = []
        self.radio_r = []
        self.radio_l = []

        # Contienen las deflexiones maximas
        self.defl_l_max = [] 
        self.defl_r_max = []

        # Contienen las desviaciones estandar
        self.defl_l_car = []
        self.defl_r_car = []

        # Unicamente para el ploteo de deflexiones individuales
        self.defl_bar_l = []
        self.defl_bar_r = []

        
        # Acumuladores que contienen todos los datos recolectados durante la ejecucion
        self.defl_r_acum = []
        self.defl_l_acum = []
        self.radio_r_acum = []
        self.radio_l_acum = []
        self.indices = []

        # Variables para el calculo de compensacion

        self.temp = None 
        self.espesor = None
        self.ft= None
        self.fh=None
        self.fc=None
        self.z = None

        # dict individual para el histograma de mediciones
        self.hist_dict = {
            "index":[],
            "defl": []
        }

        # dict que va a contener los datos que se van a mostrar por tabla
        # tambien se usan en los ploteos
        self.data_dict_r = {
            "Grupo":[],
            "Radio":[],
            "Defl.":[],
            "R*D":[],
            "D/R":[],
        } 

        self.data_dict_l = {
            "Grupo":[],
            "Radio":[],
            "Defl.":[],
            "R*D":[],
            "D/R":[],
        } 

    # Metodo toma lo que devuelve la base de datos y coloca las deflexiones y sus indices en un diccionario.
    def data_destruct(self,data):

        # print("Muestras:",muestras)
        # print("Temp:",self.temp)
        # print("Espesor:",self.espesor)   

        defl_r_aux=data[0]['valor']
        radio_r_aux=data[1]['valor']
        defl_l_aux=data[2]['valor']
        radio_l_aux=data[3]['valor']

        print("Deflexion derecha:",defl_r_aux)
        print("Deflexion izquierda:",defl_l_aux)
        print("Radio derecha:",radio_r_aux)
        print("Radio Izquierda:",radio_l_aux)
        print("\n")

        defl_r_aux,defl_l_aux,radio_r_aux,radio_l_aux = self.compensate(defl_r_aux, defl_l_aux,radio_r_aux,radio_l_aux)


        self.defl_r.append(defl_r_aux)
        self.defl_l.append(defl_l_aux)
        self.radio_r.append(radio_r_aux)
        self.radio_l.append(radio_l_aux)

        self.defl_r_acum.append(defl_r_aux)
        self.radio_r_acum.append(radio_r_aux)
        self.defl_l_acum.append(defl_l_aux)
        self.radio_l_acum.append(radio_l_aux)
       
    # Metodo que se encarga de una vez cumplido el grupo, actualizar los datos para el grafico de barras
    def update_bar_data(self,amount):
        self.defl_bar_r.extend(self.defl_r[-amount:])
        self.defl_bar_l.extend(self.defl_l[-amount:])
        return self.defl_bar_r,self.defl_bar_l

    def clear_bar_data(self):
        self.defl_bar_r.clear()
        self.defl_bar_l.clear()

    def update_structures(self):
        # Obtengo los promedios de cada cosa
       
        media_defl_r = round(np.mean(self.defl_r),2)
        media_defl_l = round(np.mean(self.defl_l),2)
        media_radio_r = round(np.mean(self.radio_r),2)
        media_radio_l = round(np.mean(self.radio_l),2)

       

        # Obtengo la deflexion caracteristica. Por el momento Z es igual a 2 y el resto (ft, fc, fh) es 1
        self.defl_l_car.append(  (media_defl_l + ((np.std(self.defl_l)*self.z)))*self.ft*self.fh*self.fc  )
        self.defl_r_car.append(  (media_defl_r + ((np.std(self.defl_r)*self.z)))*self.ft*self.fh*self.fc  )
        
        # Obtengo los máximos de las deflexiones
        self.defl_l_max.append(np.max(self.defl_l))
        self.defl_r_max.append(np.max(self.defl_r))
        

        # Los agrego a los diccionarios correspondientes
        self.data_dict_r['Grupo'].append(self.group_counter*self.get_grupos())
        self.data_dict_r['Radio'].append(media_radio_r)
        self.data_dict_r['Defl.'].append(media_defl_r)
        self.data_dict_r['R*D'].append(round(media_defl_r * media_radio_r,2))
        self.data_dict_r['D/R'].append(round(media_defl_r / media_radio_r,2))
        
        self.data_dict_l['Grupo'].append(self.group_counter*self.get_grupos())
        self.data_dict_l['Radio'].append(media_radio_l)
        self.data_dict_l['Defl.'].append(media_defl_l)
        self.data_dict_l['R*D'].append(round(media_defl_l * media_radio_l,2))
        self.data_dict_l['D/R'].append(round(media_defl_l / media_radio_l,2))
        
        self.group_counter += 1

         # limpiamos porque ya se cumplio el grupo
        self.defl_r.clear()
        self.defl_l.clear()
        self.radio_r.clear()
        self.radio_l.clear()

    
    # # Metodo que devuelve los datos compensados con respecto a la temperatura ingresada
    def compensate(self,defl_r_aux, defl_l_aux,radio_r_aux,radio_l_aux):

        defl_r_aux=round((defl_r_aux/((0.001*self.espesor*(self.temp-20))+1)),2)
        defl_l_aux=round((defl_l_aux/((0.001*self.espesor*(self.temp-20))+1)),2) 
        radio_r_aux=round((radio_r_aux*((0.001*self.espesor*(self.temp-20))+1)),2)
        radio_l_aux=round((radio_l_aux*((0.001*self.espesor*(self.temp-20))+1)),2)
        
        return defl_r_aux,defl_l_aux,radio_r_aux,radio_l_aux
       
    def calculate_stats(self): # TODO-> Consultar por el calculo de Radio Caracteristico. Falta ese cálculo

        print("Generando Calculos Estadísticos...")
        if(self.defl_r_acum==[] or self.defl_l_acum==[] or self.radio_r_acum==[] or self.radio_l_acum==[]):
            print("Detecto que alguno es None")
            media_defl_der=0
            media_defl_izq=0
            media_rad_der=0
            media_rad_izq=0
            desv_defl_der=0
            desv_defl_l=0
            coef_var_der=0
            coef_var_izq=0
            defl_car_der=0
            defl_car_izq=0
            rad_car_der=0
            rad_car_izq=0
            d_r_der=0
            d_r_izq=0
            d_x_r_der=0
            d_x_r_izq=0
            total_mediciones_defl=0
            total_mediciones_rad=0
            return media_defl_der,media_defl_izq,media_rad_der,media_rad_izq,desv_defl_der,desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq,d_r_der,d_r_izq,d_x_r_der,d_x_r_izq,total_mediciones_defl,total_mediciones_rad
       
        # Calculo de medias para mediciones totales de cada cosa
        media_defl_der = round(np.mean(self.defl_r_acum),2)
        media_defl_izq = round(np.mean(self.defl_l_acum),2)
        media_rad_der =  round(np.mean(self.radio_r_acum),2)
        media_rad_izq = round(np.mean(self.defl_l_acum),2)
        
        # # Calculo de desviaciones estandar deflexiones
        desv_defl_der = round(np.std(self.defl_r_acum),2)
        desv_defl_l = round(np.std(self.defl_l_acum),2)

        # # Calculo de coeficientes de variacion deflexiones
        coef_var_der = round((desv_defl_der/media_defl_der)*100,2)
        coef_var_izq = round((desv_defl_l/media_defl_izq)*100,2)

        # # Calculo de deflexion caracteristicas
        defl_car_der = round((media_defl_der + (desv_defl_der*self.z))*self.ft*self.fh*self.fc,2)
        defl_car_izq = round((media_defl_izq + (desv_defl_l*self.z))*self.ft*self.fh*self.fc,2)

        # Calculo de radio caracteristico
        rad_car_der = round((media_rad_der + ((np.std(self.radio_r_acum)))*self.z)*self.ft*self.fh*self.fc,2)
        rad_car_izq = round((media_rad_izq + ((np.std(self.radio_l_acum)))*self.z)*self.ft*self.fh*self.fc,2)

        # # Calculo de D/R medio
        d_r_der = round(media_defl_der/media_rad_der,2)
        d_r_izq = round(media_defl_izq/media_rad_izq,2)

        # # Calculo de D*R medio
        d_x_r_der = round(media_defl_der*media_rad_der,2)
        d_x_r_izq = round(media_defl_izq*media_rad_izq,2)

        # # Calculo de total de mediciones
        total_mediciones_defl = len(self.defl_l_acum)
        total_mediciones_rad = len(self.radio_l_acum)
        # print("Defl l acum:",len(self.defl_l_acum))
        # print("Radio l acum:",len(self.radio_l_acum))

        return media_defl_der,media_defl_izq,media_rad_der,media_rad_izq,desv_defl_der,desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq,d_r_der,d_r_izq,d_x_r_der,d_x_r_izq,total_mediciones_defl,total_mediciones_rad


    def get_data_dict(self):
        return self.data_dict_r, self.data_dict_l
    
    def get_max_defl(self):
        return self.defl_l_max, self.defl_r_max
    
    def get_car_defl(self):
        return self.defl_l_car, self.defl_r_car
    
    def get_hist_dict(self):
        return self.hist_dict

    def cant_mediciones(self):
        return len(self.defl_r)
    
    def get_indexes(self):
        # self.indices = list(range(1,len(self.defl_bar_r)+1))
        return self.indices
        # return self.hist_dict['index']

    def get_defl_bar(self):
        return  self.defl_bar_r, self.defl_bar_l
               

    # Estas dos funciones se pueden usar para pasar los valores para el grafico de barras
    def get_defl(self):
        return {
                "right": self.defl_r_acum,
                "left": self.defl_l_acum
               }
    
    def set_espesor(self,espesor):
        print("Espesor:",espesor)
        self.espesor=espesor

    def set_temp(self,temp):
        print("Temp:",temp)
        self.temp=temp
        
    def set_ft(self,ft):
        print("Ft:",ft)
        self.ft=ft

    def set_fc(self,fc):
        print("Fc",fc)
        self.fc=fc
        
    def set_fh(self,fh):
        print("Fh:",fh)
        self.fh=fh

    def set_z(self,z):
        print("Z:",z)
        self.z=z

    def set_grupos(self,grupos):
        self.grupos=grupos

    def get_grupos(self):
        return self.grupos
        
    def reset_all(self):
        self.defl_r.clear()
        self.defl_l.clear()
        self.radio_r.clear()
        self.radio_l.clear()
        self.defl_l_max.clear()
        self.defl_r_max.clear()
        self.defl_r_car.clear()
        self.defl_l_car.clear()
        self.defl_l_acum.clear()
        self.defl_r_acum.clear()
        self.radio_l_acum.clear()
        self.radio_r_acum.clear()
        self.indices.clear()
        self.defl_bar_l.clear()
        self.defl_bar_r.clear()
        self.hist_dict.clear()
        self.group_counter = 1
        self.data_dict_r = {
            "Grupo":[],
            "Radio":[],
            "Defl.":[],
            "R*D":[],
            "D/R":[],
        } 
        self.data_dict_l = {
            "Grupo":[],
            "Radio":[],
            "Defl.":[],
            "R*D":[],
            "D/R":[],
        }
         
        print("Datos reseteados!\n")
        
