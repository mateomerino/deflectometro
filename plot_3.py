from tkinter import *
from tkinter.ttk import Label, Frame, Button, Scrollbar
import view
import table
import graphs
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ttk
import graphs_2
import graphs_3
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
from PIL import Image, ImageTk


# Clase correspondiente a la vista encargada de mostrar los datos y graficos

class Plot3():
    def __init__(self,root,view_instance):
        self.root = root
        self.fourth_plot_frame = None
        self.botones_frame=None
        self.state_label=None
        self.hora_label=None
        self.puesto_label=None
        self.title_frame=None
        self.graphs2_frame=None
        self.graphs3_frame=None
        self.image_cba=None
        self.image_label=None
        self.imagenes_frame=None
        self.title = None
        self.subtitle=None
        self.next = None
        self.back = None 
        self.configuration=None 
        self.view_instance = view_instance
        self.Graphs2 = None 
        self.Graphs3 = None

    # Metodo que elimina todo lo que muestra la pagina
    def close(self):
        self.fourth_plot_frame.grid_forget()

    def reset(self):
        self.fourth_plot_frame.destroy()
        # self.show(0)

    def show(self,a):
       
        if(a == 0):

            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()

            fourth_plot_frame = Frame(self.root,background='#F6F4F2')
            self.fourth_plot_frame = fourth_plot_frame

            botones_frame=Frame(self.fourth_plot_frame,background='#F6F4F2')
            self.botones_frame=botones_frame

            title_frame=Frame(self.fourth_plot_frame,background='#F6F4F2')
            self.title_frame=title_frame

            graphs2_frame=Frame(self.fourth_plot_frame)
            self.graphs2_frame=graphs2_frame

            graphs3_frame=Frame(self.fourth_plot_frame)
            self.graphs3_frame=graphs3_frame

            imagenes_frame=Frame(self.fourth_plot_frame)
            self.imagenes_frame=imagenes_frame

            state_label=Label(self.botones_frame,text='', font=(None,10), background='white', foreground='black', relief='groove')
            self.state_label=state_label

            puesto_label=Label(self.botones_frame,text='',font=(None,12),background='#F6F4F2',foreground='#66A7EF')
            self.puesto_label=puesto_label

            hora_label=Label(self.botones_frame,text='',font=(None,12),background='#F6F4F2',foreground='#66A7EF')
            self.hora_label=hora_label

            back = ttk.Button(self.botones_frame, text="← Atras", command=self.go_to_plot_2_from_plot_3,style="TButton")
            self.back = back

            next = ttk.Button(self.botones_frame, text="Siguiente →", command=self.go_to_plot_4_from_plot_3,style="TButton")
            self.next = next

            configuration=ttk.Button(self.botones_frame,text="Ver configuración",command=self.show_configuration,style="TButton")
            self.configuration=configuration 

            title = Label(self.title_frame, text="Deflexiones y Radios",font=("Helvetica", 25),background='#F6F4F2',foreground='#625651')
            self.title=title
            
            subtitle=Label(self.title_frame, text="Lado Derecho",font=("Helvetica", 22),background='#F6F4F2',foreground='#625651')
            self.subtitle=subtitle

            self.Graphs2 = graphs_2.Graphs2(self.graphs2_frame, lado="Derecho")
            self.Graphs3 = graphs_3.Graphs3(self.graphs3_frame, lado="Derecho")

            original_image=Image.open("image3.png")
            screen_width = self.root.winfo_screenwidth()

            # Redimensiona la imagen al ancho de la pantalla y ajusta la altura proporcionalmente
            desired_width = screen_width
            aspect_ratio = original_image.width / original_image.height
            height=60
            # desired_height = int(desired_width / aspect_ratio)
            # resized_image = original_image.resize((desired_width, height), Image.ANTIALIAS)
            resized_image = original_image.resize((desired_width, height))

            # Convierte la imagen redimensionada a un objeto PhotoImage
            self.image_cba = ImageTk.PhotoImage(resized_image)
            self.image_label = Label(self.imagenes_frame, image=self.image_cba)
            self.image_label.image = self.image_cba

        if(a == 1):
            self.fourth_plot_frame.grid(sticky="NSEW")
            self.botones_frame.grid(row=0,columnspan=2,padx=(0,0),pady=(0,0))
            self.back.grid(row=0, column=0,padx=(0,1285),pady=(0,0),sticky=NW)
            self.next.grid(row=1,column=0,padx=(0,1285),pady=(0,0),sticky=NW)
            self.configuration.grid(row=2,column=0,padx=(0,1285),pady=(0,0))
            self.state_label.grid(row=0,column=0,padx=(0,950),pady=(0,0))
            self.puesto_label.grid(row=0,column=0,padx=(1100,0),pady=(0,0))
            self.hora_label.grid(row=1,column=0,padx=(1100,0),pady=(0,0))
            self.title_frame.grid(row=1,columnspan=2,pady=(0,0))
            self.title.grid()
            self.subtitle.grid()
            self.graphs2_frame.grid(row=2,column=0,padx=(0,650),pady=(0,0))
            self.graphs3_frame.grid(row=2,column=0,padx=(650,0),pady=(0,0))
            self.imagenes_frame.grid(row=2,padx=(0,90),pady=(385,0))
            self.image_label.grid(row=0,columnspan=2,padx=(0,0))

    def download_graphs(self):
        self.Graphs2.download_graphs2(lado="Derecho")
        self.Graphs3.download_graphs3(lado="Derecho")

    def get_hora_label(self):
        return self.hora_label
    
    def get_puesto_label(self):
        return self.puesto_label
    
    def new_group_data_plot3(self,dict_r, dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos):
        self.Graphs2.update_gmean(dict_r, dict_l,grupos,lado="Derecho")
        self.Graphs3.update_deflexiones_gmean(dict_r,dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos,lado="Derecho")

    def go_to_plot_2_from_plot_3(self):
        self.view_instance.enqueue_transition('go_to_plot_2_from_plot_3')

    def go_to_plot_4_from_plot_3(self):
        self.view_instance.enqueue_transition('go_to_plot_4_from_plot_3')

    def get_state_label(self):
        return self.state_label
    
    def show_configuration(self):
        self.view_instance.enqueue_transition('show_configuration')