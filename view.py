import tkinter as tk
from tkinter import *
from tkinter.ttk import Scrollbar
import threading
from threading import Thread
from tkinter.ttk import Style
from ttkthemes import ThemedTk
import config
import plot
import plot_2
import plot_3
import plot_4
import plot_5
import queue
import time
import PyPDF2
import os
from time import sleep
import datetime
from reportlab.lib.pagesizes import letter, landscape,A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
from tkinter import messagebox
from tkinter import ttk

class View():
    def __init__(self, root,data_instance,reporter_instance):


        self.state=None
        self.root=root
        self.temp = None
        self.grupos = None
        self.muestras = None
        self.espesor = None
        self.ft_ntry = None
        self.fh_ntry = None
        self.fc_ntry = None
        self.z_ntry = None
        self.ruta_ntry=None
        self.provincia_ntry=None
        self.tramo_ntry=None
        self.subtramo_ntry=None
        self.pavimento_ntry=None
        self.operador_ntry=None
        self.chofer_ntry=None
        self.apoyo_ntry=None
        self.data_instance = data_instance
        self.reporter_instance = reporter_instance
        self.data_ready=0
        self.reset=None
        self.state=None
        #Se crean los objetos Plot y Config como atributos de view 
        self.Config = config.Config(self.root,self)
        self.Plot = plot.Plot(self.root, self)
        self.Plot2 = plot_2.Plot2(self.root,self)
        self.Plot3 = plot_3.Plot3(self.root,self)
        self.Plot4 =plot_4.Plot4(self.root,self)
        self.Plot5= plot_5.Plot5(self.root,self)
        self.is_plotting = False
        self.hora_inicio=None
        self.nro_puesto=None
        self.calculos_flag=0
        self.datos_ready_flag=0
        self.width=None
        self.height=None
        ##############
        self.amount=None
        ################
         # Crear una cola bloqueante para las funciones de transición de interfaz
        self.interface_transition_queue = queue.Queue()
        self.enqueued_functions = set()
        # Crear un solo hilo para ejecutar las funciones de transición de interfaz
        self.interface_transition_thread = threading.Thread(target=self.interface_transition_function)
        self.interface_transition_thread.start()
        self.start(root)

        # self.Plot.show()

     # Metodo que inicializa la view:
    def start(self,root):
        self.root.title('Deflectómetro')
        style = Style(root)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        # self.root.attributes('-fullscreen',True) 
        # self.root.state('zoomed')
        self.root.attributes('-zoomed')
        self.inicializar_plots()

    def inicializar_plots(self):
        self.Config.show(0)
        self.Config.show(1)
        self.Plot.show(0)
        self.Plot2.show(0)
        self.Plot3.show(0)
        self.Plot4.show(0)
        self.Plot5.show(0)
     # Metodo que borra el frame Config y abre el Plot1
    def go_to_plot1_from_config(self):
        self.Config.close()
        self.Plot.show(1)
       
    # Metodo que borra el Plot 1 y abre el de Config
    def go_to_config(self):
        self.Plot.close()
        self.Config.show(1)

    # # Metodo que borra el Plot 1 y abre el Plot 2
    def go_to_plot_2_from_plot_1(self):
        self.Plot.close()
        self.Plot2.show(1)

    # Metodo que borra el Plot 2 y abre el Plot 1
    def go_to_plot_1_from_plot_2(self):
        self.Plot2.close()
        self.Plot.show(1) 

    def go_to_plot_3_from_plot2(self):
        self.Plot2.close()
        self.Plot3.show(1)

    def go_to_plot_2_from_plot_3(self):
        self.Plot3.close()
        self.Plot2.show(1)

    def go_to_plot_4_from_plot_3(self):
        self.Plot3.close()
        self.Plot4.show(1)

    def go_to_plot_3_from_plot_4(self):
        self.Plot4.close()
        self.Plot3.show(1)

    def go_to_plot_5_from_plot_4(self):
        self.Plot4.close()
        self.Plot5.show(1)

    def go_to_plot_4_from_plot_5(self):
        self.Plot5.close()
        self.Plot4.show(1)

    def reset_all_plots(self):
        self.Config.reset()
        self.Plot.reset_table()
        self.Plot.reset()
        self.Plot2.reset()
        self.Plot3.reset()
        self.Plot4.reset()
        self.Plot5.reset()
        self.inicializar_plots()

    def reset_all_data(self):
        self.data_instance.reset_all()
        self.reporter_instance.reset_reporter()
        self.temp=None
        self.grupos=None
        self.muestras=None
        self.espesor=None
        self.ft=None
        self.fh=None
        self.fc=None
        self.z=None
        self.calculos_flag=0
        self.datos_ready_flag=0
        self.set_data_ready(value=0)

    def set_reset(self,value):
        self.reset=value

    def get_reset(self):
        return self.reset
    
    def set_hora_inicio(self):
        self.hora_inicio=time.strftime("%H:%M", time.localtime())
        self.Plot.get_hora_label().config(text=f'Hora Inicio {self.hora_inicio}')
        self.Plot2.get_hora_label().config(text=f'Hora Inicio {self.hora_inicio}')
        self.Plot3.get_hora_label().config(text=f'Hora Inicio {self.hora_inicio}')
        self.Plot4.get_hora_label().config(text=f'Hora Inicio {self.hora_inicio}')
        self.Plot5.get_hora_label().config(text=f'Hora Inicio {self.hora_inicio}')

    def set_nro_puesto(self,nro_puesto):
        self.Plot.get_puesto_label().config(text=f'Nº Puesto:{nro_puesto}')
        self.Plot2.get_puesto_label().config(text=f'Nº Puesto:{nro_puesto}')
        self.Plot3.get_puesto_label().config(text=f'Nº Puesto:{nro_puesto}')
        self.Plot4.get_puesto_label().config(text=f'Nº Puesto:{nro_puesto}')
        self.Plot5.get_puesto_label().config(text=f'Nº Puesto:{nro_puesto}')
        self.nro_puesto=nro_puesto

    def download_pdf(self):
        #Genero los PDF en el orden que van en el informe
        self.generar_carátula("caratula.pdf")
        self.Plot5.download_stats()
        self.Plot.generar_pdf()
        numero_pagina=self.Plot.get_table().get_numero_pagina()
        self.Plot2.download_graphs()
        self.Plot3.download_graphs()
        self.Plot4.download_graphs(numero_pagina)
        sleep(1)
        self.combine_pdf(numero_pagina)

    def generar_carátula(self,filename):

            # Abrir el PDF existente en modo de escritura y agregar contenido
        c = canvas.Canvas(filename, pagesize=A4)
        ancho_pagina, alto_pagina = A4
        centro_x = ancho_pagina / 2
        # Dibuja la imagen en el PDF
        c.drawImage('caratula3.png', 70, 420, width=469, height=386)

        ruta = "Ruta: " + self.get_ruta()
        ancho_ruta = c.stringWidth(ruta, "Helvetica", 14)
        posicion_1 = centro_x - (ancho_ruta / 2)

        provincia = "Provincia: " + self.get_provincia()
        ancho_provincia = c.stringWidth(provincia, "Helvetica", 14)
        posicion_2 = centro_x - (ancho_provincia / 2)

        tramo ="Tramo: " + self.get_tramo()
        ancho_tramo = c.stringWidth(tramo, "Helvetica", 14)
        posicion_3 = centro_x - (ancho_tramo / 2)

        subtramo = "Subtramo: " + self.get_subtramo()
        ancho_subtramo = c.stringWidth(subtramo, "Helvetica", 14)
        posicion_4 = centro_x - (ancho_subtramo / 2)

        pavimento ="Pavimento: "+ self.get_pavimento()
        ancho_pavimento = c.stringWidth(pavimento, "Helvetica", 14)
        posicion_5 = centro_x - (ancho_pavimento / 2)

        puesto="Número de trayecto: "+str(self.reporter_instance.get_puesto())
        ancho_puesto = c.stringWidth(puesto, "Helvetica", 14)
        posicion_6 = centro_x - (ancho_puesto / 2)

        prog_max = "Progresiva final: "+str(self.Plot.get_prog_max())
        ancho_prog = c.stringWidth(prog_max, "Helvetica", 14)
        posicion_7 = centro_x - (ancho_prog / 2)

        prog_inicial = "Progresiva inicial: 0"
        ancho_prog_inicial = c.stringWidth(prog_inicial, "Helvetica", 14)
        posicion_15 = centro_x - (ancho_prog_inicial / 2)

        temperatura = "Temperatura [ºC]: "+str(self.get_temp())
        ancho_temp = c.stringWidth(temperatura, "Helvetica", 14)
        posicion_14 = centro_x - (ancho_temp / 2)

        fecha = "Fecha: "+str(datetime.datetime.now().date())
        ancho_fecha = c.stringWidth(fecha, "Helvetica", 12)
        posicion_8 = centro_x - (ancho_fecha / 2)

        hora_inicio="Inicio: "+ str(self.reporter_instance.get_initial_time())
        ancho_hora_inicio=c.stringWidth(hora_inicio, "Helvetica", 12)
        posicion_9=centro_x - (ancho_hora_inicio / 2)

        hora_final = datetime.datetime.now().strftime("%H:%M")
        hora, minutos = hora_final.split(":")
        hora = hora.zfill(2)
        minutos = minutos.zfill(2)
        hora_final_string = f"Fin: {hora}:{minutos}"
        ancho_hora_final=c.stringWidth(hora_final_string, "Helvetica", 12)
        posicion_10=centro_x - (ancho_hora_final / 2)

        chofer = "Chofer: "+self.get_chofer()
        ancho_chofer = c.stringWidth(chofer, "Helvetica", 12)
        posicion_11 = centro_x - (ancho_chofer / 2)

        apoyo = "Apoyo: "+self.get_apoyo()
        ancho_apoyo = c.stringWidth(apoyo, "Helvetica", 12)
        posicion_12 = centro_x - (ancho_apoyo / 2)

        operador = "Operador: "+self.get_operador()
        ancho_operador = c.stringWidth(operador, "Helvetica", 12)
        posicion_13 = centro_x - (ancho_operador / 2)

        c.setFont("Helvetica", 14)
        
        
        c.drawString(posicion_2, 340, f"{provincia}")
        c.drawString(posicion_3, 320, f"{tramo}")
        c.drawString(posicion_4, 300, f"{subtramo}")
        c.drawString(posicion_5, 280, f"{pavimento}")
        c.drawString(posicion_15, 260, f"{prog_inicial}")
        c.drawString(posicion_7, 240, f"{prog_max}")
        c.drawString(posicion_14, 220, f"{temperatura}")
        c.drawString(posicion_8, 190, f"{fecha}")
        c.drawString(posicion_9, 170, f"{hora_inicio}")
        c.drawString(posicion_10, 150, f"{hora_final_string}")
        c.drawString(posicion_11, 130, f"{chofer}")
        c.drawString(posicion_12, 110, f"{apoyo}")
        c.drawString(posicion_13, 90, f"{operador}")
        c.drawString(posicion_6, 70, f"{puesto}")

        c.save()
       

    def combine_pdf(self,numero_pagina):

        output1="pdf2.pdf"
        output2="pdf3.pdf"

        image_path='figure_rad_l.png'
        if os.path.exists(image_path): 

            ancho_pagina,alto_pagina=A4
            centro_x = ancho_pagina / 2
            c = canvas.Canvas(output1, pagesize=A4)
            c.drawImage('header2.png', 25, 773, width=575, height=60)
            c.drawImage('image.png', 0, 0, width=600, height=120)
            c.drawImage('figure_defl_mean_l.png',100, 200, width=383, height=230)
            c.drawImage('figure_rad_l.png', 100, 500,width=383, height=230)
            c.drawString(centro_x-1, 125, f"{numero_pagina+2}")
            c.save()

            c = canvas.Canvas(output2, pagesize=A4)
            c.drawImage('header2.png', 25, 773, width=575, height=60)
            c.drawImage('image.png', 0, 0, width=600, height=120)
            c.drawImage('figure_defl_mean_r.png', 100, 200, width=383, height=230)
            c.drawImage('figure_rad_r.png', 100, 500,width=383, height=230)
            c.drawString(centro_x-1, 125, f"{numero_pagina+3}")
            c.save()

            pdf_files = [
                "caratula.pdf",
                "stats.pdf",
                "tabla.pdf",    
                "defl_individuales.pdf",
                "pdf2.pdf",
                "pdf3.pdf",
                "radios.pdf"
            ]
            

            puesto = self.reporter_instance.get_puesto()
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H-%M")

            # Ruta absoluta para la carpeta "Informes" en el escritorio
            # informes_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Informes")

            # Nombre del archivo PDF completo
            # output_filename = os.path.join(informes_folder, f"{formatted_datetime}_puesto_{puesto}.pdf")
            output_filename = f"Informes/{formatted_datetime}_puesto_{puesto}.pdf"

            pdf_merger = PyPDF2.PdfMerger()
       
            for pdf_file in pdf_files:
                pdf_merger.append(pdf_file)
            
            
            with open(output_filename, "wb") as output_pdf:
                pdf_merger.write(output_pdf)
            
            pdf_merger.close()
            
            for pdf_file in pdf_files:
                os.remove(pdf_file)

            os.remove('figure_defl_mean_l.png')
            os.remove('figure_defl_mean_r.png')
            os.remove('figure_rad_r.png')
            os.remove('figure_rad_l.png')
            self.set_state('')
            messagebox.showinfo("Aviso","PDF generado en la carpeta 'Informes' del Escritorio.")

        else:
            # print("Detecto que la imagen no existe")
            messagebox.showwarning("Aviso","Faltan datos para generar el PDF.")
            return

