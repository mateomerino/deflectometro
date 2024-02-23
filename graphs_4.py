from tkinter import *
import tkinter as tk
from tkinter.ttk import Label, Frame, Button, Scrollbar, Treeview
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import FigureCanvasPdf
import io
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
import os


# Clase donde se inicializan y actualizan los graficos

class Graphs4():
    def __init__(self, frame):
        self.frame = frame
        self.figure_defl_mean_r = None
        self.defl_mean_r = None
        self.defl_mean_widget_l = None
        self.figure_defl_mean_l = None 
        self.defl_mean_l = None 
        self.defl_mean_widget_l = None
        self.rad_mean_l_data=[]
        self.rad_mean_r_data=[]
        self.defl_mean_l_data=[]
        self.defl_mean_r_data=[]
        self.indexes=[] 

        self.show()

    def show(self):
        self.show_defl_radios_graph()
    
    def deflexiones_radios_graph(self,row, column,title):
        
        figure = Figure(figsize=(7,7), dpi=100,facecolor='#F6F4F2')
        figure.subplots_adjust(bottom=0,top=0.9)
        sub_figure=figure.add_subplot(211)
        sub_figure.set_title(title)
        sub_figure.set_xlim(0,20)
        sub_figure.set_ylim(0,100)
        sub_figure.set_xlabel("Radio")
        sub_figure.set_ylabel("Defl.")
        sub_figure.bar([], [], width = 3, linewidth=0)
        sub_figure.grid(axis='both',linestyle='dotted')

        bar = FigureCanvasTkAgg(figure,self.frame)
        bar_widget = bar.get_tk_widget()
        bar_widget.grid(row = row, column = column)
        return figure, bar, bar_widget
    
    def update_deflexiones_radios_graph(self, dict_r, dict_l,grupos):

        self.rad_mean_r_data.extend(dict_r['Radio'][-1:])
        self.rad_mean_l_data.extend(dict_l['Radio'][-1:])
        self.defl_mean_r_data.extend(dict_r['Defl.'][-1:])
        self.defl_mean_l_data.extend(dict_l['Defl.'][-1:])
        
       

        # self.indexes=list(range(1,len(self.rad_mean_l_data)+1))
        self.indexes = [x * grupos for x in range(1, len(self.rad_mean_l_data)+1)]

        # Agregar cálculos para las leyendas
        # promedio_x_izq = sum(self.defl_mean_l_data) / len(self.defl_mean_l_data)
        promedio_x_izq = sum(self.rad_mean_l_data) / len(self.rad_mean_l_data)
        promedio_producto_izq = sum(x * y for x, y in zip(self.defl_mean_l_data, self.rad_mean_l_data)) / len(self.rad_mean_l_data)
        promedio_division_izq = sum(x / y for x, y in zip(self.defl_mean_l_data, self.rad_mean_l_data)) / len(self.rad_mean_l_data)

        # promedio_x_der = sum(self.defl_mean_r_data) / len(self.defl_mean_r_data)
        promedio_x_der = sum(self.rad_mean_r_data) / len(self.rad_mean_r_data)
        promedio_producto_der = sum(x * y for x, y in zip(self.defl_mean_r_data, self.rad_mean_r_data)) / len(self.rad_mean_r_data)
        promedio_division_der = sum(x / y for x, y in zip(self.defl_mean_r_data, self.rad_mean_r_data)) / len(self.rad_mean_r_data)

        self.figure_defl_mean_l.clear()
        self.figure_defl_mean_r.clear()
        
        subfigure_izq=self.figure_defl_mean_l.add_subplot(211)
        subfigure_der=self.figure_defl_mean_r.add_subplot(211)
        print("Voy a graficar en izquierdo:",self.rad_mean_l_data)
        print("Indices:",self.indexes)
        subfigure_der.set_xlim(min(self.rad_mean_r_data)-50, max(self.rad_mean_r_data)+50)
        subfigure_izq.set_xlim(min(self.rad_mean_l_data)-50, max(self.rad_mean_l_data)+50)
        subfigure_der.set_ylim(0,max(self.rad_mean_r_data)+500)  
        subfigure_izq.set_ylim(0,max(self.rad_mean_l_data)+500)  

        # subfigure_izq.scatter(self.defl_mean_l_data,self.rad_mean_l_data, color = 'r')
        subfigure_izq.scatter(self.rad_mean_l_data, self.defl_mean_l_data, color = 'r')
        # subfigure_der.scatter(self.defl_mean_r_data, self.rad_mean_r_data, color = 'r')
        subfigure_der.scatter(self.rad_mean_r_data, self.defl_mean_r_data, color = 'r')


        # # Agregar anotaciones con la información de los cálculos
        # subfigure_izq.annotate(
        #     f'R med.: {promedio_x_izq:.2f}\n'
        #     f'RxD m: {promedio_producto_izq:.2f}\n'
        #     f'D/R m: {promedio_division_izq:.2f}',
        #     xy=(0.05, 0.95), xycoords='axes fraction',
        #     fontsize=10, ha='left', va='top')

        # subfigure_der.annotate(
        #     f'R med.: {promedio_x_der:.2f}\n'
        #     f'RxD m: {promedio_producto_der:.2f}\n'
        #     f'D/R m: {promedio_division_der:.2f}',
        #     xy=(0.05, 0.95), xycoords='axes fraction',
        #     fontsize=10, ha='left', va='top')

        subfigure_izq.annotate(
            f'R med.: {promedio_x_izq:.2f}\n'
            f'RxD m: {promedio_producto_izq:.2f}\n'
            f'D/R m: {promedio_division_izq:.2f}',
            xy=(0, 0), xycoords='axes fraction',
            xytext=(240, -45), textcoords='offset points',
            fontsize=10, ha='right', va='top',
            annotation_clip=False,
            bbox=dict(boxstyle='round,pad=0.5', edgecolor='blue', facecolor='white'))

        subfigure_der.annotate(
            f'R med.: {promedio_x_der:.2f}\n'
            f'RxD m: {promedio_producto_der:.2f}\n'
            f'D/R m: {promedio_division_der:.2f}',
            xy=(0, 0), xycoords='axes fraction',
            xytext=(240, -45), textcoords='offset points',
            annotation_clip=False,
            fontsize=10, ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.5', edgecolor='blue', facecolor='white'))


        subfigure_izq.grid(axis='both',linestyle='dotted')
        subfigure_der.grid(axis='both',linestyle='dotted')

        subfigure_izq.set_xlabel("Radio")
        subfigure_izq.set_ylabel("Defl")
        subfigure_der.set_xlabel("Radio")
        subfigure_der.set_ylabel("Defl")

        subfigure_izq.set_title("Informe estadistico: Lado Izquierdo")
        subfigure_der.set_title("Informe estadistico: Lado Derecho")

        self.figure_defl_mean_l.canvas.draw_idle()
        self.figure_defl_mean_r.canvas.draw_idle()
    

    def show_defl_radios_graph(self):
        self.figure_defl_mean_r, self.defl_mean_r, self.defl_mean_widget_r = self.deflexiones_radios_graph(0,0,"Informe estadistico: Lado Izquierdo")
        self.figure_defl_mean_l, self.defl_mean_l, self.defl_mean_widget_l = self.deflexiones_radios_graph(0,1,"Informe estadístico: Lado Derecho")

    def download_graphs4(self,numero_pagina):

        if(self.rad_mean_r_data==[] or self.rad_mean_l_data==[]):
            print("Detecto en graphs4 que es none")
            return
        else:
            # Ajustar los límites para eliminar espacio en blanco
            self.figure_defl_mean_l.gca().set_ylim(0,max(self.rad_mean_l_data)+200)   # Ajustar límites en el eje y según tu necesidad
            self.figure_defl_mean_r.gca().set_ylim(0,max(self.rad_mean_r_data)+200)   # Ajustar límites en el eje y según tu necesidad

            self.figure_defl_mean_l.savefig('radios_l.png', bbox_inches='tight')
            self.figure_defl_mean_r.savefig('radios_r.png', bbox_inches='tight')
        
            # Crear un nuevo PDF con ambas figuras
            output_pdf = 'radios.pdf'
            c = canvas.Canvas(output_pdf, pagesize=A4)
            ancho_pagina,alto_pagina=A4
            centro_x = ancho_pagina / 2

            c.drawImage('header2.png', 25, 773, width=575, height=60)
            c.drawImage('image.png', 0, 0, width=600, height=120)
            c.drawImage('radios_l.png',100, 200, width=383, height=230)
            c.drawImage('radios_r.png',100, 500, width=383, height=230)
            c.drawString(centro_x-1, 125, f"{numero_pagina+4}")
            c.save()
            
            os.remove('radios_l.png')
            os.remove('radios_r.png')
        
