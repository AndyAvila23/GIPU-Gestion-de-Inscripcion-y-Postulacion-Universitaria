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
        """Muestra la ventana para recuperar contraseña"""
        # Crear ventana de recuperación de contraseña
        ventana_recuperar = tk.Toplevel(self)
        ventana_recuperar.title("Recuperar Contraseña")
        ventana_recuperar.geometry("400x350")  # Aumenté un poco la altura
        ventana_recuperar.config(bg="#f0f0f0")
        ventana_recuperar.transient(self)
        ventana_recuperar.grab_set()
        ventana_recuperar.resizable(False, False)
        
        # Centrar ventana
        ancho = 400
        alto = 350
        pantalla_ancho = ventana_recuperar.winfo_screenwidth()
        pantalla_alto = ventana_recuperar.winfo_screenheight()
        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2
        ventana_recuperar.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Frame principal con fondo blanco
        main_frame = tk.Frame(ventana_recuperar, bg="white", padx=20, pady=15)
        main_frame.pack(expand=True, fill="both", padx=1, pady=1)
        
        # Título
        tk.Label(main_frame, text="Recuperar Contraseña", 
                font=("Arial", 18, "bold"), 
                fg="#2a4f80",
                bg="white").pack(pady=(0, 15))
        
        # Frame para los campos de entrada (más compacto)
        campos_frame = tk.Frame(main_frame, bg="white")
        campos_frame.pack(fill="x", pady=(0, 10))
        
        # Campo de correo
        tk.Label(campos_frame, text="Correo Electrónico:", 
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#333333").pack(anchor="w", pady=(0, 5))
        
        correo_entry = tk.Entry(campos_frame, width=38, font=("Arial", 11), 
                            relief="solid", borderwidth=1)
        correo_entry.pack(fill="x", pady=(0, 10), ipady=4)
        
        # Campo de identificación
        tk.Label(campos_frame, text="Número de Identificación:", 
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#333333").pack(anchor="w", pady=(0, 5))
        
        identificacion_entry = tk.Entry(campos_frame, width=38, font=("Arial", 11),
                                    relief="solid", borderwidth=1)
        identificacion_entry.pack(fill="x", pady=(0, 15), ipady=4)
        
        # Frame para mensaje con fondo blanco (más compacto)
        mensaje_frame = tk.Frame(main_frame, bg="white", height=50)
        mensaje_frame.pack(fill="x", pady=(5, 10))
        mensaje_frame.pack_propagate(False)  # Mantener altura fija
        
        mensaje_label = tk.Label(mensaje_frame, text="", 
                                font=("Arial", 10),
                                bg="white",
                                fg="red",
                                justify="left",
                                wraplength=350)
        mensaje_label.pack(anchor="w", pady=5)
        
        # Frame para botones con fondo blanco - EN UNA POSICIÓN MÁS ALTA
        botones_frame = tk.Frame(main_frame, bg="white")
        botones_frame.pack(fill="x", pady=(10, 0))  # Menos padding arriba
        
        # Botón Cancelar
        btn_cancelar = tk.Button(botones_frame, text="Cancelar", 
                                width=14,
                                font=("Arial", 11),
                                bg="#cca14c",
                                fg="#ffffff",
                                relief="solid",
                                borderwidth=1,
                                padx=10,
                                command=ventana_recuperar.destroy)
        btn_cancelar.pack(side="left", padx=(0, 5))  # Menos espacio entre botones
        
        # Espaciador para empujar botones
        tk.Frame(botones_frame, bg="white", width=20).pack(side="left", expand=True)
        
        # Botón Recuperar Contraseña
        btn_recuperar = tk.Button(botones_frame, text="Recuperar", 
                                width=14,
                                font=("Arial", 11),
                                bg="#cca14c",
                                fg="white",
                                relief="solid",
                                borderwidth=1,
                                padx=10,
                                command=lambda: self._verificar_datos_recuperacion(
                                    correo_entry.get().strip(),
                                    identificacion_entry.get().strip(),
                                    mensaje_label,
                                    ventana_recuperar
                                ))
        btn_recuperar.pack(side="right", padx=(5, 0))
        
        # Enfocar el primer campo
        correo_entry.focus_set()

    def _verificar_datos_recuperacion(self, correo, identificacion, mensaje_label, ventana_recuperar):
        """Verifica los datos ingresados y muestra la contraseña"""
        if not correo or not identificacion:
            mensaje_label.config(text="Por favor complete todos los campos", 
                                fg="red", bg="white")
            return
        
        # Verificar en el archivo de usuarios
        usuarios_path = os.path.join("data", "registros", "usuarios_registrados.csv")
        
        if not os.path.exists(usuarios_path):
            mensaje_label.config(text="No hay usuarios registrados en el sistema", 
                                fg="red", bg="white")
            return
        
        try:
            with open(usuarios_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # Leer encabezados
                
                if headers is None or len(headers) < 6:
                    mensaje_label.config(text="Formato de archivo incorrecto", 
                                        fg="red", bg="white")
                    return
                
                for row in reader:
                    if len(row) >= 6:
                        # Verificar si el correo y la identificación coinciden
                        # row[2] = correo, row[1] = identificacion
                        if row[2] == correo and row[1] == identificacion:
                            # Mostrar la contraseña encontrada
                            contraseña = row[5]
                            mensaje_label.config(
                                text=f"Contraseña: {contraseña}\nNombres: {row[3]} {row[4]}",
                                fg="green",
                                bg="white",
                                font=("Arial", 10, "bold")
                            )
                            return
                
            # Si no se encontró el usuario
            mensaje_label.config(text="No se encontró un usuario con esos datos", 
                                fg="red", bg="white")
            
        except Exception as e:
            mensaje_label.config(text=f"Error al leer el archivo: {str(e)}", 
                                fg="red", bg="white")

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

        try:
            # 1. Verificar si es administrador del sistema
            if correo == "admin@system.com" and contraseña == "admin":
                parent_window = self.parent
                self.destroy()
                if parent_window and parent_window.winfo_exists():
                    parent_window.destroy()
                AdminVentana()
                return
            
            # 2. Verificar si es administrador regular usando GestorAdministradores
            from controls.usuarios.Administrador import GestorAdministradores
            
            gestor_admin = GestorAdministradores()
            es_admin, admin = gestor_admin.verificar_credenciales(correo, contraseña)
            
            if es_admin:
                parent_window = self.parent
                self.destroy()
                if parent_window and parent_window.winfo_exists():
                    parent_window.destroy()
                AdminVentana()
                return
            
            # 3. Verificar si es estudiante usando la clase Estudiante
            from controls.usuarios.Estudiantes import Estudiante
            
            es_estudiante, datos_estudiante = Estudiante.verificar_credenciales(correo, contraseña)
            
            if es_estudiante:
                # Login exitoso para estudiante
                parent_window = self.parent
                self.destroy()
                if parent_window and parent_window.winfo_exists():
                    parent_window.destroy()
                Ventana_Principal()
                return
            
            # 4. Si ninguna validación funciona, mostrar error
            messagebox.showerror("Acceso denegado", "Correo o contraseña incorrectos")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar credenciales: {str(e)}")