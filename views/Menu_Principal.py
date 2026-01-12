import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk, filedialog
from tkinter import *
from datetime import datetime
import os, json, csv

class Ventana_Principal(tk.Tk):
    def __init__(self, parent= None, iconos=None):
        super().__init__()
        self.logo = None
        self._crear_contenido()
        self.title("GIPU - Menu Principal")

    # Dimensiones centradas en pantalla
        self.ancho = 900
        self.alto = 600
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#2a4f80")
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
        # Frame principal
        frame_borde_azul = tk.Frame(self, bg="#2a4f80", padx=50, pady=50)
        frame_borde_azul.pack(expand=True, fill="both")
        frame = ttk.Frame(frame_borde_azul, padding=30)
        frame.pack(expand=True, fill="both")
        frame.configure(style="TFrame")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = ttk.Label(header, image=self.logo, background= "#ffffff")
        logo_label.pack(side="left", padx=(10, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(header, style="TFrame")
        titulo_frame.pack(side="left", anchor="center", pady=10)
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        ttk.Label(titulo_frame, text="Menu Principal", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")

        # ─────────────────────────────
        # CONTENIDO PRINCIPAL - BOTONES
        # ─────────────────────────────
        contenedor_botones = ttk.Frame(frame, style="TFrame")
        contenedor_botones.pack(expand=True, fill="both", pady=40)
        
        frame_botones_centro = ttk.Frame(contenedor_botones, style="TFrame")
        frame_botones_centro.pack(expand=True)
        
        # Postularse
        postular_frame = ttk.Frame(frame_botones_centro, style="TFrame")
        postular_frame.pack(side="left", padx=30, pady=20)
        icono_postular = tk.Label(postular_frame, text="📷", font=("Arial", 48),bg="white",fg="#2a4f80")
        icono_postular.pack(pady=(0, 10))
        btn_postular = tk.Button(postular_frame, text="Postularse", font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                width=15,
                                height=2,
                                command = self._postularse)
        btn_postular.pack()
        
        # Ver Postulaciones
        Vpostulaciones_frame = ttk.Frame(frame_botones_centro, style="TFrame")
        Vpostulaciones_frame.pack(side="left", padx=30, pady=20)
        icono_Vpostulaciones = tk.Label(Vpostulaciones_frame, text="📄", font=("Arial", 48), bg="white", fg="#2a4f80")
        icono_Vpostulaciones.pack(pady=(0, 10))
        btn_ver_postulaciones = tk.Button(Vpostulaciones_frame, text="Ver Postulaciones",font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                        width=15,
                                        height=2,
                                        command = self._ver_postulaciones)
        btn_ver_postulaciones.pack()
        
        # Seguridad
        seguridad_frame = ttk.Frame(frame_botones_centro, style="TFrame")
        seguridad_frame.pack(side="left", padx=30, pady=20)
        icono_seguridad = tk.Label(seguridad_frame, text="⚙️", font=("Arial", 48), bg="white", fg="#2a4f80")
        icono_seguridad.pack(pady=(0, 10))
        btn_seguridad = tk.Button(seguridad_frame, text="Seguridad", font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                width=15,
                                height=2,
                                command = self._seguridad)
        btn_seguridad.pack()

    def _postularse(self):
        ventana_postulacion = Ventana_Postulacion()
        ventana_postulacion.grab_set()
        self.wait_window(ventana_postulacion)

    def _ver_postulaciones(self):
        ventana_Vpostulacion = Ventana_VPostulacion()
        ventana_Vpostulacion.grab_set()
        self.wait_window(ventana_Vpostulacion)

    def _seguridad(self):
        ventana_seguridad = Ventana_Seguridad()
        ventana_seguridad.grab_set()
        self.wait_window(ventana_seguridad)

class Ventana_Postulacion(tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.grab_set()
        self.logo = None
        self.title("GIPU - Postulación")

        # Variables
        self.tipo_identificacion = tk.StringVar(value="Cédula")
        self.numero_identificacion = tk.StringVar()
        self.imagen_path = tk.StringVar()
        self.periodo_seleccionado = tk.StringVar()
        self.carrera_seleccionada = tk.StringVar()
        self.sede_seleccionada = tk.StringVar()
        self.numero_intencion = tk.StringVar(value="1")

        self._cargar_datos()
        self._crear_contenido()

    # Dimensiones centradas en pantalla
        self.ancho = 750
        self.alto = 800
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#2a4f80")
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
    
    def _cargar_datos(self):
        """Cargar periodos, carreras y sedes desde archivos"""
        # Periodos activos (simulado - luego vendrá de admin)
        self.periodos = ["2024-I", "2024-II", "2025-I"]
        
        # Cargar carreras desde archivo
        self.carreras = []
        carrera_path = os.path.join("data", "universidad", "oferta_academica.csv")
        if os.path.exists(carrera_path):
            try:
                with open(carrera_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            self.carreras.append(row[0])
            except:
                self.carreras = ["Ingeniería de Sistemas", "Administración", "Contaduría"]
        else:
            self.carreras = ["Ingeniería de Sistemas", "Administración", "Contaduría"]
            
        # Cargar sedes desde archivo (simulado)
        self.sedes = []
        sede_path = os.path.join("data", "universidad", "sedes.csv")
        if os.path.exists(sede_path):
            try:
                with open(sede_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            self.sedes.append(row[0])
            except:
                self.sedes = ["Sede Central", "Sede Norte", "Sede Sur"]
        else:
            self.sedes = ["Sede Central", "Sede Norte", "Sede Sur"]
            
        # Calcular número de intención
        self._calcular_numero_intencion()

    def _calcular_numero_intencion(self):
        """Calcular el siguiente número de intención para el usuario"""
        postulaciones_path = os.path.join("data", "estudiantes", "postulaciones.csv")
        if not os.path.exists(postulaciones_path):
            self.numero_intencion.set("1")
            return
            
        try:
            with open(postulaciones_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                max_intencion = 0
                for row in reader:
                    if len(row) > 7:  # Verificar que tenga suficientes columnas
                        try:
                            intencion = int(row[7])  # Columna 8 es número de intención
                            if intencion > max_intencion:
                                max_intencion = intencion
                        except (ValueError, IndexError):
                            continue
                self.numero_intencion.set(str(max_intencion + 1))
        except:
            self.numero_intencion.set("1")

    def _crear_contenido(self):
        # Frame azul
        frame_borde_azul = tk.Frame(self, bg="#2a4f80", padx=50, pady=50)
        frame_borde_azul.pack(expand=True, fill="both")

        

        # Frame principal
        frame = ttk.Frame(frame_borde_azul, padding=30)
        frame.pack(expand=True, fill="both")
        frame.configure(style="TFrame")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = ttk.Label(header, image=self.logo, background= "#ffffff")
        logo_label.pack(side="left", padx=(10, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(header, style="TFrame")
        titulo_frame.pack(side="left", anchor="center", pady=10)
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        ttk.Label(titulo_frame, text="Postulación", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")

         # ─────────────────────────────
        # FORMULARIO DE POSTULACIÓN
        # ─────────────────────────────
        form_frame = ttk.Frame(frame, style="TFrame")
        form_frame.pack(fill="both", expand=True, pady=20)

        # Tipo de identificación
        ttk.Label(form_frame, text="Tipo de Identificación:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=0, column=0, sticky="w", pady=10)
        
        tipo_frame = ttk.Frame(form_frame, style="TFrame")
        tipo_frame.grid(row=0, column=1, sticky="w", pady=10)
        
        tk.Radiobutton(tipo_frame, text="Cédula", variable=self.tipo_identificacion, 
                      value="Cédula", bg="white", font=("Arial", 11)).pack(side="left", padx=5)
        tk.Radiobutton(tipo_frame, text="Pasaporte", variable=self.tipo_identificacion, 
                      value="Pasaporte", bg="white", font=("Arial", 11)).pack(side="left", padx=5)

        # Número de identificación
        ttk.Label(form_frame, text="Número:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=1, column=0, sticky="w", pady=10)
        tk.Entry(form_frame, textvariable=self.numero_identificacion, 
                font=("Arial", 11), width=30).grid(row=1, column=1, sticky="w", pady=10)

        # Subir imagen
        ttk.Label(form_frame, text="Foto (PNG):", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=2, column=0, sticky="w", pady=10)
        
        img_frame = ttk.Frame(form_frame, style="TFrame")
        img_frame.grid(row=2, column=1, sticky="w", pady=10)
        
        btn_subir = tk.Button(img_frame, text="Seleccionar Imagen", 
                             font=("Arial", 10), bg="#2a4f80", fg="white",
                             command=self._seleccionar_imagen)
        btn_subir.pack(side="left", padx=(0, 10))
        
        self.lbl_imagen = ttk.Label(img_frame, text="No se ha seleccionado imagen", 
                                   font=("Arial", 10), background="#ffffff", foreground="#666666")
        self.lbl_imagen.pack(side="left")

        # Período
        ttk.Label(form_frame, text="Período:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=3, column=0, sticky="w", pady=10)
        
        periodo_combo = ttk.Combobox(form_frame, textvariable=self.periodo_seleccionado,
                                    values=self.periodos, font=("Arial", 11), state="readonly", width=28)
        periodo_combo.grid(row=3, column=1, sticky="w", pady=10)
        if self.periodos:
            periodo_combo.set(self.periodos[0])

        # Carrera
        ttk.Label(form_frame, text="Carrera:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=4, column=0, sticky="w", pady=10)
        
        carrera_combo = ttk.Combobox(form_frame, textvariable=self.carrera_seleccionada,
                                    values=self.carreras, font=("Arial", 11), state="readonly", width=28)
        carrera_combo.grid(row=4, column=1, sticky="w", pady=10)
        if self.carreras:
            carrera_combo.set(self.carreras[0])

        # Sede
        ttk.Label(form_frame, text="Sede:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=5, column=0, sticky="w", pady=10)
        
        sede_combo = ttk.Combobox(form_frame, textvariable=self.sede_seleccionada,
                                 values=self.sedes, font=("Arial", 11), state="readonly", width=28)
        sede_combo.grid(row=5, column=1, sticky="w", pady=10)
        if self.sedes:
            sede_combo.set(self.sedes[0])

        # Número de intención
        ttk.Label(form_frame, text="Número de Intención:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=6, column=0, sticky="w", pady=10)
        
        intencion_frame = ttk.Frame(form_frame, style="TFrame")
        intencion_frame.grid(row=6, column=1, sticky="w", pady=10)
        
        tk.Label(intencion_frame, text=self.numero_intencion.get(), 
                font=("Arial", 11, "bold"), bg="white", fg="#2a4f80").pack(side="left")

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        botones_frame = ttk.Frame(frame, style="TFrame")
        botones_frame.pack(fill="x", pady=30)
        
        btn_guardar = tk.Button(botones_frame, text="Guardar Postulación", 
                               font=("Arial", 12, "bold"), bg="#cca14c", fg="white",
                               width=20, height=2, command=self._guardar)
        btn_guardar.pack(side="left", padx=(0, 20))
        
        btn_cancelar = tk.Button(botones_frame, text="Cancelar", 
                                font=("Arial", 12, "bold"), bg="#cca14c", fg="white",
                                width=20, height=2, command=self._cancelar)
        btn_cancelar.pack(side="left")

    def _seleccionar_imagen(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.imagen_path.set(file_path)
            filename = os.path.basename(file_path)
            self.lbl_imagen.config(text=filename[:30] + "..." if len(filename) > 30 else filename)

    def _guardar(self):
        # Validar campos
        if not self.numero_identificacion.get().strip():
            messagebox.showerror("Error", "Debe ingresar el número de identificación")
            return
            
        if not self.periodo_seleccionado.get():
            messagebox.showerror("Error", "Debe seleccionar un período")
            return
            
        if not self.carrera_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una carrera")
            return
            
        if not self.sede_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una sede")
            return
        
        # Preparar datos
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = [
            self.tipo_identificacion.get(),
            self.numero_identificacion.get().strip(),
            os.path.basename(self.imagen_path.get()) if self.imagen_path.get() else "",
            self.periodo_seleccionado.get(),
            self.carrera_seleccionada.get(),
            self.sede_seleccionada.get(),
            fecha_actual,
            self.numero_intencion.get()
        ]
        
        # Guardar en CSV
        try:
            # Crear directorios si no existen
            os.makedirs(os.path.join("data", "estudiantes"), exist_ok=True)
            os.makedirs(os.path.join("data", "universidad"), exist_ok=True)
            
            # Guardar la imagen si se seleccionó una
            if self.imagen_path.get():
                img_dest = os.path.join("data", "estudiantes", "fotos", f"{self.numero_identificacion.get()}_{self.numero_intencion.get()}.png")
                os.makedirs(os.path.dirname(img_dest), exist_ok=True)
                # Aquí iría el código para copiar la imagen
            
            # Guardar en CSV
            csv_path = os.path.join("data", "estudiantes", "postulaciones.csv")
            file_exists = os.path.exists(csv_path)
            
            with open(csv_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    # Escribir encabezados
                    writer.writerow(["Tipo_ID", "Número_ID", "Foto", "Período", "Carrera", "Sede", "Fecha_Postulación", "Número_Intención"])
                writer.writerow(datos)
            
            messagebox.showinfo("Éxito", "Postulación guardada correctamente")
            self._cancelar()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la postulación: {str(e)}")

    def _cancelar(self):
        self.grab_release()
        self.destroy()

class Ventana_VPostulacion(tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.logo = None
        self._crear_contenido()
        self.title("GIPU - Ver Postulaciones")

    # Dimensiones centradas en pantalla
        self.ancho = 600
        self.alto = 600
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#2a4f80")
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
        # Frame principal
        frame_borde_azul = tk.Frame(self, bg="#2a4f80", padx=50, pady=50)
        frame_borde_azul.pack(expand=True, fill="both")
        frame = ttk.Frame(frame_borde_azul, padding=30)
        frame.pack(expand=True, fill="both")
        frame.configure(style="TFrame")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = ttk.Label(header, image=self.logo, background= "#ffffff")
        logo_label.pack(side="left", padx=(10, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(header, style="TFrame")
        titulo_frame.pack(side="left", anchor="center", pady=10)
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        ttk.Label(titulo_frame, text="Ver Postulaciones", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")

class Ventana_Seguridad(tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.logo = None
        self._crear_contenido()
        self.title("GIPU - Seguridad")

    # Dimensiones centradas en pantalla
        self.ancho = 600
        self.alto = 600
        self._centrar_ventana()

        # Fondo y estilos generales
        self.config(bg="#2a4f80")
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
        # Frame principal
        frame_borde_azul = tk.Frame(self, bg="#2a4f80", padx=50, pady=50)
        frame_borde_azul.pack(expand=True, fill="both")
        frame = ttk.Frame(frame_borde_azul, padding=30)
        frame.pack(expand=True, fill="both")
        frame.configure(style="TFrame")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)

        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = ttk.Label(header, image=self.logo, background= "#ffffff")
        logo_label.pack(side="left", padx=(10, 15))

        # Título del sistema
        titulo_frame = ttk.Frame(header, style="TFrame")
        titulo_frame.pack(side="left", anchor="center", pady=10)
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        ttk.Label(titulo_frame, text="Seguridad", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")