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
        self.alto = 750
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
        
        # Primera fila de botones
        frame_botones_fila1 = ttk.Frame(contenedor_botones, style="TFrame")
        frame_botones_fila1.pack(expand=True)

        frame_botones_fila2 = ttk.Frame(contenedor_botones, style="TFrame")
        frame_botones_fila2.pack(expand=True, pady=20)

        # Inscripciones
        inscripcion_frame = ttk.Frame(frame_botones_fila1, style="TFrame")
        inscripcion_frame.pack(side="left", padx=30, pady=20)
        icono_inscripcion = tk.Label(inscripcion_frame, text="📝", font=("Arial", 48), bg="white", fg="#2a4f80")
        icono_inscripcion.pack(pady=(0, 10))
        btn_inscripcion = tk.Button(inscripcion_frame, text="Inscripción", font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                width=15,
                                height=2,
                                command = self._inscripcion)
        btn_inscripcion.pack()
        
        # Postularse
        postular_frame = ttk.Frame(frame_botones_fila1, style="TFrame")
        postular_frame.pack(side="left", padx=30, pady=20)
        icono_postular = tk.Label(postular_frame, text="👤", font=("Arial", 48),bg="white",fg="#2a4f80")
        icono_postular.pack(pady=(0, 10))
        btn_postular = tk.Button(postular_frame, text="Postularse", font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                width=15,
                                height=2,
                                command = self._postularse)
        btn_postular.pack()
        
        # Ver Postulaciones
        Vpostulaciones_frame = ttk.Frame(frame_botones_fila1, style="TFrame")
        Vpostulaciones_frame.pack(side="left", padx=30, pady=20)
        icono_Vpostulaciones = tk.Label(Vpostulaciones_frame, text="📄", font=("Arial", 48), bg="white", fg="#2a4f80")
        icono_Vpostulaciones.pack(pady=(0, 10))
        btn_ver_postulaciones = tk.Button(Vpostulaciones_frame, text="Ver Postulaciones",font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                        width=15,
                                        height=2,
                                        command = self._ver_postulaciones)
        btn_ver_postulaciones.pack()
        
        # Seguridad
        seguridad_frame = ttk.Frame(frame_botones_fila2, style="TFrame")
        seguridad_frame.pack(side="left", padx=30, pady=20)
        icono_seguridad = tk.Label(seguridad_frame, text="⚙️", font=("Arial", 48), bg="white", fg="#2a4f80")
        icono_seguridad.pack(pady=(0, 10))
        btn_seguridad = tk.Button(seguridad_frame, text="Seguridad", font=("Arial", 12, "bold"), bg="#cca14c", activebackground="#ffffff", fg="white", relief="raised",
                                width=15,
                                height=2,
                                command = self._seguridad)
        btn_seguridad.pack()

    def _inscripcion(self):
        ventana_inscripcion = Ventana_Inscripcion()
        ventana_inscripcion.grab_set()
        self.wait_window(ventana_inscripcion)

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

