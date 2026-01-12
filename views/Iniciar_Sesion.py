import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from tkinter import *
from views.admin.Admin_menu import AdminVentana
from views.Menu_Principal import Ventana_Principal
import json, os, csv

class inicio_sesion (tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent
        self.transient(parent)
        self.logo = None
        self._crear_contenido()
        self.after(100, self._posicionar_a_derecha)
        self.grab_set()
        self.focus_set()
        self.title("GIPU - Iniciar Sesion")

        # Dimensiones centradas en pantalla
        self.ancho = 400
        self.alto = 550
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#f0f0f0")
        self._configurar_estilos()

    # ─────────────────────────────
    # Posicionar ventana
    # ─────────────────────────────
    def _centrar_ventana(self):
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho - self.ancho) // 2
        y = (pantalla_alto - self.alto) // 2
        self.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")

    # ─────────────────────────────
    # Configuracion de estilos base
    # ─────────────────────────────
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Arial", 11), padding=5, background="#cca14c")
        estilo.configure("TLabel", font=("Arial", 11), background = "#ffffff")
        estilo.configure("TFrame", background="#ffffff")
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", False)
        self.resizable(False, False)

    def _crear_contenido(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(expand=True, fill="both")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        encabezado = ttk.Frame(frame)
        encabezado.pack(fill="x", pady=10)

        # ─────────────────────────────
        # CUERPO PRINCIPAL
        # ─────────────────────────────
        cuerpo = ttk.Frame(frame)
        cuerpo.pack(fill="y", pady=10)

        # ─────────────────────────────
        # FINAL
        # ─────────────────────────────
        final = ttk.Frame(frame)
        final.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(4, 4)
            logo_label = ttk.Label(encabezado, image=self.logo)
        logo_label.pack(side="top", padx=(15, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(encabezado)
        titulo_frame.pack(side="top", anchor="center", pady=10)
        #ttk.Label(titulo_frame, text="GIPU", font=("Arial", 32, "bold")).pack(anchor="center")
        ttk.Label(titulo_frame, text="Iniciar Sesión", font=("Arial", 22, "bold"), foreground="#2a4f80").pack(anchor="center")

        # Entradas y etiquetas del sistema
        correo_frame = ttk.Frame(cuerpo)
        correo_frame.pack(side="top", anchor="center", pady= 10)
        ttk.Label(correo_frame, text="Correo electronico: ", font=("Arial", 16)).pack(anchor="w")
        self.correo = ttk.Entry(correo_frame, width=50, font=("Arial", 12))
        self.correo.pack(anchor="w")

        contraseña_frame = ttk.Frame(cuerpo)
        contraseña_frame.pack(side="bottom", anchor="center", pady= 10)
        ttk.Label(contraseña_frame, text="Contraseña: ", font=("Arial", 16)).pack(anchor="w")
        self.contraseña = ttk.Entry(contraseña_frame, width=50, font=("Arial", 12), show="*")
        self.contraseña.pack(anchor="w")

        self.recuperar_contra = ttk.Label(contraseña_frame, text="Recuperar Contraseña", font=("Arial", 11), foreground= "Blue", cursor="hand2")
        self.recuperar_contra.pack(side="left", anchor="w", pady=(5,0))
        self.recuperar_contra.bind("<Button-1>", self._recuperar_contraseña)
        self.mostrar_contra= ttk.Label(contraseña_frame, text="Mostrar Contraseña", font=("Arial", 11), foreground= "Blue", cursor="hand2")
        self.mostrar_contra.pack(side="right", anchor="e", pady=(5,0))
        self.mostrar_contra.bind("<Button-1>", self._mostrar_contraseña)

        # Botones de acción
        botones_frame = ttk.Frame(final)
        botones_frame.pack(side="bottom",anchor="s", padx=10)
        ttk.Button(botones_frame, text="Cancelar", width=15, command= self.destroy).pack(side="left", padx=5)
        ttk.Button(botones_frame, text="Aceptar", width=15, command= self._aceptar).pack(side="left", padx=5)

    def _posicionar_a_derecha(self):
        if self.master:
            self.master.update_idletasks()
            master_x = self.master.winfo_x()
            master_y = self.master.winfo_y()
            master_w = self.master.winfo_width()
            master_h = self.master.winfo_height()

            # Dimensiones propias
            self.update_idletasks()
            w = self.winfo_width()
            h = self.winfo_height()

            # Calcular posición a la derecha
            x = master_x + master_w
            y = master_y

            # Mostrar en la posición calculada
            self.geometry(f"{w}x{h}+{x+10}+{y+25}")

    def _recuperar_contraseña(self, event=None):
        messagebox.showinfo("Rcuperar contraseña", "Aquí se abrirá la ventana de recuperación de contraseña")

    def _mostrar_contraseña(self, event=None):
        if self.contraseña.cget("show") == "":
            self.contraseña.config(show="*")
            self.mostrar_contra.config(text="Mostrar Contraseña")
        else:
            self.contraseña.config(show="")
            self.mostrar_contra.config(text="Ocultar Contraseña")

    def _aceptar(self, parent=None, event=None):
        correo = self.correo.get().strip()
        contraseña = self.contraseña.get().strip()

        if not correo or not contraseña:
                messagebox.showerror("Error", "Debe ingresar correo y contraseña")
                return
        
        if correo == "admin@system.com" and contraseña == "admin":
            parent_window = self.parent
            # Destruir esta ventana primero
            self.destroy()
            # Luego destruir el menú inicio si existe
            if parent_window and parent_window.winfo_exists():
                parent_window.destroy()
            AdminVentana()
        elif correo == "." and contraseña == ".":
            parent_window = self.parent
            # Destruir esta ventana primero
            self.destroy()
            # Luego destruir el menú inicio si existe
            if parent_window and parent_window.winfo_exists():
                parent_window.destroy()
            Ventana_Principal()
        else:
            messagebox.showerror("Acceso denegado", "Correo o contraseña incorrectos")