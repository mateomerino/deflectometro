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
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
# Clase donde se inicializan y actualizan los graficos

class Graphs2():
    def __init__(self, frame,lado):
        self.frame = frame
        self.figure_rad_mean_r = None
        self.rad_mean_r = None
        self.rad_mean_widget_l = None
        self.figure_rad_mean_l = None 
        self.rad_mean_l = None 
        self.rad_mean_widget_l = None
        self.rad_r_data=[]
        self.rad_l_data=[]
        self.indexes=[] 
        self.show(lado)

    def radio_gmean_graph(self,row, column,title):
        
        figure = Figure(figsize=(7, 6), dpi=100,facecolor='#F6F4F2')
        sub_figure = figure.add_subplot(211)
        sub_figure.set_xlim(0,100)
        sub_figure.set_ylim(0,100)
        sub_figure.set_title(title)
        sub_figure.set_xlabel("Nº Grupo")
        sub_figure.set_ylabel("Radio de Curvatura")
        sub_figure.scatter([], [])
        sub_figure.grid(axis='both',linestyle='dotted')
        graph = FigureCanvasTkAgg(figure, self.frame)
        graph_widget = graph.get_tk_widget()
        graph_widget.grid(row = row, column = column,padx=(0,0))
        figure.subplots_adjust(bottom=0,top=0.93)
        return figure, graph, graph_widget
    

    def update_gmean(self, dict_r, dict_l,grupos,lado):

        self.rad_r_data.extend(dict_r['Radio'][-1:])
        self.rad_l_data.extend(dict_l['Radio'][-1:])
        self.indexes = [x * grupos for x in range(1, len(self.rad_l_data)+1)]


        if(lado == "Izquierdo"):

            # self.figure_rad_mean_l, self.rad_mean_l, self.rad_mean_widget_l = self.radio_gmean_graph(3,0,1,"Radio Izquierda")
            self.figure_rad_mean_l.clear()
            subfigure_izq=self.figure_rad_mean_l.add_subplot(211)

            subfigure_izq.set_xlim(min(self.indexes)-50, max(self.indexes)+50)
            subfigure_izq.set_ylim(0,max(self.rad_l_data)+50)

            subfigure_izq.plot(self.indexes, self.rad_l_data,'o-')

            subfigure_izq.set_title("Radio Izquierda")
            subfigure_izq.set_xlabel("Nº Grupo")
            subfigure_izq.set_ylabel("Radio de curvatura")

            subfigure_izq.grid(axis='both',linestyle='dotted')
        
            self.figure_rad_mean_l.canvas.draw_idle()

        if(lado == "Derecho"):

            # self.figure_rad_mean_r, self.rad_mean_r, self.rad_mean_widget_r = self.radio_gmean_graph(3,0,1,"Radio Derecha")
            self.figure_rad_mean_r.clear()
            subfigure_der=self.figure_rad_mean_r.add_subplot(211)

            subfigure_der.set_xlim(min(self.indexes)-50, max(self.indexes)+50)
            subfigure_der.set_ylim(0, max(self.rad_r_data)+50)

            subfigure_der.plot(self.indexes, self.rad_r_data,'o-')
            
            subfigure_der.set_title("Radio Derecha")
            subfigure_der.set_xlabel("Nº Grupo")
            subfigure_der.set_ylabel("Radio de curvatura")

            subfigure_der.grid(axis='both',linestyle='dotted')
            
            self.figure_rad_mean_r.canvas.draw_idle()

    def show(self,lado):
        
        if(lado == "Derecho"):
            self.figure_rad_mean_r, self.rad_mean_r, self.rad_mean_widget_r = self.radio_gmean_graph(0,1,"Radio Derecha")
        
        if(lado == "Izquierdo"):
            self.figure_rad_mean_l, self.rad_mean_l, self.rad_mean_widget_l = self.radio_gmean_graph(2,0,"Radio Izquierda")
           
    def download_graphs2(self,lado):
        
        if(self.rad_l_data==[] or self.rad_r_data==[]):
            print("Detecto en graphs2 que es none")
            return
        
        else:
            if(lado=="Izquierdo"):
                self.figure_rad_mean_l.gca().set_ylim(0, max(self.rad_l_data)+50)  # Ajustar límites en el eje y según tu necesidad
                self.figure_rad_mean_l.savefig('figure_rad_l.png', bbox_inches='tight')

            if(lado=="Derecho"):
                self.figure_rad_mean_r.gca().set_ylim(0, max(self.rad_r_data)+50)  # Ajustar límites en el eje y según tu necesidad
                self.figure_rad_mean_r.savefig('figure_rad_r.png', bbox_inches='tight')
            
           
        
        
        

        

           
       


   



    





























   

    # # Metodo donde se inicializan los graficos
    

    

   
       

    # Actualiza el grafico de bars de mediciones individuales
    # se pasa como parametro un dict con los datos de los dos lados
    
        # self.figure_bar_l.add_subplot(211).bar(index, defl_left_right_dict['left'])
        

    # Toma los nuevos valores y hace el update de los graficos
    # el update se hace limpiando y volviendo a graficar. (quizas hay otra solucion, la que probe no funcionaba)
    # def update_gmean(self, dict_r, dict_l):

    #     self.figure_rad_mean_r.clear()

    #     subfigure = self.figure_rad_mean_r.add_subplot(211)

    #     subfigure.set_title("Radio Derecha")

    #     subfigure.scatter(dict_r['Grupo'], dict_r['Defl.'], color = 'r')

    #     subfigure.draw()

        # self.figure_rad_mean_r.add_subplot(211).scatter(dict_r['Grupo'], dict_r['Defl.'], color = 'r')

        # self.rad_mean_r.draw()

        # self.figure_rad_mean_l.clear()
        # self.figure_rad_mean_l.add_subplot(211).scatter(dict_l['Grupo'], dict_l['Defl.'], color = 'r')
        # self.rad_mean_l.draw()