class Ventana_Inscripcion(tk.Toplevel):
    def __init__(self, parent= None, iconos=None):
        super().__init__(parent)
        self.parent = parent 
        self.transient(parent) 
        self.grab_set()
        self.logo = None
        self.title("GIPU - Inscripción")
        
        # Variables
        self.tipo_identificacion = tk.StringVar(value="Cédula")
        self.numero_identificacion = tk.StringVar()
        self.periodo_seleccionado = tk.StringVar()
        self.periodo_id = tk.StringVar()
        self.universidad_seleccionada = tk.StringVar()
        self.universidad_id = tk.StringVar()

        # Variables para datos del estudiante
        self.nombres_estudiante = ""
        self.apellidos_estudiante = ""
        self.tipo_doc_estudiante = "Cédula"
        self.identificacion_estudiante = ""
        
        # Cargar datos
        self._cargar_datos()
        
        # Cargar datos del estudiante actual
        self._cargar_datos_estudiante()

        # Establecer el tipo de documento del estudiante
        self.tipo_identificacion.set(self.tipo_doc_estudiante)
        
        self._crear_contenido()

        # Dimensiones centradas en pantalla
        self.ancho = 700
        self.alto = 850
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
        """Cargar periodos y universidades desde archivos"""
        # Cargar periodos desde periodos.csv
        self.periodos = []
        self.periodos_dict = {}  # Diccionario para mapear nombre->id
        periodos_path = os.path.join("data", "universidad", "periodos.csv")
        if os.path.exists(periodos_path):
            try:
                with open(periodos_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if 'nombre' in row and 'id' in row:
                            periodo_nombre = row['nombre'].strip()
                            periodo_id = row['id'].strip()
                            self.periodos.append(periodo_nombre)
                            self.periodos_dict[periodo_nombre] = periodo_id
            except Exception as e:
                print(f"Error al cargar periodos: {e}")
                self.periodos = ["2024-I", "2024-II", "2025-I"]
                self.periodos_dict = {"2024-I": "1", "2024-II": "2", "2025-I": "3"}
        else:
            self.periodos = ["2024-I", "2024-II", "2025-I"]
            self.periodos_dict = {"2024-I": "1", "2024-II": "2", "2025-I": "3"}
        
        # Cargar universidades desde oferta_academica.csv
        self.universidades = []
        self.universidades_dict = {}  # Diccionario para mapear nombre->id
        oferta_path = os.path.join("data", "universidad", "oferta_academica.csv")
        
        if os.path.exists(oferta_path):
            try:
                with open(oferta_path, 'r', encoding='utf-8') as file:
                    # Leer la primera línea para detectar el delimitador
                    primera_linea = file.readline()
                    file.seek(0)  # Volver al inicio
                    
                    # El archivo oferta_academica.csv usa delimitador ';'
                    reader = csv.DictReader(file, delimiter=';')
                    
                    for row in reader:
                        # Extraer los nombres de las columnas correctamente
                        if 'IES_NOMBRE_INSTIT' in row and 'IES_ID' in row:
                            uni_nombre = row['IES_NOMBRE_INSTIT'].strip()
                            uni_id = row['IES_ID'].strip()
                            
                            # Solo agregar si no está vacío
                            if uni_nombre and uni_id:
                                if uni_nombre not in self.universidades_dict:
                                    self.universidades.append(uni_nombre)
                                    self.universidades_dict[uni_nombre] = uni_id
                        else:
                            # Si los nombres de columnas son diferentes, intentar encontrar por contenido
                            for key, value in row.items():
                                key_upper = key.upper()
                                if 'IES' in key_upper and 'NOMBRE' in key_upper:
                                    uni_nombre = value.strip()
                                elif 'IES' in key_upper and 'ID' in key_upper:
                                    uni_id = value.strip()
                            
                            if uni_nombre and uni_id and uni_nombre not in self.universidades_dict:
                                self.universidades.append(uni_nombre)
                                self.universidades_dict[uni_nombre] = uni_id
                                
                if not self.universidades:
                    # Si no se cargaron universidades, usar valores por defecto
                    self.universidades = ["UNIVERSIDAD LAICA ELOY ALFARO DE MANABI"]
                    self.universidades_dict = {"UNIVERSIDAD LAICA ELOY ALFARO DE MANABI": "102"}
                    
            except Exception as e:
                self.universidades = ["UNIVERSIDAD LAICA ELOY ALFARO DE MANABI"]
                self.universidades_dict = {"UNIVERSIDAD LAICA ELOY ALFARO DE MANABI": "102"}
        else:
            self.universidades = ["UNIVERSIDAD LAICA ELOY ALFARO DE MANABI"]
            self.universidades_dict = {"UNIVERSIDAD LAICA ELOY ALFARO DE MANABI": "102"}
    
    def _cargar_datos_estudiante(self):
        """Cargar datos del estudiante que inició sesión"""
        # Esta información debería venir de la sesión activa
        # Por ahora, cargaremos del archivo de usuarios el último usuario activo
        # En un sistema real, esto vendría de la sesión activa
        
        usuarios_path = os.path.join("data", "registros", "usuarios_registrados.csv")
        if os.path.exists(usuarios_path):
            try:
                with open(usuarios_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    usuarios = list(reader)
                    
                    if usuarios:
                        # Tomar el primer usuario como el que inició sesión
                        # En un sistema real, usaríamos una variable de sesión
                        estudiante = usuarios[0]
                        
                        self.nombres_estudiante = estudiante.get('nombres', '').strip()
                        self.apellidos_estudiante = estudiante.get('apellidos', '').strip()
                        self.tipo_doc_estudiante = estudiante.get('tipoDocumento', 'Cédula').strip()
                        self.identificacion_estudiante = estudiante.get('identificacion', '').strip()
                        
                        # Establecer valores en variables
                        self.numero_identificacion.set(self.identificacion_estudiante)
            except Exception as e:
                # Valores por defecto para pruebas
                self.nombres_estudiante = "Error al cargar datos del estudiante"
                self.apellidos_estudiante = ""
                self.tipo_doc_estudiante = ""
                self.identificacion_estudiante = ""
                self.numero_identificacion.set(self.identificacion_estudiante)
        else:
            # Valores por defecto para pruebas
            self.nombres_estudiante = "Error al cargar datos del estudiante"
            self.apellidos_estudiante = ""
            self.tipo_doc_estudiante = ""
            self.identificacion_estudiante = ""
            self.numero_identificacion.set(self.identificacion_estudiante)
    
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
        ttk.Label(titulo_frame, text="Inscripción", font=("Arial", 14), foreground="#2a4f80", background= "#ffffff").pack(anchor="w")

         # ─────────────────────────────
        # FORMULARIO DE INSCRIPCIÓN
        # ─────────────────────────────
        form_frame = ttk.Frame(frame, style="TFrame")
        form_frame.pack(fill="both", expand=True, pady=20)

        # Período
        ttk.Label(form_frame, text="Período:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=0, column=0, sticky="w", pady=15)
        
        periodo_combo = ttk.Combobox(form_frame, textvariable=self.periodo_seleccionado,
                                    values=self.periodos, font=("Arial", 11), state="readonly", width=28)
        periodo_combo.grid(row=0, column=1, sticky="w", pady=15)
        if self.periodos:
            periodo_combo.set(self.periodos[0])
        periodo_combo.bind("<<ComboboxSelected>>", self._actualizar_periodo_id)

        # Universidad
        ttk.Label(form_frame, text="Universidad:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=1, column=0, sticky="w", pady=15)
        
        universidad_combo = ttk.Combobox(form_frame, textvariable=self.universidad_seleccionada,
                                        values=self.universidades, font=("Arial", 11), state="readonly", width=28)
        universidad_combo.grid(row=1, column=1, sticky="w", pady=15)
        if self.universidades:
            universidad_combo.set(self.universidades[0])
        universidad_combo.bind("<<ComboboxSelected>>", self._actualizar_universidad_id)

        # Separador
        separator = ttk.Separator(form_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", pady=20)

        # Información del estudiante
        ttk.Label(form_frame, text="Datos del Estudiante", 
                 font=("Arial", 12, "bold"), background="#ffffff", foreground="#2a4f80").grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

        # Tipo de identificación
        ttk.Label(form_frame, text="Tipo de Identificación:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=4, column=0, sticky="w", pady=10)
        
        tipo_frame = ttk.Frame(form_frame, style="TFrame")
        tipo_frame.grid(row=4, column=1, sticky="w", pady=10)
        
        tipo_text = self.tipo_identificacion.get()
        if not tipo_text:
            tipo_text = self.tipo_doc_estudiante
            
        lbl_tipo_doc = tk.Label(tipo_frame, text=tipo_text,
                               font=("Arial", 11), bg="white", fg="#2a4f80",
                               width=15, anchor="w", relief="solid", borderwidth=1)
        lbl_tipo_doc.pack(side="left", padx=5, pady=2, ipady=3)
        
        # Agregar un pequeño indicador de que es de solo lectura
        lbl_solo_lectura = tk.Label(tipo_frame, text="(Datos de su cuenta)",
                                   font=("Arial", 9), bg="white", fg="#666666",
                                   anchor="w")
        lbl_solo_lectura.pack(side="left", padx=(10, 0))

        # Número de identificación
        ttk.Label(form_frame, text="Número de Identificación:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=5, column=0, sticky="w", pady=10)
        
        identificacion_frame = ttk.Frame(form_frame, style="TFrame")
        identificacion_frame.grid(row=5, column=1, sticky="w", pady=10)
        
        tk.Entry(identificacion_frame, textvariable=self.numero_identificacion, 
                font=("Arial", 11), width=30, state="disabled").pack(side="left")
        
        lbl_info_ident = tk.Label(identificacion_frame, text="🔒",
                                 font=("Arial", 11), bg="white", fg="#666666")
        lbl_info_ident.pack(side="left", padx=(5, 0))
        
        # Mostrar información adicional del estudiante
        if self.nombres_estudiante or self.apellidos_estudiante:
            info_frame = ttk.Frame(form_frame, style="TFrame")
            info_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=15)
            
            # Frame para la información del estudiante con borde
            estudiante_info_frame = tk.Frame(info_frame, bg="#e8f4f8", relief="solid", borderwidth=1)
            estudiante_info_frame.pack(fill="x", pady=5)
            
            # Título de la sección
            lbl_titulo_info = tk.Label(estudiante_info_frame, text="Información del Estudiante",
                                      font=("Arial", 10, "bold"), bg="#e8f4f8", fg="#2a4f80",
                                      anchor="w")
            lbl_titulo_info.pack(fill="x", padx=10, pady=(8, 5))
            
            # Nombre completo
            if self.nombres_estudiante or self.apellidos_estudiante:
                nombre_completo = f"{self.nombres_estudiante} {self.apellidos_estudiante}"
                lbl_nombre = tk.Label(estudiante_info_frame, text=f"📝 Nombre: {nombre_completo}",
                                     font=("Arial", 10), bg="#e8f4f8", fg="#333333",
                                     anchor="w")
                lbl_nombre.pack(fill="x", padx=10, pady=2)
            
            # Tipo de documento e identificación
            tipo_id_text = f"📋 {self.tipo_doc_estudiante}: {self.identificacion_estudiante}"
            lbl_tipo_id = tk.Label(estudiante_info_frame, text=tipo_id_text,
                                  font=("Arial", 10), bg="#e8f4f8", fg="#333333",
                                  anchor="w")
            lbl_tipo_id.pack(fill="x", padx=10, pady=(2, 8))
            
            # Nota informativa
            nota_frame = ttk.Frame(info_frame, style="TFrame")
            nota_frame.pack(fill="x", pady=(5, 0))
            
            lbl_nota = tk.Label(nota_frame, text="ℹ️ Los datos personales no pueden ser modificados en esta sección.",
                               font=("Arial", 9, "italic"), bg="white", fg="#666666",
                               anchor="w")
            lbl_nota.pack(anchor="w")

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        botones_frame = ttk.Frame(frame, style="TFrame")
        botones_frame.pack(fill="x", pady=30)
        
        btn_inscribir = tk.Button(botones_frame, text="Inscribirse", 
                                 font=("Arial", 12, "bold"), bg="#cca14c", fg="white",
                                 width=20, height=2, command=self._inscribir)
        btn_inscribir.pack(side="left", padx=(0, 20))
        
        btn_cancelar = tk.Button(botones_frame, text="Cancelar", 
                                font=("Arial", 12, "bold"), bg="#cca14c", fg="white",
                                width=20, height=2, command=self._cancelar)
        btn_cancelar.pack(side="left")
    
    def _actualizar_periodo_id(self, event=None):
        """Actualizar el ID del período seleccionado"""
        periodo_nombre = self.periodo_seleccionado.get()
        if periodo_nombre in self.periodos_dict:
            self.periodo_id.set(self.periodos_dict[periodo_nombre])
    
    def _actualizar_universidad_id(self, event=None):
        """Actualizar el ID de la universidad seleccionada"""
        universidad_nombre = self.universidad_seleccionada.get()
        if universidad_nombre in self.universidades_dict:
            self.universidad_id.set(self.universidades_dict[universidad_nombre])
    
    def _validar_inscripcion(self):
        """Validar que se pueda realizar la inscripción"""
        # Verificar que todos los campos estén completos
        if not self.periodo_seleccionado.get():
            messagebox.showerror("Error", "Debe seleccionar un período")
            return False
        
        if not self.universidad_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una universidad")
            return False
        
        if not self.numero_identificacion.get().strip():
            messagebox.showerror("Error", "Debe ingresar el número de identificación")
            return False
        
        # Verificar que la identificación coincida con la del estudiante que inició sesión
        if self.numero_identificacion.get().strip() != self.identificacion_estudiante:
            messagebox.showerror("Error", "La identificación no coincide con la del estudiante que inició sesión")
            return False
        
        # Asegurarse de que tenemos el ID del período actual
        self._actualizar_periodo_id()
        periodo_id_actual = self.periodo_id.get()
        
        if not periodo_id_actual:
            messagebox.showerror("Error", "No se pudo obtener el ID del período seleccionado")
            return False
        
        # Verificar que no tenga inscripción previa para este período
        inscripciones_path = os.path.join("data", "estudiantes", "Inscripcion.csv")
        if os.path.exists(inscripciones_path):
            try:
                with open(inscripciones_path, 'r', encoding='utf-8') as file:
                    # Leer encabezados si existen
                    contenido = file.read()
                    
                    if contenido.strip():  # Si el archivo no está vacío
                        file.seek(0)  # Volver al inicio
                        reader = csv.DictReader(file)
                        
                        for row in reader:
                            if 'identificacion' in row and 'Período_id' in row:
                                if (row['identificacion'] == self.identificacion_estudiante and 
                                    row['Período_id'] == periodo_id_actual):
                                    # Mostrar mensaje específico
                                    periodo_nombre = self.periodo_seleccionado.get()
                                    messagebox.showwarning("Inscripción no disponible", 
                                        f"❌ Ya tienes una inscripción para el período {periodo_nombre}.\n"
                                        f"⚠️ Solo se permite una inscripción por período.\n\n"
                                        f"📋 Si necesitas modificar tu inscripción, contacta con administración.")
                                    return False
                            elif 'identificacion' in row and 'periodo_id' in row:
                                # Verificar con nombre de columna alternativo
                                if (row['identificacion'] == self.identificacion_estudiante and 
                                    row['periodo_id'] == periodo_id_actual):
                                    periodo_nombre = self.periodo_seleccionado.get()
                                    messagebox.showwarning("Inscripción no disponible", 
                                        f"❌ Ya tienes una inscripción para el período {periodo_nombre}.\n"
                                        f"⚠️ Solo se permite una inscripción por período.\n\n"
                                        f"📋 Si necesitas modificar tu inscripción, contacta con administración.")
                                    return False
            except Exception as e:
                print(f"Error al verificar inscripciones previas: {e}")
                # Continuar si hay error en la lectura
        
        return True
    
    def _inscribir(self):
        """Realizar la inscripción del estudiante"""
        # Validar que se pueda realizar la inscripción
        if not self._validar_inscripcion():
            return
        
        # Asegurarse de que los IDs están actualizados
        self._actualizar_periodo_id()
        self._actualizar_universidad_id()
        
        # Preparar datos
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = [
            self.periodo_id.get(),  # Período_id
            self.universidad_id.get(),  # IES_ID
            self.tipo_identificacion.get(),  # tipo_Documento
            self.identificacion_estudiante,  # identificacion
            self.nombres_estudiante,  # Nombres
            self.apellidos_estudiante,  # Apellidos
            fecha_actual  # Fecha_Inscripción
        ]
        
        # Guardar en CSV
        try:
            # Crear directorios si no existen
            os.makedirs(os.path.join("data", "estudiantes"), exist_ok=True)
            
            # Guardar en CSV
            csv_path = os.path.join("data", "estudiantes", "Inscripcion.csv")
            file_exists = os.path.exists(csv_path)
            
            with open(csv_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    # Escribir encabezados
                    writer.writerow(["Período_id", "IES_ID", "tipo_Documento", "identificacion", "Nombres", "Apellidos", "Fecha_Inscripción"])
                writer.writerow(datos)
            
            # Mensaje de éxito
            periodo_nombre = self.periodo_seleccionado.get()
            universidad_nombre = self.universidad_seleccionada.get()
            
            messagebox.showinfo("✅ Inscripción Exitosa", 
                f"🎉 ¡Inscripción realizada correctamente!\n\n"
                f"📚 Período: {periodo_nombre}\n"
                f"🏫 Universidad: {universidad_nombre}\n"
                f"👤 Estudiante: {self.nombres_estudiante} {self.apellidos_estudiante}\n"
                f"📅 Fecha: {fecha_actual}\n\n"
                f"💡 Recuerda que solo puedes tener una inscripción por período.")
            
            self._cancelar()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo realizar la inscripción: {str(e)}")
    
    def _cancelar(self):
        self.grab_release()
        self.destroy()

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

        # Variables para datos del estudiante
        self.nombres_estudiante = ""
        self.apellidos_estudiante = ""
        self.tipo_doc_estudiante = ""
        self.identificacion_estudiante = ""

        # Variable para intenciones permitidas
        self.intenciones_permitidas = 1
        
        # Datos del sistema
        self._cargar_datos_estudiante()
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
    
    def _cargar_datos_estudiante(self):
        """Cargar datos del estudiante que inició sesión"""
        # Cargar datos del estudiante desde el archivo de usuarios
        usuarios_path = os.path.join("data", "registros", "usuarios_registrados.csv")
        if os.path.exists(usuarios_path):
            try:
                with open(usuarios_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    usuarios = list(reader)
                    
                    if usuarios:
                        # Tomar el primer usuario como el que inició sesión
                        estudiante = usuarios[0]
                        
                        self.nombres_estudiante = estudiante.get('nombres', '').strip()
                        self.apellidos_estudiante = estudiante.get('apellidos', '').strip()
                        self.tipo_doc_estudiante = estudiante.get('tipoDocumento', 'Cédula').strip()
                        self.identificacion_estudiante = estudiante.get('identificacion', '').strip()
                        
                        # Establecer valores en variables
                        self.tipo_identificacion.set(self.tipo_doc_estudiante)
                        self.numero_identificacion.set(self.identificacion_estudiante)
                        
                        print(f"Estudiante para postulación: {self.nombres_estudiante} {self.apellidos_estudiante}")
            except Exception as e:
                print(f"Error al cargar datos del estudiante: {e}")
                # Valores por defecto para pruebas
                self.nombres_estudiante = "Error"
                self.apellidos_estudiante = "Error"
                self.tipo_doc_estudiante = "Null"
                self.identificacion_estudiante = "00000000000"
                self.tipo_identificacion.set(self.tipo_doc_estudiante)
                self.numero_identificacion.set(self.identificacion_estudiante)
        else:
            # Valores por defecto para pruebas
            self.nombres_estudiante = "Error"
            self.apellidos_estudiante = "Error"
            self.tipo_doc_estudiante = "Null"
            self.identificacion_estudiante = "00000000000"
            self.tipo_identificacion.set(self.tipo_doc_estudiante)
            self.numero_identificacion.set(self.identificacion_estudiante)

    def _cargar_datos(self):
        """Cargar periodos, carreras y sedes desde archivos"""
        # Cargar periodos activos desde postulaciones_config.csv
        config_path = os.path.join("data", "universidad", "postulaciones_config.csv")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    # Leer primera línea para detectar delimitador
                    primera_linea = file.readline()
                    file.seek(0)  # Volver al inicio
                    
                    if ';' in primera_linea:
                        reader = csv.DictReader(file, delimiter=';')
                    else:
                        reader = csv.DictReader(file)
                    
                    for row in reader:
                        # Buscar la columna de intenciones
                        for key in row.keys():
                            if 'intenciones' in key.lower():
                                try:
                                    self.intenciones_permitidas = int(row[key].strip())
                                    print(f"Intenciones permitidas cargadas: {self.intenciones_permitidas}")
                                    break
                                except ValueError:
                                    self.intenciones_permitidas = 1
                                break
            except Exception as e:
                print(f"Error al cargar intenciones permitidas: {e}")
                self.intenciones_permitidas = 1
        else:
            self.intenciones_permitidas = 1

        self.periodos = []
        config_path = os.path.join("data", "universidad", "postulaciones_config.csv")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        if 'periodo_nombre' in row and row['periodo_nombre']:
                            self.periodos.append(row['periodo_nombre'])
            except Exception as e:
                print(f"Error al cargar periodos: {e}")
                self.periodos = ["2024-I", "2024-II", "2025-I"]  # Valores por defecto
        else:
            self.periodos = ["2024-I", "2024-II", "2025-I"]
        
        # Cargar carreras desde oferta_academica.csv usando CAR_NOMBRE_CARRERA (columna 6)
        self.carreras = []
        carrera_path = os.path.join("data", "universidad", "oferta_academica.csv")
        if os.path.exists(carrera_path):
            try:
                with open(carrera_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    carreras_set = set()  # Usar set para evitar duplicados
                    for row in reader:
                        if 'CAR_NOMBRE_CARRERA' in row and row['CAR_NOMBRE_CARRERA']:
                            carreras_set.add(row['CAR_NOMBRE_CARRERA'])
                    self.carreras = sorted(list(carreras_set))
            except Exception as e:
                print(f"Error al cargar carreras: {e}")
                self.carreras = ["Ingeniería de Sistemas", "Administración", "Contaduría"]
        else:
            self.carreras = ["Ingeniería de Sistemas", "Administración", "Contaduría"]
        
        # Cargar sedes desde oferta_academica.csv usando PRQ_NOMBRE (columna 5)
        self.sedes = []
        if os.path.exists(carrera_path):
            try:
                with open(carrera_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    sedes_set = set()  # Usar set para evitar duplicados
                    for row in reader:
                        # Obtener las tres columnas necesarias
                        pro_nombre = row.get('PRO_NOMBRE', '').strip()
                        can_nombre = row.get('CAN_NOMBRE', '').strip()
                        prq_nombre = row.get('PRQ_NOMBRE', '').strip()
                        
                        # Formatear como "Pro_Nombre - Can_Nombre - Prq_Nombre"
                        if pro_nombre and can_nombre and prq_nombre:
                            sede_formateada = f"{pro_nombre} - {can_nombre} - {prq_nombre}"
                            sedes_set.add(sede_formateada)
                    
                    self.sedes = sorted(list(sedes_set))
            except Exception as e:
                print(f"Error al cargar sedes: {e}")
                self.sedes = ["Manabi - Chone - Chone", "Manabi - Manta - Manta", "Manabi El Carmen - El Carmen"]
        else:
            self.sedes = ["Manabi - Chone - Chone", "Manabi - Manta - Manta", "Manabi El Carmen - El Carmen"]
        
        # Calcular número de intención
        self._calcular_numero_intencion()

    def _calcular_numero_intencion(self):
        """Calcular el número de intención actual del estudiante para el período seleccionado"""
        postulaciones_path = os.path.join("data", "estudiantes", "postulaciones.csv")
        if not os.path.exists(postulaciones_path):
            self.numero_intencion.set(f"1 de {self.intenciones_permitidas}")
            return
        
        try:
            periodo_actual = self.periodo_seleccionado.get()
            identificacion_actual = self.identificacion_estudiante
            
            if not periodo_actual or not identificacion_actual:
                self.numero_intencion.set(f"1 de {self.intenciones_permitidas}")
                return
            
            # Contar postulaciones del estudiante para este período
            contador = 0
            with open(postulaciones_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (row.get('identificacion', '') == identificacion_actual and 
                        row.get('Período', '') == periodo_actual):
                        contador += 1
            
            # Verificar si ya alcanzó el límite de intenciones
            if contador >= self.intenciones_permitidas:
                periodo_nombre = periodo_actual
                messagebox.showwarning("Límite alcanzado",
                    f"⚠️ Ya has alcanzado el límite de {self.intenciones_permitidas} postulaciones para el período {periodo_nombre}.\n"
                    f"📋 No puedes realizar más postulaciones en este período.")
                self.numero_intencion.set(f"{contador} de {self.intenciones_permitidas} (LÍMITE)")
                return
            
            # Mostrar el número de intención actual
            intencion_actual = contador + 1
            self.numero_intencion.set(f"{intencion_actual} de {self.intenciones_permitidas}")
            
        except Exception as e:
            print(f"Error al calcular número de intención: {e}")
            self.numero_intencion.set(f"1 de {self.intenciones_permitidas}")

    def _actualizar_intencion(self, event=None):
        """Actualizar número de intención cuando cambia el período o identificación"""
        self._calcular_numero_intencion()

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

        ttk.Label(form_frame, text="Datos del Estudiante", 
                 font=("Arial", 12, "bold"), background="#ffffff", foreground="#2a4f80").grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        # Frame para información del estudiante
        estudiante_frame = tk.Frame(form_frame, bg="#e8f4f8", relief="solid", borderwidth=1)
        estudiante_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
        
        # Nombre del estudiante
        nombre_completo = f"{self.nombres_estudiante} {self.apellidos_estudiante}"
        lbl_nombre = tk.Label(estudiante_frame, text=f"👤 Estudiante: {nombre_completo}",
                             font=("Arial", 11), bg="#e8f4f8", fg="#2a4f80",
                             anchor="w")
        lbl_nombre.pack(fill="x", padx=10, pady=(8, 2))
        
        # Tipo de documento e identificación
        tipo_id_text = f"📋 {self.tipo_doc_estudiante}: {self.identificacion_estudiante}"
        lbl_tipo_id = tk.Label(estudiante_frame, text=tipo_id_text,
                              font=("Arial", 10), bg="#e8f4f8", fg="#333333",
                              anchor="w")
        lbl_tipo_id.pack(fill="x", padx=10, pady=(2, 8))

        # Período
        ttk.Label(form_frame, text="Período:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=3, column=0, sticky="w", pady=10)
        
        periodo_combo = ttk.Combobox(form_frame, textvariable=self.periodo_seleccionado,
                                    values=self.periodos, font=("Arial", 11), state="readonly", width=28)
        periodo_combo.grid(row=3, column=1, sticky="w", pady=10)
        if self.periodos:
            periodo_combo.set(self.periodos[0])
        periodo_combo = ttk.Combobox(form_frame, textvariable=self.periodo_seleccionado,
                                    values=self.periodos, font=("Arial", 11), state="readonly", width=28)
        periodo_combo.grid(row=3, column=1, sticky="w", pady=10)
        if self.periodos:
            periodo_combo.set(self.periodos[0])
        self.periodo_seleccionado.trace('w', lambda *args: self._actualizar_intencion())

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

        # Número de intención
        ttk.Label(form_frame, text="Número de Intención:", 
                 font=("Arial", 11, "bold"), background="#ffffff").grid(row=6, column=0, sticky="w", pady=15)
        
        intencion_frame = ttk.Frame(form_frame, style="TFrame")
        intencion_frame.grid(row=6, column=1, sticky="w", pady=15)
        
        # Mostrar número de intención y límite
        lbl_intencion = tk.Label(intencion_frame, text=self.numero_intencion.get(),
                                font=("Arial", 11, "bold"), bg="white", fg="#2a4f80")
        lbl_intencion.pack(side="left")
        
        # Información sobre el límite
        lbl_info_intencion = tk.Label(intencion_frame, 
                                     text=f"(Máximo {self.intenciones_permitidas} por período)",
                                     font=("Arial", 9), bg="white", fg="#666666")
        lbl_info_intencion.pack(side="left", padx=(10, 0))

        # Nota informativa
        nota_frame = ttk.Frame(form_frame, style="TFrame")
        nota_frame.grid(row=7, column=0, columnspan=2, sticky="w", pady=10)
        
        lbl_nota = tk.Label(nota_frame, 
                           text="ℹ️ Los datos del estudiante se cargan automáticamente de tu cuenta.",
                           font=("Arial", 9, "italic"), bg="white", fg="#666666",
                           anchor="w")
        lbl_nota.pack(anchor="w")

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
        if not self.periodo_seleccionado.get():
            messagebox.showerror("Error", "Debe seleccionar un período")
            return
            
        if not self.carrera_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una carrera")
            return
            
        if not self.sede_seleccionada.get():
            messagebox.showerror("Error", "Debe seleccionar una sede")
            return
        
        # Validar que no tenga postulación previa para este período
        postulaciones_path = os.path.join("data", "estudiantes", "postulaciones.csv")
        if os.path.exists(postulaciones_path):
            try:
                # Contar postulaciones actuales del estudiante para este período
                contador = 0
                with open(postulaciones_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if (row.get('identificacion', '') == self.identificacion_estudiante and 
                            row.get('Período', '') == self.periodo_seleccionado.get()):
                            contador += 1
                
                # Verificar límite
                if contador >= self.intenciones_permitidas:
                    periodo_nombre = self.periodo_seleccionado.get()
                    messagebox.showerror("Límite alcanzado", 
                        f"❌ Ya has alcanzado el límite de {self.intenciones_permitidas} postulaciones para el período {periodo_nombre}.\n"
                        f"⚠️ No puedes realizar más postulaciones en este período.")
                    return
                    
            except:
                pass  # Continuar si hay error en la validación
         # Preparar datos
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extraer solo el PRQ_NOMBRE de la sede formateada para guardar
        sede_guardar = self.sede_seleccionada.get()
        if " - " in sede_guardar:
            partes = sede_guardar.split(" - ")
            if len(partes) >= 3:
                sede_guardar = partes[2]
        
        # Obtener el número de intención actual (extraer del texto "X de Y")
        texto_intencion = self.numero_intencion.get()
        numero_intencion_actual = "1"
        if "de" in texto_intencion:
            partes_intencion = texto_intencion.split("de")
            numero_intencion_actual = partes_intencion[0].strip()
        
        datos = [
            self.tipo_doc_estudiante,  # Tipo de documento del estudiante
            self.identificacion_estudiante,  # Identificación del estudiante
            os.path.basename(self.imagen_path.get()) if self.imagen_path.get() else "",
            self.periodo_seleccionado.get(),
            self.carrera_seleccionada.get(),
            sede_guardar,  # Guardar solo el PRQ_NOMBRE
            fecha_actual,
            numero_intencion_actual  # Número de intención actual
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