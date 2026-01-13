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
        icono_postular = tk.Label(postular_frame, text="👤", font=("Arial", 48),bg="white",fg="#2a4f80")
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
                    writer.writerow(["tipo_Documento", "identificacion", "Foto", "Período", "Carrera", "Sede", "Fecha_Postulación", "Número_Intención"])
                writer.writerow(datos)
            
            messagebox.showinfo("Éxito", "Postulación guardada correctamente")
            self._cancelar()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la postulación: {str(e)}")

    def _cancelar(self):
        self.grab_release()
        self.destroy()

class Ventana_VPostulacion(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.grab_set()
        self.logo = None
        self.title("GIPU - Ver Postulaciones")
        
        # Variables para filtros
        self.filtro_identificacion = tk.StringVar()
        self.filtro_periodo = tk.StringVar()
        self.filtro_carrera = tk.StringVar()

        # Cargar datos
        self._cargar_datos()
        
        # Crear contenido
        self._crear_contenido()

        # Dimensiones centradas en pantalla
        self.ancho = 1000
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
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#2a4f80", foreground="white")
        estilo.configure("Treeview", font=("Arial", 10), background="white", fieldbackground="white")
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", False)
        self.resizable(False, False)
    
    def _cargar_datos(self):
        """Cargar postulaciones y datos adicionales"""
        # Cargar postulaciones
        self.postulaciones = []
        postulaciones_path = os.path.join("data", "estudiantes", "postulaciones.csv")
        if os.path.exists(postulaciones_path):
            try:
                with open(postulaciones_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader, None)  # Leer encabezados
                    for row in reader:
                        if len(row) >= 8:
                            # Crear diccionario con los datos
                            postulacion = {
                                'tipo_documento': row[0] if len(row) > 0 else '',
                                'identificacion': row[1] if len(row) > 1 else '',
                                'foto': row[2] if len(row) > 2 else '',
                                'periodo': row[3] if len(row) > 3 else '',
                                'carrera': row[4] if len(row) > 4 else '',
                                'sede': row[5] if len(row) > 5 else '',
                                'fecha': row[6] if len(row) > 6 else '',
                                'intencion': row[7] if len(row) > 7 else ''
                            }
                            self.postulaciones.append(postulacion)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar postulaciones: {str(e)}")
                self.postulaciones = []
        
        # Cargar datos del admin (horarios y modalidades)
        self.horarios_modalidades = {}
        admin_path = os.path.join("data", "admin", "configuracion.csv")
        if os.path.exists(admin_path):
            try:
                with open(admin_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 4:
                            key = f"{row[0]}_{row[1]}"  # periodo_carrera
                            self.horarios_modalidades[key] = {
                                'horario': row[2] if len(row) > 2 else 'No definido',
                                'modalidad': row[3] if len(row) > 3 else 'No definido',
                                'nombre_convocatoria': row[4] if len(row) > 4 else 'Convocatoria General'
                            }
            except:
                # Si hay error, usar datos por defecto
                pass
        
        # Cargar datos de estudiantes (nombre y apellido)
        self.datos_estudiantes = {}
        estudiantes_path = os.path.join("data", "registros", "usuarios_registrados.csv")
        if os.path.exists(estudiantes_path):
            try:
                with open(estudiantes_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3:
                            self.datos_estudiantes[row[0]] = {
                                'nombre': row[1] if len(row) > 1 else 'No registrado',
                                'apellido': row[2] if len(row) > 2 else 'No registrado'
                            }
            except:
                # Si hay error, datos por defecto
                pass

    def _crear_contenido(self):
        # Frame principal
        frame_borde_azul = tk.Frame(self, bg="#2a4f80", padx=30, pady=30)
        frame_borde_azul.pack(expand=True, fill="both")
        
        # Frame interior blanco
        frame = ttk.Frame(frame_borde_azul, padding=20)
        frame.pack(expand=True, fill="both")
        frame.configure(style="TFrame")

        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=(0, 20))

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
        ttk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), 
                  foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        ttk.Label(titulo_frame, text="Ver Postulaciones", font=("Arial", 14), 
                  foreground="#2a4f80", background= "#ffffff").pack(anchor="w")

        # ─────────────────────────────
        # FILTROS
        # ─────────────────────────────
        filtros_frame = ttk.Frame(frame, style="TFrame")
        filtros_frame.pack(fill="x", pady=(0, 20))
        
        # Filtro por identificación
        ttk.Label(filtros_frame, text="Filtrar por ID:", 
                 font=("Arial", 10, "bold"), background="#ffffff").pack(side="left", padx=(0, 5))
        entry_filtro = ttk.Entry(filtros_frame, textvariable=self.filtro_identificacion,
                                font=("Arial", 10), width=15)
        entry_filtro.pack(side="left", padx=(0, 15))
        entry_filtro.bind("<KeyRelease>", lambda e: self._actualizar_tabla())
        
        # Botón para limpiar filtros
        btn_limpiar = tk.Button(filtros_frame, text="Limpiar Filtros",
                               font=("Arial", 10), bg="#2a4f80", fg="white",
                               command=self._limpiar_filtros)
        btn_limpiar.pack(side="right", padx=(10, 0))
        
        # Información de cantidad
        self.lbl_cantidad = ttk.Label(filtros_frame, text=f"Total: {len(self.postulaciones)} postulaciones",
                                     font=("Arial", 10), background="#ffffff", foreground="#2a4f80")
        self.lbl_cantidad.pack(side="right", padx=(20, 0))

        # ─────────────────────────────
        # TABLA DE POSTULACIONES
        # ─────────────────────────────
        # Frame para la tabla con scrollbars
        tabla_frame = ttk.Frame(frame, style="TFrame")
        tabla_frame.pack(expand=True, fill="both", pady=(0, 20))
        
        # Crear Treeview
        columns = ("#", "Tipo Doc", "Identificación", "Período", "Carrera", "Sede", "Fecha", "Intención")
        self.tabla = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tabla.heading("#", text="#")
        self.tabla.heading("Tipo Doc", text="Tipo Documento")
        self.tabla.heading("Identificación", text="Identificación")
        self.tabla.heading("Período", text="Período")
        self.tabla.heading("Carrera", text="Carrera")
        self.tabla.heading("Sede", text="Sede")
        self.tabla.heading("Fecha", text="Fecha Postulación")
        self.tabla.heading("Intención", text="N° Intención")
        
        # Ancho de columnas
        self.tabla.column("#", width=40, anchor="center")
        self.tabla.column("Tipo Doc", width=100, anchor="center")
        self.tabla.column("Identificación", width=120, anchor="center")
        self.tabla.column("Período", width=80, anchor="center")
        self.tabla.column("Carrera", width=150, anchor="w")
        self.tabla.column("Sede", width=120, anchor="w")
        self.tabla.column("Fecha", width=150, anchor="center")
        self.tabla.column("Intención", width=80, anchor="center")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        hsb = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)
        
        # Bind para doble click
        self.tabla.bind("<Double-1>", self._mostrar_detalles)
        self.tabla.bind("<Return>", self._mostrar_detalles)
        
        # Llenar tabla
        self._actualizar_tabla()

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        botones_frame = ttk.Frame(frame, style="TFrame")
        botones_frame.pack(fill="x", pady=10)
        
        btn_actualizar = tk.Button(botones_frame, text="Actualizar", 
                                 font=("Arial", 11, "bold"), bg="#2a4f80", fg="white",
                                 width=15, height=1, command=self._actualizar_datos)
        btn_actualizar.pack(side="left", padx=(0, 10))
        
        btn_cerrar = tk.Button(botones_frame, text="Cerrar", 
                              font=("Arial", 11, "bold"), bg="#cca14c", fg="white",
                              width=15, height=1, command=self._cerrar)
        btn_cerrar.pack(side="right")

    def _actualizar_tabla(self):
        """Actualizar la tabla con los datos filtrados"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Aplicar filtro
        filtro_id = self.filtro_identificacion.get().strip().lower()
        postulaciones_filtradas = []
        
        if filtro_id:
            for post in self.postulaciones:
                if filtro_id in post['identificacion'].lower():
                    postulaciones_filtradas.append(post)
        else:
            postulaciones_filtradas = self.postulaciones
        
        # Llenar tabla
        for i, post in enumerate(postulaciones_filtradas, 1):
            self.tabla.insert("", "end", values=(
                i,
                post['tipo_documento'],
                post['identificacion'],
                post['periodo'],
                post['carrera'],
                post['sede'],
                post['fecha'],
                post['intencion']
            ))
        
        # Actualizar contador
        self.lbl_cantidad.config(text=f"Mostrando: {len(postulaciones_filtradas)} de {len(self.postulaciones)} postulaciones")

    def _limpiar_filtros(self):
        """Limpiar todos los filtros"""
        self.filtro_identificacion.set("")
        self._actualizar_tabla()

    def _actualizar_datos(self):
        """Actualizar datos desde archivos"""
        self._cargar_datos()
        self._actualizar_tabla()
        messagebox.showinfo("Actualizado", "Datos actualizados correctamente")

    def _mostrar_detalles(self, event=None):
        """Mostrar detalles de la postulación seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una postulación")
            return
        
        item = self.tabla.item(seleccion[0])
        valores = item['values']
        
        # Obtener datos completos de la postulación
        identificacion = valores[2]
        periodo = valores[3]
        carrera = valores[4]
        
        # Buscar la postulación completa
        postulacion = None
        for post in self.postulaciones:
            if (post['identificacion'] == identificacion and 
                post['periodo'] == periodo and 
                post['carrera'] == carrera):
                postulacion = post
                break
        
        if not postulacion:
            messagebox.showerror("Error", "No se encontraron los datos completos de la postulación")
            return
        
        # Obtener datos adicionales
        datos_estudiante = self.datos_estudiantes.get(identificacion, {})
        nombre = datos_estudiante.get('nombre', 'No registrado')
        apellido = datos_estudiante.get('apellido', 'No registrado')
        
        # Obtener horario y modalidad
        key = f"{periodo}_{carrera}"
        config_admin = self.horarios_modalidades.get(key, {})
        horario = config_admin.get('horario', 'No definido')
        modalidad = config_admin.get('modalidad', 'No definido')
        nombre_convocatoria = config_admin.get('nombre_convocatoria', 'Convocatoria General')
        
        # Crear mensaje detallado
        mensaje = f"""
        📋 DETALLES DE LA POSTULACIÓN
        
        🏷️  CONVOCATORIA: {nombre_convocatoria}
        
        👤 DATOS DEL ESTUDIANTE:
           • Tipo Documento: {postulacion['tipo_documento']}
           • Identificación: {postulacion['identificacion']}
           • Nombre: {nombre} {apellido}
        
        📚 DATOS ACADÉMICOS:
           • Período: {postulacion['periodo']}
           • Carrera: {postulacion['carrera']}
           • Sede: {postulacion['sede']}
        
        ⏰ INFORMACIÓN DEL EXAMEN:
           • Horario: {horario}
           • Modalidad: {modalidad}
        
        📅 DATOS DE POSTULACIÓN:
           • Fecha: {postulacion['fecha']}
           • N° de Intención: {postulacion['intencion']}
        
        📎 INFORMACIÓN ADICIONAL:
           • Foto: {postulacion['foto'] if postulacion['foto'] else 'No subida'}
        """
        
        # Mostrar ventana de detalles
        ventana_detalles = tk.Toplevel(self)
        ventana_detalles.title("Detalles de Postulación")
        ventana_detalles.geometry("500x600")
        ventana_detalles.config(bg="#f0f0f0")
        ventana_detalles.transient(self)
        ventana_detalles.grab_set()
        
        # Frame principal
        frame_detalles = tk.Frame(ventana_detalles, bg="#ffffff", padx=20, pady=20)
        frame_detalles.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Título
        tk.Label(frame_detalles, text="Detalles de Postulación", 
                font=("Arial", 16, "bold"), bg="#ffffff", fg="#2a4f80").pack(pady=(0, 20))
        
        # Texto con detalles
        texto_detalles = tk.Text(frame_detalles, font=("Arial", 11), bg="#ffffff", fg="#333333", wrap="word",height=20, width=50)
        texto_detalles.pack(fill="both", expand=True, pady=(0, 20))
        texto_detalles.insert("1.0", mensaje)
        texto_detalles.config(state="disabled")
        
        # Botón cerrar
        btn_cerrar_detalles = tk.Button(frame_detalles, text="Cerrar", font=("Arial", 11, "bold"), bg="#2a4f80", fg="white",width=20, command=ventana_detalles.destroy)
        btn_cerrar_detalles.pack()

    def _cerrar(self):
        """Cerrar la ventana"""
        self.grab_release()
        self.destroy()

