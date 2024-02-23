from tkinter import *
from tkinter.ttk import Label, Frame, Button, Scrollbar
from PIL import Image, ImageTk 
import view
import table
import graphs
from tkinter.ttk import Treeview
import tkinter as tk
import datetime
from tkinter.ttk import Treeview
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from tkinter import messagebox



# Clase correspondiente a la vista encargada de mostrar los datos y graficos

class Plot():
    def __init__(self,root,view_instance):

        self.root = root
        self.second_plot_frame = None
        self.botones_frame=None
        self.table_frame=None
        self.state_label=None
        self.state=None
        self.graphs_frame=None
        self.labels_frame=None
        self.imagen_frame=None
        self.image_cba=None
        self.image_label=None
        self.view_instance = view_instance
        self.title = None 
        self.temperatura = None 
        self.muestras = None 
        self.grupos = None 
        self.atras = None 
        self.next = None
        self.configuration=None 
        self.Table = None
        self.Graphs = None
        self.label_der=None
        self.label_izq=None
        self.hora_inicio=None
        self.puesto_label=None
        self.hora_label=None

    # Metodo que elimina todo lo que muestra la pagina
    def close(self):
        self.second_plot_frame.grid_forget()
    
    def reset(self):
        self.second_plot_frame.destroy()
        # self.show(0)

    def get_state_label(self):
        return self.state_label
    
    def get_puesto_label(self):
        return self.puesto_label
    
    def get_hora_label(self):
        return self.hora_label
    
    def get_puesto_label(self):
        return self.puesto_label
    
    def show(self,a):

        if(a == 0):
            second_plot_frame = Frame(self.root)
            self.second_plot_frame = second_plot_frame
            
            botones_frame=Frame(self.second_plot_frame)
            self.botones_frame=botones_frame

            labels_frame=Frame(self.second_plot_frame)
            self.labels_frame=labels_frame

            table_frame=Frame(self.second_plot_frame)
            self.table_frame=table_frame

            graphs_frame=Frame(self.second_plot_frame)
            self.graphs_frame=graphs_frame

            imagen_frame=Frame(self.second_plot_frame)
            self.imagen_frame=imagen_frame

            state_label=Label(self.botones_frame,text='',font=(None,10),background='white',foreground='black',relief='groove')
            self.state_label=state_label

            puesto_label=Label(self.botones_frame,text='',font=(None,12),foreground='#66A7EF')
            self.puesto_label=puesto_label

            hora_label=Label(self.botones_frame,text='',font=(None,12),foreground='#66A7EF')
            self.hora_label=hora_label

            columns = ("columna1", "columna2", "columna3", "columna4","columna5","columna6")  # Especifica los nombres de las columnas

            self.table = Treeview(self.table_frame, columns=columns, show='headings')
            
            atras = ttk.Button(self.botones_frame, text="← Atras", command=self.go_to_config,style="TButton")
            self.atras=atras

            next = ttk.Button(self.botones_frame,text="Siguiente →",command=self.go_to_plot_2_from_plot_1,style="TButton")
            self.next = next

            configuration=ttk.Button(self.botones_frame,text="Ver configuración",command=self.show_configuration,style="TButton")
            self.configuration=configuration 

            self.Table = table.Tabla(self.table_frame) 
            self.Graphs = graphs.Graphs(self.graphs_frame) 

            label_der = Label(self.labels_frame, text="Huella Externa (DERECHA)", font=("Helvetica", 19))
            self.label_der=label_der

            label_izq = Label(self.labels_frame, text="Huella Interna (IZQUIERDA)", font=("Helvetica", 19))
            self.label_izq=label_izq

            original_image=Image.open("image3.png")
            screen_width = self.root.winfo_screenwidth()

            # Redimensiona la imagen al ancho de la pantalla y ajusta la altura proporcionalmente
            desired_width = screen_width+10
            aspect_ratio = original_image.width / original_image.height
            height=60
            desired_height = int(desired_width / aspect_ratio)
            print("desired height",desired_height)
            # resized_image = original_image.resize((desired_width, height), Image.ANTIALIAS)
            resized_image = original_image.resize((desired_width, height))

            # Convierte la imagen redimensionada a un objeto PhotoImage
            self.image_cba = ImageTk.PhotoImage(resized_image)
            self.image_label = Label(self.imagen_frame, image=self.image_cba)
            self.image_label.image = self.image_cba

        if(a == 1):
            self.second_plot_frame.grid(sticky=NSEW)
            self.botones_frame.grid(row=0,columnspan=2,padx=(0,0),pady=(0,0))  
            self.atras.grid(row=0, column=0,padx=(0,1275),pady=(0,0),sticky=NW)
            self.next.grid(row=1, column=0,padx=(0,1275),pady=(0,0),sticky=NW)
            self.configuration.grid(row=2,column=0,padx=(0,1275),pady=(0,0))
            self.state_label.grid(row=0,column=0,padx=(0,950),pady=(0,0))
            self.puesto_label.grid(row=0,column=0,padx=(1100,0))
            self.hora_label.grid(row=1,column=0,padx=(1100,0))

            self.labels_frame.grid(row=0,columnspan=2,padx=(0,0),pady=(70,0))
            self.label_izq.grid(row=1, column=0,padx=(0,350))
            self.label_der.grid(row=1, column=0,padx=(550,0))

            self.table_frame.grid(row=1,padx=(0,45),pady=(0,0))
            self.graphs_frame.grid(row=3,columnspan=2,padx=(0,0),pady=(0,0))

            self.imagen_frame.grid(row=3,padx=(0,60),pady=(135,0))
            self.image_label.grid(row=0,columnspan=2,padx=(0,0))
            
            
    def generar_pdf(self):
        self.Table.donwload_table()
        numero_pagina=self.Table.get_numero_pagina()
        self.Graphs.donwload_graphs(numero_pagina)
        
    def get_prog_max(self):
        return self.Graphs.get_max()
 
    def set_ruta(self,ruta):
        self.Table.set_ruta(ruta)
        self.Table.set_fecha(datetime.datetime.now().date())

    def grid_plot1(self):
        self.second_plot_frame.grid(ipadx=10, ipady=5)

    def update_bar_plot(self, defl_r,defl_l):
        self.Graphs.update_bar(defl_r,defl_l)

    def get_table(self):
        return self.Table

    # Metodo que recibe los datos nuevos y manda a actualizar estructuras y plots
    def new_group_data_plot(self,dict_r, dict_l):
        self.Table.insert(dict_r, dict_l)

    def go_to_plot_2_from_plot_1(self):
        self.view_instance.enqueue_transition('go_to_plot_2_from_plot_1')
        
    def show_configuration(self):
        self.view_instance.enqueue_transition('show_configuration')

    def go_to_config(self):
        self.view_instance.enqueue_transition('go_to_config')

    def reset_table(self):
        self.Table.reset()

    
   


