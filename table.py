from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
from tabulate import tabulate
from fpdf import FPDF
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
# Clase donde se inicializa y actualiza la tabla

class Tabla():
    def __init__(self, frame):
        self.table = None
        self.frame=frame
        self.show(frame)
        self.original_table_height = None
        self.grupos=None
        self.fecha=None
        self.ruta=None
        self.num_pagina=2
        self.doble_pagina=False

    # Metodo que inserta valores en el diccionario
    # TODO -> Falta compensar los valores con respecto a la temperatura
    def insert(self, dict_r, dict_l):

        last_index_r = dict_r['Grupo'][len(dict_r['Grupo'])-1] # ultimo valor del array
        last_defl_mean_r = dict_r['Defl.'][len(dict_r['Defl.'])-1] # ultimo valor del array
        last_radio_mean_r = dict_r['Radio'][len(dict_r['Radio'])-1] # ultimo valor del array
        last_rd_r = dict_r['R*D'][len(dict_r['R*D'])-1] # ultimo valor del array
        last_r_d_r = dict_r['D/R'][len(dict_r['D/R'])-1] # ultimo valor del array

        last_index_l = dict_l['Grupo'][len(dict_l['Grupo'])-1] # ultimo valor del array
        last_defl_mean_l = dict_l['Defl.'][len(dict_l['Defl.'])-1] # ultimo valor del array
        last_radio_mean_l = dict_l['Radio'][len(dict_l['Radio'])-1] # ultimo valor del array
        last_rd_l = dict_l['R*D'][len(dict_l['R*D'])-1] # ultimo valor del array
        last_r_d_l = dict_l['D/R'][len(dict_l['D/R'])-1] # ultimo valor del array


        self.table.insert('', END, values = (
            last_index_r,
            last_radio_mean_r, 
            last_defl_mean_r,
            last_rd_r, 
            last_r_d_r, 
            # last_index_l,
            last_radio_mean_l,
            last_defl_mean_l, 
            last_rd_l, 
            last_r_d_l
            )) 

    def show(self,frame):
        columns = ("Grupos", "Radio.", "Defl.", "R*D.", "R/D.", ".Radio.", ".Defl.", ".R*D.", ".R/D.")

        # Crear el Treeview
        self.table = Treeview(self.frame, columns=columns, show='headings')
        self.table.grid(row=2, column=0, columnspan=2, pady=0)

        # Configurar el alto del Treeview
        self.table.configure(height=9)
        
        headers = [
            ("Grupos", "Grupos"),
            ("Radio.", "Radio"),
            ("Defl.", "Defl."),
            ("R*D.", "R*D"),
            ("R/D.", "D/R"),
            (".Radio.", "Radio"),
            (".Defl.", "Defl."),
            (".R*D.", "R*D"),
            (".R/D.", "D/R")
        ]
        for column, header in headers:
            self.table.heading(column, text=header)
            self.table.column(column, anchor=CENTER, width=110)

    def clear_table(self):
        # Elimina todos los elementos de la tabla
        self.table.delete(*self.table.get_children())

    def get_doble_pagina(self):
        return self.doble_pagina
    
    def get_numero_pagina(self):
        return int(self.num_pagina)
    def donwload_table(self):
        
        buffer = BytesIO()


        c = canvas.Canvas(buffer, pagesize=A4)
        ancho_pagina,alto_pagina=A4
        centro_x = ancho_pagina / 2
    
        titulo_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),  # Fondo para todas las filas
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),   # Color de texto para todas las filas
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        titulo_der,titulo_izq="Huella Externa (DER)","Huella Interna (IZQ)"
        tabla_titulo = Table([[titulo_der,titulo_izq]],colWidths=[200,200])
        tabla_titulo.setStyle(titulo_style)
        tabla_titulo.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
        tabla_titulo.drawOn(c, 125, 735) 

        h1,h2,h3,h4,h5,h6,h7,h8,h9="Grupos", "Radio.", "Defl.", "R*D.", "R/D.", ".Radio.", ".Defl.", ".R*D.", ".R/D."
        tabla_headers = Table([[h1,h2,h3,h4,h5,h6,h7,h8,h9]],colWidths=[50,50,50,50,50,50,50,50,50])
        tabla_headers.setStyle(titulo_style)
        tabla_headers.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
        tabla_headers.drawOn(c, 75, 710)

        datos = []
        for item in self.table.get_children():
                datos.append(self.table.item(item, 'values'))

        altura_maxima = 660
        altura_tabla = 20 * len(datos)
        # print("Altura tabla:",altura_tabla)
        num_filas_por_pagina = 33  # Número de filas por página
        pagina_actual = 1
      
        altura_restante=altura_tabla
        filas_totales=int(altura_tabla/20)
        
        print("Filas totales:",filas_totales)

        while(altura_restante>=altura_maxima):

            c.drawString(centro_x-1, 25, f"{self.num_pagina}")
            c.drawImage('header.png', 25, 773, width=550, height=60)
            datos_pagina = datos[:num_filas_por_pagina]
            datos = datos[num_filas_por_pagina:]
            tabla_datos_pagina = Table(datos_pagina, colWidths=[50,50,50,50,50,50,50,50,50],rowHeights=20)
            tabla_datos_pagina.setStyle(table_style)
            tabla_datos_pagina.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
            tabla_datos_pagina.drawOn(c, 75, 705-(20*num_filas_por_pagina))
            c.showPage()
            # c.save()
            filas_totales=filas_totales-num_filas_por_pagina
            altura_restante=altura_restante-altura_maxima
            self.num_pagina+=1

        datos_pagina_final=datos[:filas_totales]
        datos=datos[filas_totales:]
        tabla_final = Table(datos_pagina_final, colWidths=[50,50,50,50,50,50,50,50,50],rowHeights=20)
        tabla_final.setStyle(table_style)
        tabla_final.wrapOn(c, 400, 200)  # Ajusta el tamaño de la tabla si es necesario
        tabla_final.drawOn(c, 75, 705-(20*filas_totales))
        c.drawString(centro_x-1, 25, f"{self.num_pagina}")
        c.drawImage('header.png', 25, 773, width=550, height=60)
        c.showPage()
        c.save()


        # Guardar el contenido del buffer en un archivo PDF
        buffer.seek(0)
        with open('tabla.pdf', 'wb') as f:
            f.write(buffer.read())
     
        
        
        
    def reset(self):
        self.clear_table()
        self.show(self)

    def set_fecha(self,fecha):
        self.fecha=fecha

    def get_fecha(self):
        return self.fecha
    
    def set_ruta(self,ruta):
        self.ruta=ruta

    def get_ruta(self):
        return self.ruta