class Ventana_Seguridad(tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.grab_set()
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
        ttk.Label(titulo_frame, text="Seguridad - Cambiar Contraseña", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")
        # ─────────────────────────────
        # FORMULARIO DE CAMBIO DE CONTRASEÑA
        # ─────────────────────────────
        form_frame = ttk.Frame(frame, style="TFrame")
        form_frame.pack(fill="both", expand=True, pady=15)

        # Información
        info_label = ttk.Label(form_frame, 
                            text="Ingrese su información para cambiar la contraseña", 
                            font=("Arial", 11),
                            background="#ffffff")
        info_label.pack(pady=(0, 15))

        # Contenedor para campos en dos columnas
        campos_frame = ttk.Frame(form_frame, style="TFrame")
        campos_frame.pack(fill="x", pady=5)

        # Columna izquierda (etiquetas)
        etiquetas_frame = ttk.Frame(campos_frame, style="TFrame")
        etiquetas_frame.pack(side="left", padx=(0, 10))

        # Columna derecha (entradas)
        entradas_frame = ttk.Frame(campos_frame, style="TFrame")
        entradas_frame.pack(side="left")

        # Tipo de documento
        ttk.Label(etiquetas_frame, text="Tipo de Documento:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        tipo_frame = ttk.Frame(entradas_frame, style="TFrame")
        tipo_frame.pack(anchor="w", pady=3)

        self.tipo_doc = tk.StringVar(value="Cédula")
        tk.Radiobutton(tipo_frame, text="Cédula", variable=self.tipo_doc, 
                    value="Cédula", bg="white", font=("Arial", 10)).pack(side="left", padx=2)
        tk.Radiobutton(tipo_frame, text="Pasaporte", variable=self.tipo_doc, 
                    value="Pasaporte", bg="white", font=("Arial", 10)).pack(side="left", padx=2)

        # Número de identificación
        ttk.Label(etiquetas_frame, text="Número de Identificación:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        self.identificacion = ttk.Entry(entradas_frame, font=("Arial", 10), width=25)
        self.identificacion.pack(anchor="w", pady=3)

        # Correo electrónico
        ttk.Label(etiquetas_frame, text="Correo Electrónico:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        self.correo = ttk.Entry(entradas_frame, font=("Arial", 10), width=25)
        self.correo.pack(anchor="w", pady=3)

        # Contraseña actual
        ttk.Label(etiquetas_frame, text="Contraseña Actual:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        self.password_actual = ttk.Entry(entradas_frame, font=("Arial", 10), width=25, show="*")
        self.password_actual.pack(anchor="w", pady=3)

        # Nueva contraseña
        ttk.Label(etiquetas_frame, text="Nueva Contraseña:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        self.nueva_password = ttk.Entry(entradas_frame, font=("Arial", 10), width=25, show="*")
        self.nueva_password.pack(anchor="w", pady=3)

        # Confirmar nueva contraseña
        ttk.Label(etiquetas_frame, text="Confirmar Nueva Contraseña:", 
                font=("Arial", 10, "bold"), 
                background="#ffffff").pack(anchor="w", pady=3)

        self.confirmar_password = ttk.Entry(entradas_frame, font=("Arial", 10), width=25, show="*")
        self.confirmar_password.pack(anchor="w", pady=3)

        # Mostrar/Ocultar contraseñas
        mostrar_frame = ttk.Frame(form_frame, style="TFrame")
        mostrar_frame.pack(anchor="w", pady=(10, 5))

        self.mostrar_passwords = tk.BooleanVar(value=False)
        tk.Checkbutton(mostrar_frame, text="Mostrar contraseñas", 
                    variable=self.mostrar_passwords,
                    bg="white", font=("Arial", 9),
                    command=self._alternar_mostrar_passwords).pack(side="left")

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        botones_frame = ttk.Frame(frame, style="TFrame")
        botones_frame.pack(fill="x", pady=(5, 0))

        btn_cambiar = tk.Button(botones_frame, text="Cambiar Contraseña", 
                            font=("Arial", 11, "bold"), bg="#cca14c", fg="white",
                            width=18, height=1, command=self._cambiar_contraseña)
        btn_cambiar.pack(side="left", padx=(0, 10))

        btn_cancelar = tk.Button(botones_frame, text="Cancelar", 
                                font=("Arial", 11, "bold"), bg="#2a4f80", fg="white",
                                width=15, height=1, command=self._cancelar)
        btn_cancelar.pack(side="left")
    
    def _alternar_mostrar_passwords(self):
        mostrar = self.mostrar_passwords.get()
        show_char = "" if mostrar else "*"
        
        self.password_actual.config(show=show_char)
        self.nueva_password.config(show=show_char)
        self.confirmar_password.config(show=show_char)
    
    def _cambiar_contraseña(self):
        # Obtener datos
        tipo_doc = self.tipo_doc.get()
        identificacion = self.identificacion.get().strip()
        correo = self.correo.get().strip()
        password_actual = self.password_actual.get()
        nueva_password = self.nueva_password.get()
        confirmar_password = self.confirmar_password.get()
        
        # Validaciones básicas
        if not all([identificacion, correo, password_actual, nueva_password, confirmar_password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if nueva_password != confirmar_password:
            messagebox.showerror("Error", "Las nuevas contraseñas no coinciden")
            return
            
        if len(nueva_password) < 6:
            messagebox.showerror("Error", "La nueva contraseña debe tener al menos 6 caracteres")
            return
        
        # Verificar y actualizar en archivo
        usuarios_path = os.path.join("data", "registros", "usuarios_registrados.csv")
        
        if not os.path.exists(usuarios_path):
            messagebox.showerror("Error", "No hay usuarios registrados en el sistema")
            return
        
        usuarios = []
        usuario_encontrado = False
        
        try:
            with open(usuarios_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # Leer encabezados
                
                if headers is None or len(headers) < 6:
                    messagebox.showerror("Error", "Formato de archivo de usuarios incorrecto")
                    return
                
                for row in reader:
                    if len(row) >= 6:
                        # Verificar si es el usuario
                        if (row[0] == tipo_doc and 
                            row[1] == identificacion and 
                            row[2] == correo):
                            
                            # Verificar contraseña actual
                            if row[5] != password_actual:
                                messagebox.showerror("Error", "Contraseña actual incorrecta")
                                return
                            
                            usuario_encontrado = True
                            # Actualizar contraseña
                            row[5] = nueva_password
                        
                        usuarios.append(row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo de usuarios: {str(e)}")
            return
        
        if not usuario_encontrado:
            messagebox.showerror("Error", "No se encontró un usuario con esos datos")
            return
        
        # Guardar cambios
        try:
            with open(usuarios_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["tipoDocumento", "identificacion", "correo", "nombres", "apellidos", "contraseña"])
                # Escribir todos los usuarios
                for usuario in usuarios:
                    writer.writerow(usuario)
            
            messagebox.showinfo("Éxito", "Contraseña cambiada correctamente")
            self._cancelar()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {str(e)}")
    
    def _cancelar(self):
        self.grab_release()
        self.destroy()