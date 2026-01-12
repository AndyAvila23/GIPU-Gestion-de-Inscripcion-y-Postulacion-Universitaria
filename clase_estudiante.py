import tkinter as tk
from tkinter import messagebox
import os, json
class estudiante_aspirante:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Postulación e Inscripción Universitaria")
        self.root.geometry("800x550")
        # Centrar ventana principal
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Menú principal con solo los botones solicitados
        menu = tk.Frame(root)
        menu.pack(pady=50)

        tk.Button(menu, text="Crear Postulación", font=("Arial", 12), width=25, command=self.crear_postulacion).pack(pady=10)
        tk.Button(menu, text="Verificar Registro Único", font=("Arial", 12), width=25, command=self.verificar_registro).pack(pady=10)
        tk.Button(menu, text="Salir", font=("Arial", 12), width=25, command=self.root.destroy).pack(pady=10)

    def crear_postulacion(self):
        ventana_postulacion = tk.Toplevel(self.root)
        ventana_postulacion.title("Crear Postulación")
        ventana_postulacion.geometry("400x400")
  
  
        ventana_postulacion.update_idletasks()
        w = ventana_postulacion.winfo_width()
        h = ventana_postulacion.winfo_height()
        xs = (ventana_postulacion.winfo_screenwidth() // 2) - (w // 2)
        ys = (ventana_postulacion.winfo_screenheight() // 2) - (h // 2)
        ventana_postulacion.geometry(f"{w}x{h}+{xs}+{ys}")

        tk.Label(ventana_postulacion, text="Seleccione el Periodo:").pack(pady=5)
        periodo_var = tk.StringVar(value="2025 - Primer Semestre")
        tk.OptionMenu(ventana_postulacion, periodo_var, "2025 -1", "2025 - 2").pack()

        tk.Label(ventana_postulacion, text="Número de Postulación:").pack(pady=5)
        numero_postulacion = tk.Entry(ventana_postulacion)
        numero_postulacion.pack()

        tk.Label(ventana_postulacion, text="Seleccione la Carrera:").pack(pady=5)
        carrera_var = tk.StringVar(value="Ingeniería en Sistemas")
        tk.OptionMenu(ventana_postulacion, carrera_var, "Ingeniería en Sistemas", "Medicina", "Derecho", "Administración de Empresas").pack()

        tk.Label(ventana_postulacion, text="Seleccione la Sede:").pack(pady=5)
        sede_var = tk.StringVar(value="Quito")
        tk.OptionMenu(ventana_postulacion, sede_var, "Quito", "Guayaquil", "Cuenca").pack()

        tk.Button(ventana_postulacion, text="Guardar", command=lambda: self.guardar_postulacion(periodo_var.get(), numero_postulacion.get(), carrera_var.get(), sede_var.get(), ventana_postulacion)).pack(pady=20)

    def guardar_postulacion(self, periodo, numero, carrera, sede, ventana):
        data = {
            "periodo": periodo,
            "numero_postulacion": numero,
            "carrera": carrera,
            "sede": sede
        }
        with open("data/postulacion.json", "a", encoding='utf-8') as file:
            file.write(json.dumps(data) + "\n")
        messagebox.showinfo("Postulación", "La postulación se ha guardado correctamente")
        ventana.destroy()

    def verificar_registro(self):
        messagebox.showinfo("Verificar Registro", "En proceso")