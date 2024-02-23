import tkinter as tk

def show_reset_message():
    reset_message = tk.Toplevel(root)
    reset_message.title("Reseteando")
    message_label = tk.Label(reset_message, text="Reseteando. Por favor espere...")
    message_label.pack()
    
    # Cerrar el cuadro de diálogo después de 3 segundos (3000 milisegundos)
    root.after(3000, reset_message.destroy)

def reset_widgets():
    # Coloca aquí tu lógica de reseteo
    # ...

    # Llamar a la función para mostrar el mensaje de reseteo
    show_reset_message()

root = tk.Tk()
root.title("Ejemplo de Mensaje Emergente")

reset_button = tk.Button(root, text="Resetear", command=reset_widgets)
reset_button.pack()

root.mainloop()
