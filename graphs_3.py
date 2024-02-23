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

# Clase donde se inicializan y actualizan los graficos

class Graphs3():
    def __init__(self, frame,lado):

        self.frame = frame
        self.figure_defl_mean_r = None
        self.defl_mean_r = None
        self.defl_mean_widget_l = None
        self.figure_defl_mean_l = None 
        self.defl_mean_l = None 
        self.defl_mean_widget_l = None
        self.max_value=0
        self.defl_mean_l_data=[]
        self.defl_mean_r_data=[]
        self.defl_car_l_data=[]
        self.defl_car_r_data=[]
        self.defl_max_l_data=[]
        self.defl_max_r_data=[]
        self.indexes=[] 
        self.show(lado)


    def show(self,lado):

        self.show_deflexiones_gmean_graph(lado)

    
    def deflexiones_gmean_graph(self,row, column,title):
        
        # figure = Figure(figsize=(7, 6), dpi=100,facecolor='#F6F4F2')
        figure = Figure(figsize=(7, 6), dpi=100,facecolor='#F6F4F2')
        figure.subplots_adjust(bottom=0,top=0.93)
        sub_figure=figure.add_subplot(211)
        sub_figure.set_title(title)

        # sub_figure.set_xlim(0,20)

        sub_figure.set_ylim(0,100)
        sub_figure.set_xlabel("Progresivas")
        sub_figure.set_ylabel("Deflexiones")

        sub_figure.bar([], [], width = 3, linewidth=0)
        sub_figure.grid(axis='both',linestyle='dotted')

        bar = FigureCanvasTkAgg(figure,self.frame)
        bar_widget = bar.get_tk_widget()
        bar_widget.grid(row = row, column = column)
        return figure, bar, bar_widget
    
    def update_deflexiones_gmean(self, dict_r, dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos,lado):

        self.defl_mean_l_data.extend(dict_l['Defl.'][-1:])
        self.defl_car_l_data.extend(defl_l_car[-1:])
        self.defl_max_l_data.extend(defl_l_max[-1:])
        self.indexes = [x * grupos for x in range(1, len(self.defl_mean_l_data)+1)]
        self.defl_mean_r_data.extend(dict_r['Defl.'][-1:])
        self.defl_car_r_data.extend(defl_r_car[-1:])
        self.defl_max_r_data.extend(defl_r_max[-1:])
        self.indexes = [x * grupos for x in range(1, len(self.defl_mean_r_data)+1)]
        max_value = max(
        max(self.defl_mean_l_data),
        max(self.defl_car_l_data),
        max(self.defl_max_l_data)
        )
        if max_value > self.max_value:
            self.max_value = max_value
        
        if(lado == "Izquierdo"):
            # self.indexes=list(range(1,len(self.defl_mean_l_data)+1))
          
            self.figure_defl_mean_l.clear()

            subfigure_izq = self.figure_defl_mean_l.add_subplot(211)
            
            subfigure_izq.set_xlim(min(self.indexes)-50, max(self.indexes)+50)
            subfigure_izq.set_ylim(0,self.max_value+50)  
            
            subfigure_izq.bar(self.indexes, self.defl_mean_l_data, color='black', width=1, edgecolor='black')
            subfigure_izq.plot(self.indexes, self.defl_car_l_data)
            subfigure_izq.scatter(self.indexes, self.defl_max_l_data)
            subfigure_izq.legend(['Defl. Caracterist', 'Defl. Máxima', 'Defl. Promedio'], 
                        loc='upper center', bbox_to_anchor=(0.5, -0.2)) 
            subfigure_izq.grid(axis='both', linestyle='dotted')

            subfigure_izq.set_title("Deflexiones Izquierda")
            subfigure_izq.set_xlabel("Progresivas")
            subfigure_izq.set_ylabel("Deflexiones")
        
            self.figure_defl_mean_l.canvas.draw_idle()

        if(lado == "Derecho"):
            # self.indexes=list(range(1,len(self.defl_mean_r_data)+1))
            
            self.figure_defl_mean_r.clear()

            subfigure_der=self.figure_defl_mean_r.add_subplot(211)

            subfigure_der.set_xlim(min(self.indexes)-50, max(self.indexes)+50)
            subfigure_der.set_ylim(0,self.max_value+50)
            
            subfigure_der.bar(self.indexes, self.defl_mean_r_data, color='black', width=1, edgecolor='black')
            subfigure_der.plot(self.indexes, self.defl_car_r_data)
            subfigure_der.scatter(self.indexes, self.defl_max_r_data)
            # subfigure_der.legend(['Defl. Caracterist','Defl. Máxima', 'Defl. Promedio'])  # Leyendas para el scatter y el plot
            subfigure_der.legend(['Defl. Caracterist', 'Defl. Máxima', 'Defl. Promedio'], 
                     loc='upper center', bbox_to_anchor=(0.5, -0.2))

            subfigure_der.grid(axis='both', linestyle='dotted')

            subfigure_der.set_title("Deflexiones Derecha")
            subfigure_der.set_xlabel("Progresivas")
            subfigure_der.set_ylabel("Deflexiones")
            
            self.figure_defl_mean_r.canvas.draw_idle()
        
    def show_deflexiones_gmean_graph(self,lado):

        if(lado == "Derecho"):
            self.figure_defl_mean_r, self.defl_mean_r, self.defl_mean_widget_r = self.deflexiones_gmean_graph(0,0,"Deflexiones Derecha")

        if(lado == "Izquierdo"):
            self.figure_defl_mean_l, self.defl_mean_l, self.defl_mean_widget_l = self.deflexiones_gmean_graph(0,0,"Deflexiones Izquierda")


    def download_graphs3(self,lado):
        print("Defl mean l data:",self.defl_mean_l_data)
        print("Defl mean r data:",self.defl_mean_r_data)

        if(self.defl_mean_l_data==[] or self.defl_mean_r_data==[]):
            print("Detecto en graphs3 que es none")
            return
        else:
            if(lado=="Izquierdo"):

                self.figure_defl_mean_l.gca().set_ylim(0, max(self.defl_mean_l_data)+50)   # Ajustar límites en el eje y según tu necesidad
                self.figure_defl_mean_l.savefig('figure_defl_mean_l.png', bbox_inches='tight')
                
            if(lado=="Derecho"):
                
                self.figure_defl_mean_r.gca().set_ylim(0, max(self.defl_mean_r_data)+50)  # Ajustar límites en el eje y según tu necesidad
                self.figure_defl_mean_r.savefig('figure_defl_mean_r.png', bbox_inches='tight')
                
           