# Metodo que obtiene los datos nuevos y debe mandar a actualizar los ploteos y las estructuras
    def new_group_data_view(self, dict_r, dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos):
        self.Plot.new_group_data_plot(dict_r, dict_l)
        self.Plot2.new_group_data_plot2(dict_r,dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos)
        self.Plot3.new_group_data_plot3(dict_r,dict_l, defl_r_car, defl_l_car, defl_r_max, defl_l_max,grupos)
        self.Plot4.new_group_data_plot4(dict_r, dict_l,grupos)

    # Metodo que manda a actualizar el gafico de barras 
    def update_bar_view(self, defl_r,defl_l):
        self.Plot.update_bar_plot(defl_r,defl_l)

    def show_stats_in_plot(self,media_defl_r, media_defl_izq,media_rad_der, media_rad_izq,desv_defl_der, desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq, d_r_der,d_r_izq ,d_x_r_der, d_x_r_izq, total_mediciones_defl, total_mediciones_rad):
        self.Plot5.grid_stats(media_defl_r, media_defl_izq,media_rad_der, media_rad_izq,desv_defl_der, desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq, d_r_der,d_r_izq ,d_x_r_der, d_x_r_izq, total_mediciones_defl, total_mediciones_rad)

    def get_config(self):
        return self.Config.get_config()

    def get_params(self):
        return self.Config.get_params()
    
    def on_plot(self):
        return self.is_plotting
    
    def obtain_values(self):
       return self.temp, self.grupos, self.muestras, self.espesor, self.ft_ntry, self.fh_ntry, self.fc_ntry, self.z_ntry

    def set_temp(self,temp):
        self.data_instance.set_temp(temp)
        self.temp=temp

    def get_temp(self):
        return self.temp

    def set_grupos(self,grupos):
        self.grupos=grupos
        self.data_instance.set_grupos(grupos)
        
    def get_grupos(self):
        return self.grupos

    def set_muestras(self,muestras):
        self.muestras=muestras

    def get_muestras(self):
        return self.muestras

    def set_espesor(self,espesor):
        self.data_instance.set_espesor(espesor)
        self.espesor=espesor

    def get_espesor(self):
        return self.espesor

    def set_ft(self,ft):
        self.data_instance.set_ft(ft)
        self.ft_ntry=ft

    def get_ft(self):
        return self.ft_ntry

    def set_fh(self,fh):
        self.data_instance.set_fh(fh)
        self.fh_ntry=fh

    def get_fh(self):
        return self.fh_ntry

    def set_fc(self,fc):
        self.data_instance.set_fc(fc)
        self.fc_ntry=fc

    def get_fc(self):
        return self.fc_ntry
    
    def set_z(self,z):
        self.data_instance.set_z(z)
        self.z_ntry=z 

    def get_z(self):
        return self.z_ntry
    
    def set_data_ready(self,value):
        self.data_ready=value

    def get_data_ready(self):
        return self.data_ready
    
    def set_ruta(self,ruta):
        self.Plot5.set_ruta(ruta)
        self.Plot.set_ruta(ruta)
        self.ruta_ntry=ruta

    def get_ruta(self):
        return self.ruta_ntry
    
    def set_provincia(self,provincia):
        self.provincia_ntry=provincia

    def get_provincia(self):
        return self.provincia_ntry
    
    def set_tramo(self,tramo):
        self.tramo_ntry=tramo

    def get_tramo(self):
        return self.tramo_ntry
    
    def set_subtramo(self,subtramo):
        self.subtramo_ntry=subtramo

    def get_subtramo(self):
        return self.subtramo_ntry
    
    def set_pavimento(self,pavimento):
        self.pavimento_ntry=pavimento

    def get_pavimento(self):
        return self.pavimento_ntry
    
    def set_chofer(self,chofer):
        self.chofer_ntry=chofer

    def get_chofer(self):
        return self.chofer_ntry
    
    def set_operador(self,operador):
        self.operador_ntry=operador

    def get_operador(self):
        return self.operador_ntry
    
    def set_apoyo(self,apoyo):
        self.apoyo_ntry=apoyo

    def get_apoyo(self):
        return self.apoyo_ntry

    def get_state(self):
        return self.program_state
    
    def set_state(self,state):
        if(self.get_reset()!=1):
            if(state=="Detenido"):
                self.set_data_ready(0)
            print("View State:",state)
            self.program_state=state
            self.Plot.get_state_label().config(text=f'{state}')
            self.Plot2.get_state_label().config(text=f'{state}')
            self.Plot3.get_state_label().config(text=f'{state}')
            self.Plot4.get_state_label().config(text=f'{state}')
            self.Plot5.get_state_label().config(text=f'{state}')
        else:
            return
        
    def set_calculos_flag(self,flag):
        self.calculos_flag=flag

    def set_datos_ready_flag(self,flag):
        self.datos_ready_flag=flag

    def get_calculos_flag(self):
        return self.calculos_flag

    def interface_transition_function(self):
            while True:

                # self.actualizar_estado()
                # Utilizar una cola bloqueante para esperar a que se solicite una función de transición
                target_function = self.interface_transition_queue.get()

                # Ejecutar la función de transición de interfaz correspondiente
                if target_function == 'go_to_config':
                    # if(self.get_state()=='Obteniendo datos'):
                    respuesta= messagebox.askokcancel("Aviso","Si vuelve a la configuración deberá resetear el recorrido. ¿Desea continuar?")
                    if respuesta:
                        reset_message = tk.Toplevel(self.root)
                        
                        reset_message.title("Reset Info")
                        message_label = tk.Label(reset_message, text="Reseteando. Por favor espere...",font=(None,10))
                        message_label.pack()
                        reset_message.geometry(f"200x100")
                        self.set_reset(1)
                        self.go_to_config()
                        self.reset_all_data()
                        self.reset_all_plots()
                        reset_message.destroy()
                        # messagebox.showinfo("Aviso", "Datos reseteados!")
                        self.set_reset(0)
                        self.enqueued_functions.remove(target_function)
                        self.interface_transition_queue.task_done()
                        # continue
                    else:
                        self.enqueued_functions.remove(target_function)
                        self.interface_transition_queue.task_done()
                        # continue
                    # self.go_to_config()
                    # self.enqueued_functions.remove(target_function)
                    # self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_1_from_config':
                    if(self.get_data_ready()==1):
                        messagebox.showwarning("Aviso","Debe resetear los datos antes de intentar modificarlos")
                        # self.interface_transition_queue.task_done()
                        # self.enqueued_functions.remove(target_function)
                        # continue

                    self.go_to_plot1_from_config()
               
                    self.enqueued_functions.remove(target_function)

                
                    self.interface_transition_queue.task_done()
                    data_thread = Thread(target=self.process_data)
                    data_thread.daemon = True
                    data_thread.start()
                    print("RETORNO ACÁ")

                elif target_function == 'go_to_plot_2_from_plot_1':
                    self.go_to_plot_2_from_plot_1()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()
                
                elif target_function == 'go_to_plot_1_from_plot_2':
                    self.go_to_plot_1_from_plot_2()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_3_from_plot_2':
                    self.go_to_plot_3_from_plot2()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                # Agregar más casos para otras funciones de transición...
                elif target_function == 'go_to_plot_2_from_plot_3':
                    self.go_to_plot_2_from_plot_3()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_4_from_plot_3':
                    self.go_to_plot_4_from_plot_3()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_3_from_plot_4':
                    self.go_to_plot_3_from_plot_4()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_5_from_plot_4':
                    self.go_to_plot_5_from_plot_4()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'go_to_plot_4_from_plot_5':
                    self.go_to_plot_4_from_plot_5()
                    self.enqueued_functions.remove(target_function)
                    self.interface_transition_queue.task_done()

                elif target_function == 'reset_all_plots':
                    reset_message = tk.Toplevel(self.root)
                        
                    reset_message.title("Reset Info")
                    message_label = tk.Label(reset_message, text="Reseteando. Por favor espere...",font=(None,10))
                    message_label.pack()
                    reset_message.geometry(f"200x100")
                    print("Ejecuto reset")
                    self.set_reset(1)
                    self.reset_all_plots()
                    self.reset_all_data()
                    # messagebox.showinfo("Aviso", "Datos reseteados!")
                    self.set_reset(0)
                    reset_message.destroy()
                    self.interface_transition_queue.task_done()
                    self.enqueued_functions.remove(target_function)

                elif target_function == 'generate_stats':

                    media_defl_r, media_defl_izq,media_rad_der, media_rad_izq,desv_defl_der, desv_defl_l,coef_var_der,coef_var_izq,defl_car_der,defl_car_izq,rad_car_der,rad_car_izq, d_r_der,d_r_izq ,d_x_r_der, d_x_r_izq, total_mediciones_defl, total_mediciones_rad =self.data_instance.calculate_stats()
                    
                    if(media_defl_r==0):
                        messagebox.showwarning("Aviso","No hay datos para calcular.")
                        self.set_state('')
                        self.set_calculos_flag(0)
                        self.interface_transition_queue.task_done()
                        self.enqueued_functions.remove(target_function)
                        continue

                    self.show_stats_in_plot(
                        media_defl_r, media_defl_izq,media_rad_der, media_rad_izq,
                        desv_defl_der, desv_defl_l,coef_var_der,coef_var_izq,
                        defl_car_der,defl_car_izq ,rad_car_der, rad_car_izq,
                        d_r_der,d_r_izq,
                        d_x_r_der, d_x_r_izq, 
                        total_mediciones_defl, total_mediciones_rad
                    )
                    self.set_state('Cálculos generados.')
                    self.interface_transition_queue.task_done()
                    self.enqueued_functions.remove(target_function)
                    # self.set_data_ready(value=0)
                
                elif target_function=='download_pdf':
                    if(self.get_calculos_flag()!=1):
                        messagebox.showwarning("Aviso","Se deben generar los cálculos para descargar el PDF.")
                        self.interface_transition_queue.task_done()
                        self.enqueued_functions.remove(target_function)
                        # continue
                    else:
                        self.set_state("Generando PDF.")
                        self.download_pdf()
                        self.interface_transition_queue.task_done()
                        self.enqueued_functions.remove(target_function)

                elif target_function=='show_configuration':
                    ventana_emergente = tk.Toplevel(self.root)
                    ventana_emergente.title("Configuración")

                    # Agregar contenido a la ventana emergente
                    temperatura="Temperatura: " + str(self.get_temp())
                    grupos= "Grupos: " + str(self.get_grupos())
                    espesor= "Espesor: "+ str(self.get_espesor())
                    ft="Ft: " + str(self.get_ft()) 
                    fh ="Fh: " + str(self.get_fh())
                    fc ="Fc: " + str(self.get_fc())
                    z ="Z: " + str(self.get_z())
                    etiqueta = ttk.Label(ventana_emergente, text=temperatura)
                    etiqueta.pack(padx=10, pady=10)
                    etiqueta2 = ttk.Label(ventana_emergente, text=grupos)
                    etiqueta2.pack(padx=10, pady=10)
                    etiqueta3 = ttk.Label(ventana_emergente, text=espesor)
                    etiqueta3.pack(padx=10, pady=10)
                    etiqueta4 = ttk.Label(ventana_emergente, text=ft)
                    etiqueta4.pack(padx=10, pady=10)
                    etiqueta5 = ttk.Label(ventana_emergente, text=fh)
                    etiqueta5.pack(padx=10, pady=10)
                    etiqueta6 = ttk.Label(ventana_emergente, text=fc)
                    etiqueta6.pack(padx=10, pady=10)
                    etiqueta7 = ttk.Label(ventana_emergente, text=z)
                    etiqueta7.pack(padx=10, pady=10)
                    self.interface_transition_queue.task_done()
                    self.enqueued_functions.remove(target_function)



    def enqueue_transition(self, function_name):
        # self.interface_transition_queue.put(function_name)
        if function_name not in self.enqueued_functions:
            self.interface_transition_queue.put(function_name)
            self.enqueued_functions.add(function_name)


    def update_all(self):
        self.data_instance.update_structures()
        dict_r, dict_l = self.data_instance.get_data_dict()
        defl_l_max, defl_r_max = self.data_instance.get_max_defl()
        defl_l_car, defl_r_car = self.data_instance.get_car_defl()
        self.new_group_data_view(dict_r,dict_l,defl_r_car,defl_l_car,defl_r_max,defl_l_max,grupos=self.grupos)

    def update_defl_one(self):
        defl_r, defl_l = self.data_instance.update_bar_data(self.amount)
        self.update_bar_view(defl_r,defl_l)
        self.data_instance.clear_bar_data()

    def process_data(self):
        self.set_state("Listo para obtener datos")
        self.reporter_instance.start()
        grupos=self.get_grupos()
        muestras=self.get_muestras()
        a=0
        b=0

        c=0
        print("C value:",c)

        while True:
                
            data, this_cycle = self.reporter_instance.get_new_measurements()
            
            if data is None or this_cycle is None:

                if(self.reporter_instance.get_puesto_change()==1):
                    messagebox.showinfo("Aviso","Cambio de Puesto detectado. Se mostrarán los resultados estadísticos.")
                    # self.set_state("Cambio de puesto")
                    self.enqueue_transition('generate_stats')
                    return

                elif(a==muestras):
                    messagebox.showinfo("Aviso","Cantidad de muestras alcanzada.")
                    self.set_state("Detenido")
                    return
                
                elif(self.get_reset()==1):
                        print("Identifico reset")
                        self.set_state("Deteniendo...")
                        self.set_reset(1)
                        print("Vuelvo a empezar")
                        return
                else:
                    continue

            # if(self.get_state()!="Detenido"):
            if(c==0):
                c=1
                self.amount=1
                print("Seteo cosas")
                
                self.set_hora_inicio()
                self.set_nro_puesto(self.reporter_instance.get_last_puesto())

            self.set_state("Obteniendo datos")
            self.data_instance.data_destruct(data)
            cantidad=self.data_instance.cant_mediciones()
            a=a+1
            print(cantidad)
            
            if(self.reporter_instance.get_puesto_change()==0):
                if(a>=100):
                    self.amount=10
                    b=b+1
                    if(b==10):
                        b=0
                        print("Grafico barras")
                        # update_bar_thread = Thread(target=self.update_defl_one,args=(self,10))
                        update_bar_thread = Thread(target=self.update_defl_one)
                        update_bar_thread.daemon=True
                        update_bar_thread.start()
                else:
                    # View.set_state("Grafico barras")
                    print("Grafico barras")
                    # update_bar_thread = Thread(target=self.update_defl_one,args=(self,1))
                    update_bar_thread = Thread(target=self.update_defl_one)
                    update_bar_thread.daemon=True
                    update_bar_thread.start()
                
                if(cantidad%5 == 0):
                    print("Grafico grupos")
                    update_all_thread = Thread(target=self.update_all)
                    update_all_thread.daemon=True 
                    update_all_thread.start()










     
    