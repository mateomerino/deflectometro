from tkinter import *
from tkinter.ttk import Label, Frame, Button, Scrollbar
from tkinter.ttk import Treeview

from tkinter import ttk
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Spacer, Image, Paragraph
from reportlab.lib import utils
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, PageTemplate,Image, Spacer
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox


# Clase correspondiente a la vista encargada de mostrar los datos y graficos

class Plot5():
    def __init__(self,root,view_instance):

        self.root = root
        self.sixth_plot_frame = None
        self.top_frame=None
        self.state_frame=None
        self.state_label=None
        self.state=None
        self.title_frame=None
        self.subtitle_frame=None
        self.labels_frame=None
        self.puesto_label=None
        self.hora_label=None
        self.botones_frame=None
        self.title = None
        self.back = None
        self.configuration=None
        self.stats = None 
        self.pdf = None 
        self.view_instance = view_instance
        self.Graphs2 = None

        self.huella_ext = None 

        self.defl_media_der = None
        # self.defl_media_der_value = None
        self.defl_media_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        
        self.desv_std_der = None
        self.desv_std_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.coef_var_der = None
        self.coef_var_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.defl_car_der = None
        self.defl_car_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.total_med_defl_der = None
        self.total_med_defl_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.radio_med_der = None
        self.radio_med_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.radio_car_der = None
        self.radio_car_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.total_med_rad_der = None
        self.total_med_rad_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')
        
        self.d_r_med_der = None
        self.d_r_med_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.r_x_d_der = None
        self.r_x_d_der_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')
        ##############
        self.whitespace = None 
        ##############

        self.huella_int = None
        self.huella_int_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.defl_media_izq = None
        self.defl_media_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.desv_std_izq = None
        self.desv_std_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.coef_var_izq = None
        self.coef_var_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.defl_car_izq = None
        self.defl_car_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.total_med_defl_izq = None
        self.total_med_defl_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.radio_med_izq = None
        self.radio_med_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.radio_car_izq = None
        self.radio_car_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.total_med_rad_izq = None
        self.total_med_rad_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.d_r_med_izq = None
        self.d_r_med_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')

        self.r_x_d_izq = None
        self.r_x_d_izq_value=Label(self.labels_frame,font=(None, 10),background='#F6F4F2',foreground='#625651')
        self.empty_value=''
        self.ruta=None

        self.imagen_frame=None
        self.image_cba=None
        self.image_label=None

    # Metodo que elimina todo lo que muestra la pagina
    def close(self):
        self.sixth_plot_frame.grid_forget()

    def reset(self):
        self.sixth_plot_frame.destroy()
        # self.show(0)

    def show(self,a):
       
        if(a==0):

            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()

            sixth_plot_frame = Frame(self.root, width=width, height=height,background='#F6F4F2')
            self.sixth_plot_frame = sixth_plot_frame

            top_frame=Frame(self.sixth_plot_frame, width=width, height=height,background='#F6F4F2')
            self.top_frame=top_frame

            title_frame=Frame(self.sixth_plot_frame,background='#F6F4F2')
            self.title_frame=title_frame

            subtitle_frame=Frame(self.sixth_plot_frame,background='#F6F4F2')
            self.subtitle_frame=subtitle_frame

            labels_frame=Frame(self.sixth_plot_frame,background='#F6F4F2')
            self.labels_frame=labels_frame

            botones_frame=Frame(self.sixth_plot_frame,background='#F6F4F2')
            self.botones_frame=botones_frame

            state_label=Label(self.top_frame,text='',font=(None,10), background='white', foreground='black', relief='groove')
            self.state_label=state_label

            puesto_label=Label(self.top_frame,text='',font=(None,12),background='#F6F4F2',foreground='#66A7EF')
            self.puesto_label=puesto_label

            hora_label=Label(self.top_frame,text='',font=(None,12),background='#F6F4F2',foreground='#66A7EF')
            self.hora_label=hora_label

            imagen_frame=Frame(self.sixth_plot_frame)
            self.imagen_frame=imagen_frame

            title = Label(self.title_frame, text="PLANILLA GENERAL DE RESULTADOS ESTADISTICOS",font=(None, 18),background='#F6F4F2',foreground='#625651') 
            self.title = title

            back = ttk.Button(self.top_frame, text="← Atras", command=self.go_to_plot_4_from_plot_5,style="TButton")
            self.back = back

            configuration=ttk.Button(self.top_frame,text="Ver configuración",command=self.show_configuration,style="TButton")
            self.configuration=configuration 
            
            stats = ttk.Button(self.botones_frame, text="Generar Cálculos", command=self.generate_stats,style="TButton")
            self.stats = stats

            pdf = ttk.Button(self.botones_frame, text="Descargar PDF", command=self.download_pdf,style="TButton")
            self.pdf = pdf

            huella_ext = Label(self.labels_frame, text="HUELLA EXTERNA (DERECHA)",font=(None, 15),background='#F6F4F2',foreground='#625651')
            self.huella_ext = huella_ext

            defl_media_der = Label(self.labels_frame, text="Deflexion media:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.defl_media_der = defl_media_der
           
            desv_std_der = Label(self.labels_frame, text="Desviacion Standart:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.desv_std_der = desv_std_der
            
            coef_var_der = Label(self.labels_frame, text="Coeficiente de variacion:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.coef_var_der = coef_var_der

            defl_car_der = Label(self.labels_frame, text="Deflexion caracteristica:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.defl_car_der = defl_car_der
            
            total_med_defl_der = Label(self.labels_frame, text="Total de mediciones:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.total_med_defl_der = total_med_defl_der
            
            radio_med_der = Label(self.labels_frame, text="Radio Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.radio_med_der = radio_med_der
            
            radio_car_der = Label(self.labels_frame, text="Radio Caracteristico:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.radio_car_der = radio_car_der
            
            total_med_rad_der = Label(self.labels_frame, text="Total de Mediciones:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.total_med_rad_der = total_med_rad_der
            
            d_r_med_der = Label(self.labels_frame, text="(D / R) Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.d_r_med_der = d_r_med_der
            
            r_x_d_der = Label(self.labels_frame, text="(R x D) Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.r_x_d_der = r_x_d_der

            huella_int = Label(self.labels_frame, text="HUELLA INTERNA (IZQUIERDA)",font=(None, 15),background='#F6F4F2',foreground='#625651')
            self.huella_int = huella_int

            defl_media_izq = Label(self.labels_frame, text="Deflexion media:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.defl_media_izq = defl_media_izq
            
            desv_std_izq = Label(self.labels_frame, text="Desviacion Standart:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.desv_std_izq = desv_std_izq
            
            coef_var_izq = Label(self.labels_frame, text="Coeficiente de variacion:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.coef_var_izq = coef_var_izq
            
            defl_car_izq = Label(self.labels_frame, text="Deflexion caracteristica:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.defl_car_izq = defl_car_izq
            
            total_med_defl_izq = Label(self.labels_frame, text="Total de mediciones:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.total_med_defl_izq = total_med_defl_izq
            
            radio_med_izq = Label(self.labels_frame, text="Radio Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.radio_med_izq = radio_med_izq
            
            radio_car_izq = Label(self.labels_frame, text="Radio Caracteristico:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.radio_car_izq = radio_car_izq
            
            total_med_rad_izq = Label(self.labels_frame, text="Total de Mediciones:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.total_med_rad_izq = total_med_rad_izq
            
            d_r_med_izq = Label(self.labels_frame, text="(D / R) Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.d_r_med_izq = d_r_med_izq
            
            r_x_d_izq = Label(self.labels_frame, text="(R x D) Medio:",font=(None, 13),background='#F6F4F2',foreground='#625651')
            self.r_x_d_izq = r_x_d_izq

            original_image=Image.open("image.png")
            screen_width = self.root.winfo_screenwidth()

            # Redimensiona la imagen al ancho de la pantalla y ajusta la altura proporcionalmente
            desired_width = screen_width
            aspect_ratio = original_image.width / original_image.height
            height=230
            desired_height = int(desired_width / aspect_ratio)
            # resized_image = original_image.resize((desired_width, height), Image.ANTIALIAS)
            resized_image = original_image.resize((desired_width, height))
            print("Desired:",desired_width)
            # Convierte la imagen redimensionada a un objeto PhotoImage
            self.image_cba = ImageTk.PhotoImage(resized_image)
            self.image_label = Label(self.imagen_frame, image=self.image_cba)
            self.image_label.image = self.image_cba
            

        if(a == 1):

            self.sixth_plot_frame.grid(sticky="nsew")
            self.top_frame.grid(row=0,columnspan=2,padx=(0,0),pady=(0,0))
            self.back.grid(row=0, column=0,padx=(0,1285),pady=(0,0),sticky=NW)
            self.configuration.grid(row=1, column=0,padx=(0,1285),pady=(0,0),sticky=NW)
            self.state_label.grid(row=0,column=0,padx=(0,950),pady=(0,0))
            self.puesto_label.grid(row=0,column=0,padx=(1100,0),pady=(0,0))
            self.hora_label.grid(row=1,column=0,padx=(1100,0),pady=(6,0))
            self.title_frame.grid(row=1,columnspan=2,padx=(0,0),pady=(0,0))
            self.title.grid(row=0, column=0,padx=(0,0))

            self.labels_frame.grid(row=2,columnspan=2,pady=(0,0))
            self.huella_ext.grid(row=0,column=0,padx=(0,150))
            self.huella_int.grid(row=0,column=1,padx=(150,0))
            
            self.defl_media_der.grid(row=1, column=0,sticky=NW,pady=(0,4))
            self.desv_std_der.grid(row=2,sticky=NW,pady=(0,4))
            self.coef_var_der.grid(row=3, column=0,sticky=NW,pady=(0,4))
            self.defl_car_der.grid(row=4, column=0,sticky=NW,pady=(0,4))
            self.total_med_defl_der.grid(row=5, column=0,sticky=NW,pady=(0,4))
            self.radio_med_der.grid(row=6, column=0,sticky=NW,pady=(0,4))
            self.radio_car_der.grid(row=7, column=0,sticky=NW,pady=(0,4))
            self.total_med_rad_der.grid(row=8, column=0,sticky=NW,pady=(0,4))
            self.d_r_med_der.grid(row=9, column=0,sticky=NW,pady=(0,4))
            self.r_x_d_der.grid(row=10, column=0,sticky=NW,pady=(0,0))

            # # self.whitespace.grid(row=12+2, column=0,sticky=NW)
            
            self.defl_media_izq.grid(row=1, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.desv_std_izq.grid(row=2, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.coef_var_izq.grid(row=3, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.defl_car_izq.grid(row=4, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.total_med_defl_izq.grid(row=5, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.radio_med_izq.grid(row=6, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.radio_car_izq.grid(row=7, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.total_med_rad_izq.grid(row=8, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.d_r_med_izq.grid(row=9, column=1,padx=(150,0),sticky=NW,pady=(0,4))
            self.r_x_d_izq.grid(row=10, column=1,padx=(150,0),sticky=NW,pady=(0,0))

            self.botones_frame.grid(row=3,columnspan=2,pady=(0,0))
            self.stats.grid(row=0,pady=(0,0))
            self.pdf.grid(row=1,pady=(0,0))
            self.imagen_frame.grid(row=4,padx=(0,90),pady=(0,0))
            self.image_label.grid(row=0,columnspan=2,padx=(0,0))
    

    def grid_stats(self,media_defl_r, media_defl_izq,media_rad_der, media_rad_izq,desv_defl_der, desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq, d_r_der,d_r_izq ,d_x_r_der, d_x_r_izq, total_mediciones_defl, total_mediciones_rad):
        
        print("Total mediciones defl:",total_mediciones_defl)
        print("Total mediciones rad:",total_mediciones_rad)


        empty_label=Label(self.labels_frame, text='',font=(None, 12),background='#F6F4F2',foreground='#625651')


        self.defl_media_der_value.destroy()
        self.defl_media_der_value=Label(self.labels_frame, text=media_defl_r,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.defl_media_der_value=defl_media_der_value
        # self.defl_media_der_value.config(text=media_defl_r)
        self.defl_media_der_value.grid(row=1, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        
        self.defl_media_izq_value.destroy()
        self.defl_media_izq_value=Label(self.labels_frame, text=media_defl_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.defl_media_izq_value=defl_media_izq_value
        # self.defl_media_izq_value.config(text=media_defl_izq)
        self.defl_media_izq_value.grid(row=1, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        
        self.desv_std_der_value.destroy()
        self.desv_std_der_value=Label(self.labels_frame, text=desv_defl_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.desv_std_der_value=desv_std_der_value
        # empty_label.grid(row=2, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.desv_std_der_value.grid(row=2, column=0,padx=(0,0),pady=(0,4),sticky=NE)

        self.desv_std_izq_value.destroy()
        self.desv_std_izq_value=Label(self.labels_frame, text=desv_defl_l,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # desv_std_izq_value=Label(self.labels_frame, text='desv std izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.desv_std_izq_value=desv_std_izq_value
        # empty_label.grid(row=2, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.desv_std_izq_value.grid(row=2, column=1,padx=(0,0),pady=(0,4),sticky=NE)

        self.coef_var_der_value.destroy()
        self.coef_var_der_value=Label(self.labels_frame, text=coef_var_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # coef_var_der_value=Label(self.labels_frame, text='coef_var_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.coef_var_der_value=coef_var_der_value
        # empty_label.grid(row=3, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.coef_var_der_value.grid(row=3, column=0,padx=(0,0),pady=(0,4),sticky=NE)

        self.coef_var_izq_value.destroy()
        self.coef_var_izq_value=Label(self.labels_frame, text=coef_var_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # coef_var_izq_value=Label(self.labels_frame, text='coef_var_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.coef_var_izq_value=coef_var_izq_value
        # empty_label.grid(row=3, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.coef_var_izq_value.grid(row=3, column=1,padx=(0,0),pady=(0,4),sticky=NE)

        self.defl_car_der_value.destroy()
        self.defl_car_der_value=Label(self.labels_frame, text=defl_car_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # defl_car_der_value=Label(self.labels_frame, text='defl_car_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.defl_car_der_value=defl_car_der_value
        # empty_label.grid(row=4, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.defl_car_der_value.grid(row=4, column=0,padx=(0,0),pady=(0,4),sticky=NE)

        self.defl_car_izq_value.destroy()
        self.defl_car_izq_value=Label(self.labels_frame, text=defl_car_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # defl_car_izq_value=Label(self.labels_frame, text='defl_car_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.defl_car_izq_value=defl_car_izq_value
        # empty_label.grid(row=4, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.defl_car_izq_value.grid(row=4, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.total_med_defl_der_value.destroy()
        self.total_med_defl_der_value=Label(self.labels_frame, text=total_mediciones_defl,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # total_med_defl_der_value=Label(self.labels_frame, text='total_mediciones_defl',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.total_med_defl_der_value=total_med_defl_der_value
        # empty_label.grid(row=5, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.total_med_defl_der_value.grid(row=5, column=0,padx=(0,0),pady=(0,4),sticky=NE)

        self.total_med_defl_izq_value.destroy()
        self.total_med_defl_izq_value=Label(self.labels_frame, text=total_mediciones_defl,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # total_med_defl_izq_value=Label(self.labels_frame, text='total_mediciones_defl',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.total_med_defl_izq_value=total_med_defl_izq_value
        # empty_label.grid(row=5, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.total_med_defl_izq_value.grid(row=5, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.radio_med_der_value.destroy()
        self.radio_med_der_value=Label(self.labels_frame, text=media_rad_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # radio_med_der_value=Label(self.labels_frame, text='media_rad_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # empty_label.grid(row=6, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        # self.radio_med_der_value=radio_med_der_value
        self.radio_med_der_value.grid(row=6, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        

        self.radio_med_izq_value.destroy()
        self.radio_med_izq_value=Label(self.labels_frame, text=media_rad_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # radio_med_izq_value=Label(self.labels_frame, text='media_rad_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.radio_med_izq_value=radio_med_izq_value
        # empty_label.grid(row=6, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.radio_med_izq_value.grid(row=6, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.radio_car_der_value.destroy()
        self.radio_car_der_value=Label(self.labels_frame, text=rad_car_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # radio_car_der_value=Label(self.labels_frame, text='rad_car_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.radio_car_der_value=radio_car_der_value
        # empty_label.grid(row=7, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.radio_car_der_value.grid(row=7, column=0,padx=(0,0),pady=(0,4),sticky=NE)


        self.radio_car_izq_value.destroy()
        self.radio_car_izq_value=Label(self.labels_frame, text=rad_car_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # radio_car_izq_value=Label(self.labels_frame, text='rad_car_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.radio_car_izq_value=radio_car_izq_value
        # empty_label.grid(row=7, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.radio_car_izq_value.grid(row=7, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.total_med_rad_der_value.destroy()
        self.total_med_rad_der_value=Label(self.labels_frame, text=total_mediciones_rad,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # total_med_rad_der_value=Label(self.labels_frame, text='total_mediciones_rad',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.total_med_rad_der_value=total_med_rad_der_value
        # empty_label.grid(row=8, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.total_med_rad_der_value.grid(row=8, column=0,padx=(0,0),pady=(0,4),sticky=NE)


        self.total_med_rad_izq_value.destroy()
        self.total_med_rad_izq_value=Label(self.labels_frame, text=total_mediciones_rad,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # total_med_rad_izq_value=Label(self.labels_frame, text='total_mediciones_rad',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.total_med_rad_izq_value=total_med_rad_izq_value
        # empty_label.grid(row=8, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.total_med_rad_izq_value.grid(row=8, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.d_r_med_der_value.destroy()
        self.d_r_med_der_value=Label(self.labels_frame, text=d_r_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # d_r_med_der_value=Label(self.labels_frame, text='d_r_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.d_r_med_der_value=d_r_med_der_value
        # empty_label.grid(row=9, column=0,padx=(0,0),pady=(0,4),sticky=NE)
        self.d_r_med_der_value.grid(row=9, column=0,padx=(0,0),pady=(0,4),sticky=NE)


        self.d_r_med_izq_value.destroy()
        self.d_r_med_izq_value=Label(self.labels_frame, text=d_r_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # d_r_med_izq_value=Label(self.labels_frame, text='d_r_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.d_r_med_izq_value=d_r_med_izq_value
        # empty_label.grid(row=9, column=1,padx=(0,0),pady=(0,4),sticky=NE)
        self.d_r_med_izq_value.grid(row=9, column=1,padx=(0,0),pady=(0,4),sticky=NE)


        self.r_x_d_der_value.destroy()
        self.r_x_d_der_value=Label(self.labels_frame, text=d_x_r_der,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # r_x_d_der_value=Label(self.labels_frame, text='d_x_r_der',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.r_x_d_der_value=r_x_d_der_value
        # empty_label.grid(row=10, column=0,padx=(0,0),pady=(0,0),sticky=NE)
        self.r_x_d_der_value.grid(row=10, column=0,padx=(0,0),pady=(0,0),sticky=NE)

        self.r_x_d_izq_value.destroy()
        self.r_x_d_izq_value=Label(self.labels_frame, text=d_x_r_izq,font=(None, 10),background='#F6F4F2',foreground='#625651')
        # r_x_d_izq_value=Label(self.labels_frame, text='d_x_r_izq',font=(None, 10),background='#F6F4F2',foreground='#625651')
        # self.r_x_d_izq_value=r_x_d_izq_value
        # empty_label.grid(row=10, column=1,padx=(0,0),pady=(0,0),sticky=NE)
        self.r_x_d_izq_value.grid(row=10, column=1,padx=(0,0),pady=(0,0),sticky=NE)
        self.r_x_d_izq_value.config(text=d_x_r_izq)

        
       

    def go_to_plot_4_from_plot_5(self):
        self.view_instance.enqueue_transition('go_to_plot_4_from_plot_5')

    def generate_stats(self):
        self.view_instance.enqueue_transition('generate_stats')
        self.view_instance.set_calculos_flag(1)

    def download_pdf(self):
        self.view_instance.enqueue_transition('download_pdf')

    
    def get_hora_label(self):
        return self.hora_label
    
    def get_puesto_label(self):
        return self.puesto_label

    def set_ruta(self,ruta):
        self.ruta=ruta

    def get_ruta(self):
        return self.ruta
    
    def get_state_label(self):
        return self.state_label
    
    def show_configuration(self):
        self.view_instance.enqueue_transition('show_configuration')

    def download_stats(self):
        
        buffer = BytesIO()
        
        # Crear un objeto Canvas
        c = canvas.Canvas(buffer, pagesize=A4)

        # Dibuja la imagen de encabezado
        c.drawImage('header.png', 25, 773, width=550, height=60)
        ancho_pagina,alto_pagina=A4
        centro_x = ancho_pagina / 2
        c.drawString(centro_x-1, 125, "1")
        c.drawImage('image.png', 0, 0, width=600, height=120)

        labels_der = [
            self.defl_media_der, self.desv_std_der, 
            self.coef_var_der, self.defl_car_der, self.total_med_defl_der, 
            self.radio_med_der, self.radio_car_der, self.total_med_rad_der, 
            self.d_r_med_der, self.r_x_d_der 
        ]
        
        labels_izq= [
            self.defl_media_izq, self.desv_std_izq, 
            self.coef_var_izq, self.defl_car_izq, self.total_med_defl_izq,
            self.radio_med_izq, self.radio_car_izq, self.total_med_rad_izq, 
            self.d_r_med_izq, self.r_x_d_izq
        ]

        labels_der_values=[
            self.defl_media_der_value, self.desv_std_der_value, 
            self.coef_var_der_value, self.defl_car_der_value, self.total_med_defl_der_value, 
            self.radio_med_der_value, self.radio_car_der_value, self.total_med_rad_der_value, 
            self.d_r_med_der_value, self.r_x_d_der_value 
        ]

        labels_izq_values= [
            self.defl_media_izq_value, self.desv_std_izq_value, 
            self.coef_var_izq_value, self.defl_car_izq_value, self.total_med_defl_izq_value,
            self.radio_med_izq_value, self.radio_car_izq_value, self.total_med_rad_izq_value, 
            self.d_r_med_izq_value, self.r_x_d_izq_value
        ]

          # Configura el estilo de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),  # Fondo para todas las filas
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),   # Color de texto para todas las filas
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        titulo_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        titulo_der="HUELLA EXTERNA (DERECHA)"
        tabla_der = []

        titulo_izq="HUELLA INTERNA (IZQUIERDA)"
        tabla_izq = []

        for label,value in zip(labels_der, labels_der_values):
            tabla_der.append([label.cget("text"), value.cget("text")])

        for label,value in zip(labels_izq, labels_izq_values):
            tabla_izq.append([label.cget("text"), value.cget("text")])

        # Dibuja la tabla derecha
        tabla_datos_der = Table(tabla_der, colWidths=[200, 200], rowHeights=22)
        tabla_datos_der.setStyle(table_style)
        tabla_titulo_der = Table([[titulo_der]], colWidths=[400])
        tabla_titulo_der.setStyle(titulo_style)
        tabla_titulo_der.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
        tabla_titulo_der.drawOn(c, 95, 700) 
        tabla_datos_der.wrapOn(c, 400, 400)  # Ajusta el tamaño de la tabla si es necesario
        tabla_datos_der.drawOn(c, 95, 480)  # Dibuja la tabla en las coordenadas especificadas

        # Dibuja la tabla izquierda
        tabla_datos_izq = Table(tabla_izq, colWidths=[200, 200], rowHeights=22)
        tabla_datos_izq.setStyle(table_style)
        tabla_titulo_izq = Table([[titulo_izq]], colWidths=[400])
        tabla_titulo_izq.setStyle(titulo_style)
        tabla_titulo_izq.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
        tabla_titulo_izq.drawOn(c, 95, 440) 
        tabla_datos_izq.wrapOn(c, 400, 400)  # Ajusta el tamaño de la tabla si es necesario
        tabla_datos_izq.drawOn(c, 95, 225)  # Dibuja la tabla en las coordenadas especificadas

        # Guarda el PDF en el buffer
        c.showPage()
        c.save()

        # Guarda el contenido del buffer en un archivo
        buffer.seek(0)
        with open('stats.pdf', 'wb') as f:
            f.write(buffer.read())


        




  