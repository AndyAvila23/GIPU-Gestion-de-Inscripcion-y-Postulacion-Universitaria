import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk, filedialog
import os
import csv
import json
from datetime import datetime, timedelta
from controls.usuarios.Administrador import GestorAdministradores

class AdminVentana(tk.Tk):
    def __init__(self, parent=None, iconos=None):
        super().__init__()
        self.logo = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "..", "..", "data", "universidad")
        self.postulaciones_dir = os.path.join(self.base_dir, "..", "..", "data", "postulaciones")
        
        # Crear directorios si no existen
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.postulaciones_dir, exist_ok=True)
        
        # Variables para periodos
        self.var_periodo_nombre = tk.StringVar()
        self.var_periodo_inicio = tk.StringVar()
        self.var_periodo_fin = tk.StringVar()

        # Variables para postulaciones
        self.var_postulacion_periodo = tk.StringVar()
        self.var_postulacion_intenciones = tk.StringVar(value="1")
        self.var_postulacion_fecha_limite = tk.StringVar()
        self.var_postulacion_hora_limite = tk.StringVar(value="23:59")

        # Variables para administradores
        self.var_admin_filtro_tipo = tk.StringVar(value="todos")
        self.var_admin_busqueda = tk.StringVar()
        
        # Variables para formulario de administradores
        self.var_admin_id = tk.StringVar()
        self.var_admin_tipo_doc = tk.StringVar(value="Cédula")
        self.var_admin_identificacion = tk.StringVar()
        self.var_admin_nombres = tk.StringVar()
        self.var_admin_apellidos = tk.StringVar()
        self.var_admin_correo = tk.StringVar()
        self.var_admin_password = tk.StringVar()
        self.var_admin_rol = tk.StringVar(value="Administrador")
        self.var_admin_show_password = tk.BooleanVar(value=False)
        
        # Variables para oferta académica
        self.var_ies_id = tk.StringVar()
        self.var_ies_nombre = tk.StringVar()
        self.var_carrera_nombre = tk.StringVar()
        self.var_area_nombre = tk.StringVar()
        self.var_subarea_nombre = tk.StringVar()
        self.var_nivel = tk.StringVar()
        self.var_modalidad = tk.StringVar()
        self.var_jornada = tk.StringVar()
        self.var_cupos_total = tk.StringVar()
        self.var_focalizada = tk.StringVar()
        
        self.var_file_path = tk.StringVar()
        
        # Inicializar menú de administración
        self.admin_menu = AdminMenu()
        
        # Ahora crear contenido
        self._crear_contenido()
        self.title("GIPU - Panel de Administración")
        
        # Dimensiones centradas en pantalla
        self.ancho = 1200  # Aumentado para más columnas
        self.alto = 750
        self._centrar_ventana()
        
        # Fondo y estilos generales
        self._configurar_estilos()
        
        # Cargar datos iniciales
        self.cargar_datos()
        self.inicializar_archivo_admin()

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
    # Configuración de estilos base
    # ─────────────────────────────
    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        
        # Configurar estilos para diferentes widgets
        estilo.configure("TButton", font=("Arial", 11), padding=5, background="#cca14c", foreground="#ffffff")
        estilo.map("TButton", background=[('active', '#d4a94c')])
        
        estilo.configure("TLabel", font=("Arial", 11))
        estilo.configure("TFrame", background="#f0f0f0")
        
        # Estilo para frames con fondo blanco
        estilo.configure("White.TFrame", background="#ffffff")
        estilo.configure("Header.TFrame", background="#f0f0f0")
        
        estilo.configure("TNotebook", background="#f0f0f0")
        estilo.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 11, "bold"))
        
        self.config(bg="#f0f0f0")
        self.attributes("-fullscreen", False)
        self.attributes("-topmost", False)
        self.resizable(True, True)  # Permitir redimensionar para ver más columnas
    
    def cargar_datos(self):
        # Cargar períodos
        self.periodos = []
        periodos_path = os.path.join(self.data_dir, "periodos.csv")
        if os.path.exists(periodos_path):
            try:
                with open(periodos_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.periodos = list(reader)
            except:
                self.periodos = []
    
    def _crear_contenido(self):
        # Frame principal
        main_frame = ttk.Frame(self, style="Header.TFrame", padding=10)
        main_frame.pack(expand=True, fill="both")
        
        # ─────────────────────────────
        # ENCABEZADO
        # ─────────────────────────────
        header = tk.Frame(main_frame, bg="#f0f0f0")
        header.pack(fill="x", pady=(0, 10))
        
        # Cargar logo
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = PhotoImage(file=logo_path)
            self.logo = self.logo.subsample(7, 7)
            logo_label = tk.Label(header, image=self.logo, bg="#f0f0f0")
            logo_label.pack(side="left", padx=(10, 15))
        
        # Título del sistema
        titulo_frame = tk.Frame(header, bg="#f0f0f0")
        titulo_frame.pack(side="left", anchor="center", pady=10)
        tk.Label(titulo_frame, text="GIPU", font=("Arial", 18, "bold"), 
                 fg="#2a4f80", bg="#f0f0f0").pack(anchor="w")
        tk.Label(titulo_frame, text="Panel de Administración", font=("Arial", 12), 
                 fg="#2a4f80", bg="#f0f0f0").pack(anchor="w")
        
        # ─────────────────────────────
        # NOTEBOOK (PESTAÑAS)
        # ─────────────────────────────
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Pestaña 1: Gestionar Inscripciones
        self.tab_inscripciones = ttk.Frame(self.notebook, style="White.TFrame")
        self.notebook.add(self.tab_inscripciones, text="Gestionar Inscripciones")
        self._crear_tab_inscripciones()
        
        # Pestaña 2: Gestionar Postulaciones
        self.tab_postulaciones = ttk.Frame(self.notebook, style="White.TFrame")
        self.notebook.add(self.tab_postulaciones, text="Gestionar Postulaciones")
        self._crear_tab_postulaciones()
        
        # Pestaña 3: Gestionar Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook, style="White.TFrame")
        self.notebook.add(self.tab_usuarios, text="Gestionar Usuarios")
        self._crear_tab_usuarios()
        
        # Pestaña 4: Gestionar Administradores
        self.tab_administradores = ttk.Frame(self.notebook, style="White.TFrame")
        self.notebook.add(self.tab_administradores, text="Gestionar Administradores")
        self._crear_tab_administradores()
        
        # Pestaña 5: Oferta Académica
        self.tab_oferta = ttk.Frame(self.notebook, style="White.TFrame")
        self.notebook.add(self.tab_oferta, text="Oferta Académica")
        self._crear_tab_oferta()
        
        # Botón para cerrar
        btn_cerrar = ttk.Button(main_frame, text="Cerrar Sesión", command=self.destroy)
        btn_cerrar.pack(pady=10)
    
    def _crear_tab_inscripciones(self):
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.tab_inscripciones, bg="#ffffff")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido de la pestaña
        content_frame = tk.Frame(scrollable_frame, bg="#ffffff", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Sección 1: Gestión de Períodos
        tk.Label(content_frame, text="Gestión de Períodos Académicos", 
                 font=("Arial", 16, "bold"), fg="#2a4f80", bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Formulario para agregar período
        form_frame = tk.LabelFrame(content_frame, text="Agregar Nuevo Período", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Nombre del período (ej: 2025-1, 2025-2)
        tk.Label(form_frame, text="Nombre del Período (ej: 2025-1):", 
                bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombre = ttk.Entry(form_frame, textvariable=self.var_periodo_nombre, width=20)
        entry_nombre.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Fecha de inicio
        tk.Label(form_frame, text="Fecha de Inicio (YYYY-MM-DD):", 
                bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        entry_inicio = ttk.Entry(form_frame, textvariable=self.var_periodo_inicio, width=20)
        entry_inicio.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Fecha de fin
        tk.Label(form_frame, text="Fecha de Fin (YYYY-MM-DD):", 
                bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        entry_fin = ttk.Entry(form_frame, textvariable=self.var_periodo_fin, width=20)
        entry_fin.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Botones del formulario
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Agregar Período", 
                  command=self.agregar_periodo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", 
                  command=self.limpiar_form_periodo).pack(side="left", padx=5)
        
        # Sección 2: Lista de Períodos
        lista_frame = tk.LabelFrame(content_frame, text="Períodos Registrados", 
                                   bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                   padx=15, pady=15)
        lista_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Treeview para mostrar períodos
        columns = ("ID", "Nombre", "Fecha Inicio", "Fecha Fin", "Estado", "Duración")
        self.tree_periodos = ttk.Treeview(lista_frame, columns=columns, show="headings", height=8)
        
        # Configurar anchos de columnas
        column_widths = {
            "ID": 50,
            "Nombre": 100,
            "Fecha Inicio": 120,
            "Fecha Fin": 120,
            "Estado": 100,
            "Duración": 80
        }
        
        for col in columns:
            self.tree_periodos.heading(col, text=col)
            self.tree_periodos.column(col, width=column_widths.get(col, 100))
        
        scrollbar_tree = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_periodos.yview)
        self.tree_periodos.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree_periodos.pack(side="left", fill="both", expand=True)
        scrollbar_tree.pack(side="right", fill="y")
        
        # Botones de acción para períodos
        action_frame = tk.Frame(lista_frame, bg="#ffffff")
        action_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        ttk.Button(action_frame, text="Eliminar Período", 
                  command=self.eliminar_periodo).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Actualizar Lista", 
                  command=self.actualizar_lista_periodos).pack(side="left", padx=5)
        
        # Sección 3: Subir Oferta Académica
        oferta_frame = tk.LabelFrame(content_frame, text="Gestión de Oferta Académica", 
                                    bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                    padx=15, pady=15)
        oferta_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(oferta_frame, text="Cargar archivo CSV de oferta académica:", 
                bg="#ffffff").pack(anchor="w", pady=5)
        
        file_frame = tk.Frame(oferta_frame, bg="#ffffff")
        file_frame.pack(fill="x", pady=10)
        
        ttk.Entry(file_frame, textvariable=self.var_file_path, width=50).pack(side="left", padx=(0, 10))
        ttk.Button(file_frame, text="Buscar", command=self.buscar_archivo).pack(side="left")
        
        ttk.Button(oferta_frame, text="Subir Oferta Académica", 
                  command=self.subir_oferta_csv).pack(pady=10)
        
        # Cargar lista inicial de períodos
        self.actualizar_lista_periodos()
    
    def _crear_tab_postulaciones(self):
        content_frame = tk.Frame(self.tab_postulaciones, bg="#ffffff", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Gestión de Postulaciones", 
                 font=("Arial", 16, "bold"), fg="#2a4f80", bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Frame con dos columnas
        columns_frame = tk.Frame(content_frame, bg="#ffffff")
        columns_frame.pack(fill="both", expand=True)
        
        # Columna izquierda: Crear postulación
        left_frame = tk.Frame(columns_frame, bg="#ffffff", width=400)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Formulario para crear postulación
        form_frame = tk.LabelFrame(left_frame, text="Crear Nueva Postulación", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Campo 1: Seleccionar período
        tk.Label(form_frame, text="Período Académico:", 
                bg="#ffffff", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(5, 2))
        
        # Frame para combobox y botón de actualizar
        periodo_frame = tk.Frame(form_frame, bg="#ffffff")
        periodo_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Combobox para períodos
        self.combo_periodos = ttk.Combobox(periodo_frame, textvariable=self.var_postulacion_periodo, 
                                          state="readonly", width=25)
        self.combo_periodos.pack(side="left", padx=(0, 10))
        
        # Botón para actualizar lista de períodos
        ttk.Button(periodo_frame, text="Actualizar", 
                  command=self.actualizar_combo_periodos, width=10).pack(side="left")
        
        # Campo 2: Número de intenciones (ahora es un Entry)
        tk.Label(form_frame, text="Número de Intenciones (1-5):", 
                bg="#ffffff", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 2))
        
        # Entry para número de intenciones
        entry_intenciones = ttk.Entry(form_frame, textvariable=self.var_postulacion_intenciones, width=10)
        entry_intenciones.grid(row=3, column=0, sticky="w", pady=(0, 10))
        
        # Información adicional
        tk.Label(form_frame, text="Número de carreras que puede seleccionar", 
                bg="#ffffff", font=("Arial", 9), fg="#666666").grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(0, 10))
        
        # Campo 3: Fecha límite
        tk.Label(form_frame, text="Fecha Límite (YYYY-MM-DD):", 
                bg="#ffffff", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 2))
        
        fecha_entry = ttk.Entry(form_frame, textvariable=self.var_postulacion_fecha_limite, width=20)
        fecha_entry.grid(row=5, column=0, sticky="w", pady=(0, 10))
        
        # Sugerencia de fecha actual + 30 días
        fecha_sugerida = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        tk.Label(form_frame, text=f"Sugerencia: {fecha_sugerida}", 
                bg="#ffffff", font=("Arial", 9), fg="#666666").grid(row=5, column=1, sticky="w", padx=(10, 0), pady=(0, 10))
        
        # Campo 4: Hora límite
        tk.Label(form_frame, text="Hora Límite (HH:MM):", 
                bg="#ffffff", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w", pady=(10, 2))
        
        hora_entry = ttk.Entry(form_frame, textvariable=self.var_postulacion_hora_limite, width=10)
        hora_entry.grid(row=7, column=0, sticky="w", pady=(0, 20))
        
        # Información adicional para hora
        tk.Label(form_frame, text="Formato 24 horas", 
                bg="#ffffff", font=("Arial", 9), fg="#666666").grid(row=7, column=1, sticky="w", padx=(10, 0), pady=(0, 20))
        
        # Botones del formulario
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Crear Postulación", 
                  command=self.crear_postulacion, width=20).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", 
                  command=self.limpiar_form_postulacion, width=10).pack(side="left", padx=5)
        
        # Información de validación
        info_frame = tk.LabelFrame(left_frame, text="Reglas de Validación", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 10, "bold"),
                                  padx=10, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        reglas = [
            "• Solo se puede crear una postulación por período",
            "• El período debe estar en estado 'PLANIFICADO'",
            "• La fecha límite debe ser posterior a hoy",
            "• Número de intenciones: 1 a 5",
            "• Si se elimina la postulación, se elimina su archivo"
        ]
        
        for regla in reglas:
            tk.Label(info_frame, text=regla, bg="#ffffff", 
                    font=("Arial", 9), justify="left").pack(anchor="w", pady=2)
        
        # Columna derecha: Lista de postulaciones
        right_frame = tk.Frame(columns_frame, bg="#ffffff")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        lista_frame = tk.LabelFrame(right_frame, text="Postulaciones Activas", 
                                   bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                   padx=15, pady=15)
        lista_frame.pack(fill="both", expand=True)
        
        # Treeview para postulaciones
        columns = ("Período", "Intenciones", "Fecha Límite", "Hora", "Estado", "Archivo")
        self.tree_postulaciones = ttk.Treeview(lista_frame, columns=columns, show="headings", height=15)
        
        column_widths = {
            "Período": 120,
            "Intenciones": 100,
            "Fecha Límite": 120,
            "Hora": 80,
            "Estado": 100,
            "Archivo": 150
        }
        
        for col in columns:
            self.tree_postulaciones.heading(col, text=col)
            self.tree_postulaciones.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_postulaciones.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient="horizontal", command=self.tree_postulaciones.xview)
        self.tree_postulaciones.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_postulaciones.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Botones de acción
        action_frame = tk.Frame(lista_frame, bg="#ffffff")
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Button(action_frame, text="Eliminar Postulación", 
                  command=self.eliminar_postulacion, width=20).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Actualizar Lista", 
                  command=self.actualizar_lista_postulaciones, width=15).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Ver Detalles", 
                  command=self.ver_detalles_postulacion, width=15).pack(side="right", padx=5)
        
        # Cargar datos iniciales
        self.actualizar_combo_periodos()
        self.actualizar_lista_postulaciones()
    
    # ─────────────────────────────
    # MÉTODOS PARA POSTULACIONES
    # ─────────────────────────────
    
    def actualizar_combo_periodos(self):
        """Actualiza el combobox con períodos disponibles"""
        periodos = self.admin_menu.obtener_periodos()
        
        # Filtrar solo períodos en estado PLANIFICADO
        periodos_planificados = []
        valores_combo = []
        
        for periodo in periodos:
            if periodo.get('estado') == 'ABIERTO': #PLANIFICADO
                nombre = periodo.get('nombre', '')
                id_periodo = periodo.get('id', '')
                if nombre:
                    periodos_planificados.append(periodo)
                    valores_combo.append(f"{nombre} (ID: {id_periodo})")
        
        # Actualizar combobox
        self.combo_periodos['values'] = valores_combo
        
        # Verificar si hay períodos planificados
        if not periodos_planificados:
            messagebox.showwarning("Sin períodos", 
                                 "No hay períodos en estado 'PLANIFICADO' disponibles.")
        
        return periodos_planificados
    
    def crear_postulacion(self, datos_postulacion):
        """Crea una nueva configuración de postulación"""
        try:
            periodo_id = datos_postulacion.get('periodo_id')
            intenciones = datos_postulacion.get('intenciones')
            fecha_limite = datos_postulacion.get('fecha_limite')
            hora_limite = datos_postulacion.get('hora_limite')
            
            # Validar que no exista ya una postulación para este período
            configs = self.obtener_postulaciones_config()
            for config in configs:
                if config.get('periodo_id') == str(periodo_id):
                    return {"success": False, "message": "Ya existe una postulación para este período"}
            
            # Obtener información del período
            periodos = self.obtener_periodos()
            periodo_nombre = ""
            for periodo in periodos:
                if periodo.get('id') == str(periodo_id):
                    periodo_nombre = periodo.get('nombre', '')
                    break
            
            if not periodo_nombre:
                return {"success": False, "message": "Período no encontrado"}
            
            # Obtener siguiente ID
            if configs:
                max_id = 0
                for config in configs:
                    try:
                        id_num = int(config.get('id', 0))
                        max_id = max(max_id, id_num)
                    except:
                        pass
                new_id = str(max_id + 1)
            else:
                new_id = "1"
            
            # Crear archivo CSV de postulación
            archivo_nombre = f"postulacion_{periodo_id}.csv"
            archivo_path = os.path.join(self.postulaciones_dir, archivo_nombre)
            
            # Crear encabezados del archivo
            with open(archivo_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['periodo_id', 'periodo_nombre', 'fecha_limite', 'hora_limite', 
                            'intenciones', 'estado', 'fecha_creacion'])
                writer.writerow([periodo_id, periodo_nombre, fecha_limite, hora_limite, 
                            intenciones, 'ACTIVA', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            
            # Guardar en configuraciones
            with open(self.postulaciones_config_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    new_id, periodo_id, periodo_nombre, intenciones,
                    fecha_limite, hora_limite, 
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'ACTIVA'
                ])
            
            # Cambiar estado del período a ACTIVO
            self.actualizar_estado_periodo(periodo_id, 'ACTIVO')
            
            return {
                "success": True, 
                "message": f"Postulación creada exitosamente. Archivo: {archivo_nombre}"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error al crear postulación: {str(e)}"}
    
    def eliminar_postulacion(self):
        """Elimina una postulación seleccionada"""
        selected_item = self.tree_postulaciones.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una postulación para eliminar")
            return
        
        item = self.tree_postulaciones.item(selected_item[0])
        valores = item['values']
        
        if not valores:
            return
        
        periodo = valores[0]
        archivo = valores[5] if len(valores) > 5 else ""
        
        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                     f"¿Está seguro de eliminar la postulación del período '{periodo}'?\n\n"
                                     f"Esta acción eliminará el archivo: {archivo}")
        
        if confirm:
            # Extraer ID del período del archivo
            import re
            match = re.search(r'postulacion_(\d+)\.csv', archivo)
            if match:
                periodo_id = match.group(1)
                resultado = self.admin_menu.eliminar_postulacion(periodo_id)
                
                if resultado["success"]:
                    messagebox.showinfo("Éxito", resultado["message"])
                    self.actualizar_lista_postulaciones()
                    self.actualizar_combo_periodos()
                else:
                    messagebox.showerror("Error", resultado["message"])
            else:
                messagebox.showerror("Error", "No se pudo identificar el período de la postulación")
    
    def actualizar_lista_postulaciones(self):
        """Actualiza la lista de postulaciones activas"""
        # Limpiar treeview
        for item in self.tree_postulaciones.get_children():
            self.tree_postulaciones.delete(item)
        
        # Obtener postulaciones activas
        postulaciones = self.admin_menu.obtener_postulaciones_activas()
        
        for post in postulaciones:
            self.tree_postulaciones.insert("", "end", values=(
                post.get('periodo_nombre', ''),
                post.get('intenciones', ''),
                post.get('fecha_limite', ''),
                post.get('hora_limite', ''),
                post.get('estado', ''),
                post.get('archivo', '')
            ))
    
    def ver_detalles_postulacion(self):
        """Muestra los detalles de una postulación seleccionada"""
        selected_item = self.tree_postulaciones.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una postulación para ver detalles")
            return
        
        item = self.tree_postulaciones.item(selected_item[0])
        valores = item['values']
        
        if not valores or len(valores) < 6:
            return
        
        periodo = valores[0]
        archivo = valores[5]
        
        # Leer archivo de postulación
        archivo_path = os.path.join(self.postulaciones_dir, archivo)
        
        if not os.path.exists(archivo_path):
            messagebox.showerror("Error", f"No se encontró el archivo: {archivo}")
            return
        
        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Mostrar contenido en una ventana emergente
            ventana_detalles = tk.Toplevel(self)
            ventana_detalles.title(f"Detalles Postulación - {periodo}")
            ventana_detalles.geometry("600x400")
            ventana_detalles.config(bg="#ffffff")
            
            # Texto con scroll
            text_frame = tk.Frame(ventana_detalles, bg="#ffffff")
            text_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap="word", font=("Courier", 10), 
                                 bg="#f8f8f8", relief="flat")
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Insertar contenido
            text_widget.insert("1.0", contenido)
            text_widget.config(state="disabled")  # Solo lectura
            
            # Botón cerrar
            ttk.Button(ventana_detalles, text="Cerrar", 
                      command=ventana_detalles.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {str(e)}")
    
    def limpiar_form_postulacion(self):
        """Limpia el formulario de postulación"""
        self.var_postulacion_periodo.set("")
        self.var_postulacion_intenciones.set("")  # Vaciar en lugar de "1"
        
        # Sugerir fecha actual + 30 días
        fecha_sugerida = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.var_postulacion_fecha_limite.set(fecha_sugerida)
        
        self.var_postulacion_hora_limite.set("23:59")
    
    def _crear_tab_usuarios(self):
        # Frame principal con scroll
        main_frame = tk.Frame(self.tab_usuarios, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        # Crear Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Frame que contendrá todo el contenido
        content_frame = tk.Frame(canvas, bg="#ffffff")
        
        # Configurar el scroll
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Crear ventana en el canvas
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Asegurar que el contenido_frame tenga el ancho correcto
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.bind("<Configure>", configure_canvas)
        
        # AHORA TODO EL CONTENIDO VA DENTRO DE content_frame
        
        tk.Label(content_frame, text="Gestión de Usuarios", 
                 font=("Arial", 16, "bold"), fg="#2a4f80", bg="#ffffff").pack(anchor="w", pady=(20, 20), padx=20)
        
        # --- SECCIÓN SUPERIOR: BÚSQUEDA Y FILTROS ---
        busqueda_frame = tk.LabelFrame(content_frame, text="Buscar Usuarios", 
                                      bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                      padx=15, pady=15)
        busqueda_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # Filtros de búsqueda
        filtros_frame = tk.Frame(busqueda_frame, bg="#ffffff")
        filtros_frame.pack(fill="x", pady=(0, 10))
        
        # Tipo de filtro
        tk.Label(filtros_frame, text="Filtrar por:", bg="#ffffff").pack(side="left", padx=(0, 10))
        
        self.var_tipo_filtro = tk.StringVar(value="todos")
        tipos_filtro = [
            ("Todos", "todos"),
            ("Nombre", "nombres"),
            ("Apellido", "apellidos"),
            ("Identificación", "identificacion"),
            ("Correo", "correo")
        ]
        
        for texto, valor in tipos_filtro:
            rb = tk.Radiobutton(filtros_frame, text=texto, variable=self.var_tipo_filtro,
                              value=valor, bg="#ffffff", command=self.actualizar_placeholder)
            rb.pack(side="left", padx=(0, 10))
        
        # Campo de búsqueda
        busqueda_entry_frame = tk.Frame(busqueda_frame, bg="#ffffff")
        busqueda_entry_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(busqueda_entry_frame, text="Buscar:", bg="#ffffff").pack(side="left", padx=(0, 10))
        
        self.var_busqueda = tk.StringVar()
        self.entry_busqueda = ttk.Entry(busqueda_entry_frame, textvariable=self.var_busqueda, width=40)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        
        # Placeholder inicial
        self.entry_busqueda.insert(0, "Ingrese texto para buscar...")
        self.entry_busqueda.config(foreground="grey")
        self.entry_busqueda.bind("<FocusIn>", self.on_entry_focus_in)
        self.entry_busqueda.bind("<FocusOut>", self.on_entry_focus_out)
        
        # Botones de búsqueda
        btn_busqueda_frame = tk.Frame(busqueda_entry_frame, bg="#ffffff")
        btn_busqueda_frame.pack(side="left")
        
        ttk.Button(btn_busqueda_frame, text="Buscar", 
                  command=self.buscar_usuarios, width=10).pack(side="left", padx=(0, 5))
        ttk.Button(btn_busqueda_frame, text="Limpiar", 
                  command=self.limpiar_busqueda, width=10).pack(side="left")
        
        # Botón para mostrar todos
        ttk.Button(busqueda_frame, text="Mostrar Todos", 
                  command=self.mostrar_todos_usuarios, width=15).pack(anchor="e", pady=(5, 0))
        
        # --- SECCIÓN MEDIA: LISTA DE USUARIOS ---
        lista_frame = tk.LabelFrame(content_frame, text="Usuarios Registrados", 
                                   bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                   padx=15, pady=15)
        lista_frame.pack(fill="both", expand=True, pady=(0, 20), padx=20)
        
        # Treeview para usuarios
        columns = ("ID", "Tipo Doc", "Identificación", "Nombres", "Apellidos", "Correo", "Estado")
        self.tree_usuarios = ttk.Treeview(lista_frame, columns=columns, show="headings", height=8)
        
        column_widths = {
            "ID": 50,
            "Tipo Doc": 80,
            "Identificación": 120,
            "Nombres": 150,
            "Apellidos": 150,
            "Correo": 180,
            "Estado": 100
        }
        
        for col in columns:
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=column_widths.get(col, 100))
        
        # Scrollbar para el treeview (opcional)
        tree_v_scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=tree_v_scrollbar.set)
        
        # Colocar treeview y scrollbar
        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        tree_v_scrollbar.pack(side="right", fill="y")
        
        # Botones de acción para lista
        action_lista_frame = tk.Frame(lista_frame, bg="#ffffff")
        action_lista_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        ttk.Button(action_lista_frame, text="Modificar Usuario", 
                  command=self.mostrar_form_modificar, width=15).pack(side="left", padx=5)
        ttk.Button(action_lista_frame, text="Eliminar Usuario", 
                  command=self.eliminar_usuario, width=15).pack(side="left", padx=5)
        ttk.Button(action_lista_frame, text="Actualizar Lista", 
                  command=self.mostrar_todos_usuarios, width=15).pack(side="right", padx=5)
        
        # --- SECCIÓN INFERIOR: FORMULARIO MODIFICACIÓN ---
        form_frame = tk.LabelFrame(content_frame, text="Modificar Usuario", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # Variables para el formulario
        self.var_mod_id = tk.StringVar()
        self.var_mod_tipo_doc = tk.StringVar(value="Cédula")
        self.var_mod_identificacion = tk.StringVar()
        self.var_mod_nombres = tk.StringVar()
        self.var_mod_apellidos = tk.StringVar()
        self.var_mod_correo = tk.StringVar()
        self.var_mod_password = tk.StringVar()
        
        # Grid para formulario
        row = 0
        
        # ID (oculto, solo para referencia)
        tk.Label(form_frame, text="ID:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        tk.Label(form_frame, textvariable=self.var_mod_id, bg="#ffffff", fg="#666666").grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Tipo de documento
        tk.Label(form_frame, text="Tipo Documento:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        tipo_doc_combo = ttk.Combobox(form_frame, textvariable=self.var_mod_tipo_doc, 
                                     values=["Cédula", "Pasaporte", "RUC", "Carnet Extranjería"], 
                                     state="readonly", width=20)
        tipo_doc_combo.grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Identificación
        tk.Label(form_frame, text="Identificación:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_mod_identificacion, width=25).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Nombres
        tk.Label(form_frame, text="Nombres:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_mod_nombres, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Apellidos
        tk.Label(form_frame, text="Apellidos:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_mod_apellidos, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Correo
        tk.Label(form_frame, text="Correo Electrónico:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_mod_correo, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Contraseña
        tk.Label(form_frame, text="Contraseña:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        password_frame = tk.Frame(form_frame, bg="#ffffff")
        password_frame.grid(row=row, column=1, sticky="w", pady=5)
        
        self.entry_mod_password = ttk.Entry(password_frame, textvariable=self.var_mod_password, 
                                           show="*", width=25)
        self.entry_mod_password.pack(side="left")
        
        # Checkbox para mostrar contraseña
        self.var_show_password = tk.BooleanVar(value=False)
        check_show = tk.Checkbutton(password_frame, text="Mostrar", variable=self.var_show_password,
                                   command=self.toggle_show_password, bg="#ffffff")
        check_show.pack(side="left", padx=(10, 0))
        row += 1
        
        # Botones del formulario
        btn_form_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_form_frame.grid(row=row, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_form_frame, text="Guardar Cambios", 
                  command=self.guardar_modificacion_usuario, width=15).pack(side="left", padx=5)
        ttk.Button(btn_form_frame, text="Cancelar", 
                  command=self.limpiar_form_modificar, width=10).pack(side="left", padx=5)
        ttk.Button(btn_form_frame, text="Generar Nueva Contraseña", 
                  command=self.generar_nueva_password, width=20).pack(side="left", padx=5)
        
        # Información de estado
        self.label_estado = tk.Label(form_frame, text="", bg="#ffffff", fg="green", font=("Arial", 10))
        self.label_estado.grid(row=row+1, column=0, columnspan=2, pady=(5, 0))
        
        # Cargar usuarios inicialmente
        self.mostrar_todos_usuarios()
    
    # ─────────────────────────────
    # MÉTODOS PARA GESTIÓN DE USUARIOS
    # ─────────────────────────────
    
    def on_entry_focus_in(self, event):
        """Maneja el evento cuando el entry de búsqueda recibe foco"""
        if self.entry_busqueda.get() == "Ingrese texto para buscar...":
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.config(foreground="black")
    
    def on_entry_focus_out(self, event):
        """Maneja el evento cuando el entry de búsqueda pierde foco"""
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, "Ingrese texto para buscar...")
            self.entry_busqueda.config(foreground="grey")
    
    def actualizar_placeholder(self):
        """Actualiza el placeholder según el tipo de filtro seleccionado"""
        if self.var_tipo_filtro.get() == "todos":
            placeholder = "Ingrese texto para buscar en todos los campos..."
        elif self.var_tipo_filtro.get() == "nombres":
            placeholder = "Ej: Juan, María, Carlos..."
        elif self.var_tipo_filtro.get() == "apellidos":
            placeholder = "Ej: Pérez, González, López..."
        elif self.var_tipo_filtro.get() == "identificacion":
            placeholder = "Ej: 1234567890, 0987654321..."
        elif self.var_tipo_filtro.get() == "correo":
            placeholder = "Ej: usuario@email.com..."
        
        # Actualizar placeholder si está visible
        current_text = self.entry_busqueda.get()
        if current_text == "Ingrese texto para buscar..." or current_text.startswith("Ej:"):
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.insert(0, placeholder)
            self.entry_busqueda.config(foreground="grey")
    
    def buscar_usuarios(self):
        """Busca usuarios según los filtros seleccionados"""
        tipo_filtro = self.var_tipo_filtro.get()
        texto_busqueda = self.var_busqueda.get().strip().lower()
        
        # Si el texto es el placeholder, buscar vacío
        if texto_busqueda in ["ingrese texto para buscar...", "ej: juan, maría, carlos...", 
                             "ej: pérez, gonzález, lópez...", "ej: 1234567890, 0987654321...",
                             "ej: usuario@email.com...", "ingrese texto para buscar en todos los campos..."]:
            texto_busqueda = ""
        
        # Obtener todos los usuarios
        usuarios = self.admin_menu.obtener_todos_usuarios()
        
        if not usuarios:
            messagebox.showinfo("Sin usuarios", "No hay usuarios registrados en el sistema")
            return
        
        # Filtrar usuarios
        usuarios_filtrados = []
        
        for usuario in usuarios:
            if tipo_filtro == "todos":
                # Buscar en todos los campos
                campos = [
                    usuario.get('tipoDocumento', ''),
                    usuario.get('identificacion', ''),
                    usuario.get('nombres', ''),
                    usuario.get('apellidos', ''),
                    usuario.get('correo', '')
                ]
                if any(texto_busqueda in campo.lower() for campo in campos if campo):
                    usuarios_filtrados.append(usuario)
            else:
                # Buscar en campo específico
                campo = usuario.get(tipo_filtro, '')
                if texto_busqueda in campo.lower():
                    usuarios_filtrados.append(usuario)
        
        # Actualizar treeview
        self.actualizar_treeview_usuarios(usuarios_filtrados)
        
        # Mostrar mensaje de resultados
        if texto_busqueda:
            self.label_estado.config(
                text=f"Se encontraron {len(usuarios_filtrados)} usuarios",
                fg="blue"
            )
    
    def mostrar_todos_usuarios(self):
        """Muestra todos los usuarios en el treeview"""
        usuarios = self.admin_menu.obtener_todos_usuarios()
        self.actualizar_treeview_usuarios(usuarios)
        self.label_estado.config(
            text=f"Total de usuarios: {len(usuarios)}",
            fg="green"
        )
    
    def actualizar_treeview_usuarios(self, usuarios):
        """Actualiza el treeview con la lista de usuarios"""
        # Limpiar treeview
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        # Ordenar por ID
        usuarios_ordenados = sorted(usuarios, key=lambda x: int(x.get('id', 0)))
        
        # Insertar usuarios
        for usuario in usuarios_ordenados:
            self.tree_usuarios.insert("", "end", values=(
                usuario.get('id', ''),
                usuario.get('tipoDocumento', ''),
                usuario.get('identificacion', ''),
                usuario.get('nombres', ''),
                usuario.get('apellidos', ''),
                usuario.get('correo', ''),
                'Activo'
            ))
    
    def limpiar_busqueda(self):
        """Limpia los campos de búsqueda"""
        self.var_busqueda.set("")
        self.var_tipo_filtro.set("todos")
        self.actualizar_placeholder()
        self.mostrar_todos_usuarios()
    
    def mostrar_form_modificar(self):
        """Muestra el formulario con los datos del usuario seleccionado"""
        selected_item = self.tree_usuarios.selection()
        
        if not selected_item:
            messagebox.showwarning("Seleccionar Usuario", 
                                  "Por favor, seleccione un usuario de la lista para modificar.")
            return
        
        item = self.tree_usuarios.item(selected_item[0])
        valores = item['values']
        
        
        if not valores or len(valores) < 7:
            messagebox.showerror("Error", "Datos del usuario incompletos")
            return
        
        try:
            # Obtener identificación del usuario (columna 2 en el treeview)
            identificacion = valores[2]  # Columna "Identificación"
            nombres = valores[3]
            apellidos = valores[4]
            correo = valores[5]
            tipo_doc = valores[1]
            
            # Obtener usuario completo por identificación
            usuario = self.admin_menu.obtener_usuario_por_identificacion(identificacion)
            
            if not usuario:
                # Intentar cargar con datos básicos del treeview
                usuario = {
                    'tipoDocumento': tipo_doc,
                    'identificacion': identificacion,
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'correo': correo,
                    'contraseña': '********'  # Contraseña por defecto
                }
                messagebox.showinfo("Información", 
                                  "Contraseña no disponible. Deberá establecer una nueva contraseña.")
            
            # Llenar formulario
            self.var_mod_id.set(identificacion)
            self.var_mod_tipo_doc.set(usuario.get('tipoDocumento', 'Cédula'))
            self.var_mod_identificacion.set(usuario.get('identificacion', ''))
            self.var_mod_nombres.set(usuario.get('nombres', ''))
            self.var_mod_apellidos.set(usuario.get('apellidos', ''))
            self.var_mod_correo.set(usuario.get('correo', ''))
            self.var_mod_password.set(usuario.get('contraseña', ''))
            self.var_show_password.set(False)
            self.entry_mod_password.config(show="*")
            
            # Mostrar mensaje
            self.label_estado.config(
                text=f"Modificando usuario: {nombres} {apellidos}",
                fg="orange"
            )
            
        except Exception as e:
            print(f"DEBUG: Error al cargar formulario: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el formulario: {str(e)}")
    
    def toggle_show_password(self):
        """Alterna entre mostrar y ocultar la contraseña"""
        if self.var_show_password.get():
            self.entry_mod_password.config(show="")
        else:
            self.entry_mod_password.config(show="*")
    
    def generar_nueva_password(self):
        """Genera una nueva contraseña aleatoria"""
        import random
        import string
        
        # Generar contraseña de 8 caracteres
        caracteres = string.ascii_letters + string.digits
        nueva_password = ''.join(random.choice(caracteres) for _ in range(8))
        
        self.var_mod_password.set(nueva_password)
        messagebox.showinfo("Nueva Contraseña", 
                           f"Contraseña generada: {nueva_password}\n\nRecuerde guardar los cambios.")
    
    def guardar_modificacion_usuario(self):
        """Guarda los cambios del usuario modificado"""
        # Validar campos obligatorios
        campos_obligatorios = [
            ("Tipo Documento", self.var_mod_tipo_doc.get().strip()),
            ("Identificación", self.var_mod_identificacion.get().strip()),
            ("Nombres", self.var_mod_nombres.get().strip()),
            ("Apellidos", self.var_mod_apellidos.get().strip()),
            ("Correo", self.var_mod_correo.get().strip()),
            ("Contraseña", self.var_mod_password.get().strip())
        ]
        
        campos_vacios = [nombre for nombre, valor in campos_obligatorios if not valor]
        if campos_vacios:
            messagebox.showerror("Error", f"Campos obligatorios vacíos:\n{', '.join(campos_vacios)}")
            return
        
        # Validar formato de correo
        correo = self.var_mod_correo.get().strip()
        if "@" not in correo or "." not in correo:
            if not messagebox.askyesno("Confirmar", 
                                      "El correo electrónico no parece tener un formato válido.\n"
                                      "¿Desea continuar de todos modos?"):
                return
        
        # Validar longitud de contraseña
        password = self.var_mod_password.get().strip()
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        # Obtener identificación original (antes de modificar)
        identificacion_original = self.var_mod_id.get()
        
        # Preparar datos
        datos_usuario = {
            'identificacion_original': identificacion_original,
            'tipoDocumento': self.var_mod_tipo_doc.get().strip(),
            'identificacion': self.var_mod_identificacion.get().strip(),
            'nombres': self.var_mod_nombres.get().strip(),
            'apellidos': self.var_mod_apellidos.get().strip(),
            'correo': self.var_mod_correo.get().strip(),
            'contraseña': self.var_mod_password.get().strip()
        }
        
        # Verificar si la identificación cambió
        if identificacion_original != datos_usuario['identificacion']:
            respuesta = messagebox.askyesno("Confirmar Cambio", 
                                           f"Está cambiando la identificación del usuario:\n\n"
                                           f"De: {identificacion_original}\n"
                                           f"A: {datos_usuario['identificacion']}\n\n"
                                           f"¿Está seguro de continuar?")
            if not respuesta:
                return
        
        # Guardar cambios
        resultado = self.admin_menu.modificar_usuario(datos_usuario)
        
        if resultado["success"]:
            messagebox.showinfo("Éxito", resultado["message"])
            self.limpiar_form_modificar()
            self.mostrar_todos_usuarios()
            self.label_estado.config(text="Cambios guardados correctamente", fg="green")
        else:
            messagebox.showerror("Error", resultado["message"])
    
    def eliminar_usuario(self):
        """Elimina el usuario seleccionado"""
        selected_item = self.tree_usuarios.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar Usuario", "Seleccione un usuario para eliminar")
            return
        
        item = self.tree_usuarios.item(selected_item[0])
        valores = item['values']
        
        if not valores or len(valores) < 7:
            return
        
        identificacion = valores[2]  # Usar identificación en lugar de ID
        nombres = valores[3]
        apellidos = valores[4]
        
        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                     f"¿Está seguro de eliminar al usuario:\n\n"
                                     f"{nombres} {apellidos}\n"
                                     f"Identificación: {identificacion}\n\n"
                                     f"Esta acción no se puede deshacer.")
        
        if confirm:
            resultado = self.admin_menu.eliminar_usuario_por_identificacion(identificacion)
            
            if resultado["success"]:
                messagebox.showinfo("Éxito", resultado["message"])
                self.mostrar_todos_usuarios()
                self.limpiar_form_modificar()
            else:
                messagebox.showerror("Error", resultado["message"])
    
    def limpiar_form_modificar(self):
        """Limpia el formulario de modificación"""
        self.var_mod_id.set("")
        self.var_mod_tipo_doc.set("Cédula")
        self.var_mod_identificacion.set("")
        self.var_mod_nombres.set("")
        self.var_mod_apellidos.set("")
        self.var_mod_correo.set("")
        self.var_mod_password.set("")
        self.var_show_password.set(False)
        self.entry_mod_password.config(show="*")
        self.label_estado.config(text="", fg="green")
    
    def _crear_tab_administradores(self):
        content_frame = tk.Frame(self.tab_administradores, bg="#ffffff", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Gestión de Administradores", 
                 font=("Arial", 16, "bold"), fg="#2a4f80", bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(content_frame, bg="#ffffff")
        main_frame.pack(fill="both", expand=True)
        
        # --- COLUMNA IZQUIERDA: BÚSQUEDA Y LISTA ---
        left_frame = tk.Frame(main_frame, bg="#ffffff", width=500)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Sección de búsqueda
        busqueda_frame = tk.LabelFrame(left_frame, text="Buscar Administradores", 
                                      bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                      padx=15, pady=15)
        busqueda_frame.pack(fill="x", pady=(0, 20))
        
        # Filtros de búsqueda
        filtros_frame = tk.Frame(busqueda_frame, bg="#ffffff")
        filtros_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filtros_frame, text="Filtrar por:", bg="#ffffff").pack(side="left", padx=(0, 10))
        
        tipos_filtro_admin = [
            ("Todos", "todos"),
            ("Nombre", "Nombre"),
            ("Apellido", "Apellido"),
            ("Identificación", "C.I."),
            ("Correo", "Correo"),
            ("Rol", "Rol")
        ]
        
        for texto, valor in tipos_filtro_admin:
            rb = tk.Radiobutton(filtros_frame, text=texto, variable=self.var_admin_filtro_tipo,
                              value=valor, bg="#ffffff")
            rb.pack(side="left", padx=(0, 10))
        
        # Campo de búsqueda
        busqueda_entry_frame = tk.Frame(busqueda_frame, bg="#ffffff")
        busqueda_entry_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(busqueda_entry_frame, text="Buscar:", bg="#ffffff").pack(side="left", padx=(0, 10))
        
        entry_busqueda_admin = ttk.Entry(busqueda_entry_frame, textvariable=self.var_admin_busqueda, width=30)
        entry_busqueda_admin.pack(side="left", padx=(0, 10))
        
        # Botones de búsqueda
        btn_busqueda_frame = tk.Frame(busqueda_entry_frame, bg="#ffffff")
        btn_busqueda_frame.pack(side="left")
        
        ttk.Button(btn_busqueda_frame, text="Buscar", 
                  command=self.buscar_administradores, width=10).pack(side="left", padx=(0, 5))
        ttk.Button(btn_busqueda_frame, text="Limpiar", 
                  command=self.limpiar_busqueda_admin, width=10).pack(side="left")
        
        # Botón para mostrar todos
        ttk.Button(busqueda_frame, text="Mostrar Todos", 
                  command=self.mostrar_todos_administradores, width=15).pack(anchor="e", pady=(5, 0))
        
        # Lista de administradores
        lista_frame = tk.LabelFrame(left_frame, text="Administradores Registrados", 
                                   bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                   padx=15, pady=15)
        lista_frame.pack(fill="both", expand=True)
        
        # Treeview para administradores
        columns = ("ID", "Tipo Doc", "Identificación", "Nombres", "Apellidos", "Correo", "Rol", "Estado")
        self.tree_administradores = ttk.Treeview(lista_frame, columns=columns, show="headings", height=15)
        
        column_widths = {
            "ID": 50,
            "Tipo Doc": 80,
            "Identificación": 100,
            "Nombres": 120,
            "Apellidos": 120,
            "Correo": 150,
            "Rol": 100,
            "Estado": 80
        }
        
        for col in columns:
            self.tree_administradores.heading(col, text=col)
            self.tree_administradores.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_administradores.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient="horizontal", command=self.tree_administradores.xview)
        self.tree_administradores.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree_administradores.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Botones de acción para lista
        action_lista_frame = tk.Frame(lista_frame, bg="#ffffff")
        action_lista_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Button(action_lista_frame, text="Seleccionar", 
                  command=self.seleccionar_administrador, width=12).pack(side="left", padx=5)
        ttk.Button(action_lista_frame, text="Eliminar", 
                  command=self.eliminar_administrador, width=10).pack(side="left", padx=5)
        ttk.Button(action_lista_frame, text="Actualizar", 
                  command=self.mostrar_todos_administradores, width=10).pack(side="right", padx=5)
        
        # --- COLUMNA DERECHA: FORMULARIO ---
        right_frame = tk.Frame(main_frame, bg="#ffffff")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        form_frame = tk.LabelFrame(right_frame, text="Gestión de Administrador", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        form_frame.pack(fill="both", expand=True)
        
        # Variables de estado del formulario
        self.var_form_mode = tk.StringVar(value="nuevo")  # "nuevo" o "editar"
        self.label_form_title = tk.Label(form_frame, text="Nuevo Administrador", 
                                        bg="#ffffff", fg="#2a4f80", font=("Arial", 11, "bold"))
        self.label_form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Grid para formulario
        row = 1
        
        # ID (solo visible en modo edición)
        self.label_admin_id = tk.Label(form_frame, text="ID:", bg="#ffffff", font=("Arial", 10, "bold"))
        self.label_admin_id.grid(row=row, column=0, sticky="w", pady=5)
        self.label_admin_id_val = tk.Label(form_frame, textvariable=self.var_admin_id, 
                                          bg="#ffffff", fg="#666666")
        self.label_admin_id_val.grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Tipo de documento
        tk.Label(form_frame, text="Tipo Documento:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        tipo_doc_combo = ttk.Combobox(form_frame, textvariable=self.var_admin_tipo_doc, 
                                     values=["Cédula", "Pasaporte", "RUC", "Carnet Extranjería"], 
                                     state="readonly", width=20)
        tipo_doc_combo.grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Identificación
        tk.Label(form_frame, text="Identificación:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_admin_identificacion, width=25).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Nombres
        tk.Label(form_frame, text="Nombres:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_admin_nombres, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Apellidos
        tk.Label(form_frame, text="Apellidos:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_admin_apellidos, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Correo
        tk.Label(form_frame, text="Correo Electrónico:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_admin_correo, width=30).grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Contraseña
        tk.Label(form_frame, text="Contraseña:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        password_frame = tk.Frame(form_frame, bg="#ffffff")
        password_frame.grid(row=row, column=1, sticky="w", pady=5)
        
        self.entry_admin_password = ttk.Entry(password_frame, textvariable=self.var_admin_password, 
                                             show="*", width=25)
        self.entry_admin_password.pack(side="left")
        
        # Checkbox para mostrar contraseña
        check_show = tk.Checkbutton(password_frame, text="Mostrar", variable=self.var_admin_show_password,
                                   command=self.toggle_show_password_admin, bg="#ffffff")
        check_show.pack(side="left", padx=(10, 0))
        row += 1
        
        # Rol
        tk.Label(form_frame, text="Rol:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
        rol_combo = ttk.Combobox(form_frame, textvariable=self.var_admin_rol, 
                                values=["Administrador", "Super Administrador", "Soporte", "Auditor"], 
                                state="readonly", width=20)
        rol_combo.grid(row=row, column=1, sticky="w", pady=5, padx=(0, 20))
        row += 1
        
        # Botones del formulario
        btn_form_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_form_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_form_frame, text="Nuevo", 
                  command=self.nuevo_administrador, width=10).pack(side="left", padx=5)
        ttk.Button(btn_form_frame, text="Guardar", 
                  command=self.guardar_administrador, width=10).pack(side="left", padx=5)
        ttk.Button(btn_form_frame, text="Cancelar", 
                  command=self.cancelar_form_admin, width=10).pack(side="left", padx=5)
        ttk.Button(btn_form_frame, text="Generar Contraseña", 
                  command=self.generar_password_admin, width=15).pack(side="left", padx=5)
        
        # Información de estado
        self.label_admin_estado = tk.Label(form_frame, text="", bg="#ffffff", fg="green", font=("Arial", 10))
        self.label_admin_estado.grid(row=row+1, column=0, columnspan=2, pady=(5, 0))
        
        # Cargar administradores inicialmente
        self.mostrar_todos_administradores()
        self.nuevo_administrador()  # Iniciar en modo nuevo
    
        # ─────────────────────────────
    # MÉTODOS PARA GESTIÓN DE ADMINISTRADORES
    # ─────────────────────────────
    
    def toggle_show_password_admin(self):
        """Alterna entre mostrar y ocultar la contraseña de administrador"""
        if self.var_admin_show_password.get():
            self.entry_admin_password.config(show="")
        else:
            self.entry_admin_password.config(show="*")
    
    def buscar_administradores(self):
        """Busca administradores según los filtros seleccionados"""
        tipo_filtro = self.var_admin_filtro_tipo.get()
        texto_busqueda = self.var_admin_busqueda.get().strip().lower()
        
        if not texto_busqueda:
            self.mostrar_todos_administradores()
            return
        
        # Obtener todos los administradores
        administradores = self.admin_menu.obtener_todos_administradores()
        
        if not administradores:
            self.label_admin_estado.config(text="No hay administradores registrados", fg="orange")
            return
        
        # Filtrar administradores
        administradores_filtrados = []
        
        for admin in administradores:
            if tipo_filtro == "todos":
                # Buscar en todos los campos
                campos = [
                    admin.get('Nombre', ''),
                    admin.get('Apellido', ''),
                    admin.get('C.I.', ''),
                    admin.get('Correo', ''),
                    admin.get('Rol', '')
                ]
                if any(texto_busqueda in str(campo).lower() for campo in campos if campo):
                    administradores_filtrados.append(admin)
            else:
                # Buscar en campo específico
                campo = admin.get(tipo_filtro, '')
                if texto_busqueda in str(campo).lower():
                    administradores_filtrados.append(admin)
        
        # Actualizar treeview
        self.actualizar_treeview_administradores(administradores_filtrados)
        
        # Mostrar mensaje de resultados
        self.label_admin_estado.config(
            text=f"Resultados: {len(administradores_filtrados)} administradores encontrados",
            fg="blue"
        )
    
    def mostrar_todos_administradores(self):
        """Muestra todos los administradores en el treeview"""
        administradores = self.admin_menu.obtener_todos_administradores()
        self.actualizar_treeview_administradores(administradores)
        self.label_admin_estado.config(
            text=f"Total de administradores: {len(administradores)}",
            fg="green"
        )
    
    def actualizar_treeview_administradores(self, administradores):
        """Actualiza el treeview con la lista de administradores"""
        # Limpiar treeview
        for item in self.tree_administradores.get_children():
            self.tree_administradores.delete(item)
        
        # Insertar administradores
        for i, admin in enumerate(administradores, 1):
            # Determinar tipo de documento basado en el formato de C.I.
            ci = admin.get('C.I.', '')
            if ci == ".":
                tipo_doc = "Sistema"
            elif ci.isdigit() and len(ci) == 10:
                tipo_doc = "Cédula"
            else:
                tipo_doc = "Pasaporte"
            
            self.tree_administradores.insert("", "end", values=(
                i,
                tipo_doc,
                ci,
                admin.get('Nombre', ''),
                admin.get('Apellido', ''),
                admin.get('Correo', ''),
                admin.get('Rol', 'Sistema'),
                'Activo'
            ))

    def inicializar_archivo_admin(self):
        """Inicializa el archivo admin.json si no existe"""
        admin_path = os.path.join(self.base_dir, "..", "..", "data", "registros", "admin.json")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(admin_path), exist_ok=True)
        
        if not os.path.exists(admin_path):
            admin_por_defecto = {
                "Correo": "admin@system.com",
                "Contraseña": "admin",
                "Nombre": "Admin",
                "Apellido": "Sistema",
                "C.I.": ".",
                "Dirección": ".",
                "Teléfono": ".",
                "Género": "Prefiero no decirlo",
                "Rol": "Sistema"
            }
            
            with open(admin_path, 'w', encoding='utf-8') as f:
                json.dump(admin_por_defecto, f, indent=4, ensure_ascii=False)
            
            print(f"Archivo admin.json creado en: {admin_path}")
    
    def limpiar_busqueda_admin(self):
        """Limpia los campos de búsqueda de administradores"""
        self.var_admin_busqueda.set("")
        self.var_admin_filtro_tipo.set("todos")
        self.mostrar_todos_administradores()
    
    def seleccionar_administrador(self):
        """Carga los datos del administrador seleccionado en el formulario"""
        selected_item = self.tree_administradores.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar", "Seleccione un administrador de la lista")
            return
        
        item = self.tree_administradores.item(selected_item[0])
        valores = item['values']
        
        if not valores or len(valores) < 8:
            return
        
        # Obtener identificación del administrador
        identificacion = valores[2]
        
        # Obtener administrador completo
        administrador = self.admin_menu.obtener_administrador_por_ci(identificacion)
        
        if not administrador:
            messagebox.showerror("Error", "No se pudo cargar la información del administrador")
            return
        
        # Cambiar a modo edición
        self.var_form_mode.set("editar")
        self.label_form_title.config(text="Editar Administrador")
        
        # Mostrar ID
        self.label_admin_id.config(state="normal")
        self.label_admin_id_val.config(state="normal")
        
        # Llenar formulario
        self.var_admin_id.set(identificacion)
        self.var_admin_tipo_doc.set("Cédula" if identificacion.isdigit() and len(identificacion) == 10 else "Pasaporte")
        self.var_admin_identificacion.set(identificacion)
        self.var_admin_nombres.set(administrador.get('Nombre', ''))
        self.var_admin_apellidos.set(administrador.get('Apellido', ''))
        self.var_admin_correo.set(administrador.get('Correo', ''))
        self.var_admin_password.set(administrador.get('Contraseña', ''))
        self.var_admin_rol.set(administrador.get('Rol', 'Administrador'))
        self.var_admin_show_password.set(False)
        self.entry_admin_password.config(show="*")
        
        self.label_admin_estado.config(
            text=f"Editando administrador: {administrador.get('Nombre', '')} {administrador.get('Apellido', '')}",
            fg="orange"
        )
    
    def nuevo_administrador(self):
        """Prepara el formulario para un nuevo administrador"""
        self.var_form_mode.set("nuevo")
        self.label_form_title.config(text="Nuevo Administrador")
        
        # Ocultar ID
        self.label_admin_id.config(state="disabled")
        self.label_admin_id_val.config(state="disabled")
        
        # Limpiar formulario
        self.var_admin_id.set("")
        self.var_admin_tipo_doc.set("Cédula")
        self.var_admin_identificacion.set("")
        self.var_admin_nombres.set("")
        self.var_admin_apellidos.set("")
        self.var_admin_correo.set("")
        self.var_admin_password.set("")
        self.var_admin_rol.set("Administrador")
        self.var_admin_show_password.set(False)
        self.entry_admin_password.config(show="*")
        
        self.label_admin_estado.config(
            text="Complete los datos del nuevo administrador",
            fg="blue"
        )
    
    def guardar_administrador(self):
        """Guarda los datos del administrador (nuevo o editado)"""
        # Validar campos obligatorios
        campos_obligatorios = [
            ("Tipo Documento", self.var_admin_tipo_doc.get().strip()),
            ("Identificación", self.var_admin_identificacion.get().strip()),
            ("Nombres", self.var_admin_nombres.get().strip()),
            ("Apellidos", self.var_admin_apellidos.get().strip()),
            ("Correo", self.var_admin_correo.get().strip()),
            ("Contraseña", self.var_admin_password.get().strip()),
            ("Rol", self.var_admin_rol.get().strip())
        ]
        
        campos_vacios = [nombre for nombre, valor in campos_obligatorios if not valor]
        if campos_vacios:
            messagebox.showerror("Error", f"Campos obligatorios vacíos:\n{', '.join(campos_vacios)}")
            return
        
        # Validar formato de correo
        correo = self.var_admin_correo.get().strip()
        if "@" not in correo or "." not in correo:
            if not messagebox.askyesno("Confirmar", 
                                      "El correo electrónico no parece tener un formato válido.\n"
                                      "¿Desea continuar de todos modos?"):
                return
        
        # Validar longitud de contraseña
        password = self.var_admin_password.get().strip()
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        # Preparar datos
        datos_admin = {
            'C.I.': self.var_admin_identificacion.get().strip(),
            'Nombre': self.var_admin_nombres.get().strip(),
            'Apellido': self.var_admin_apellidos.get().strip(),
            'Correo': correo,
            'Contraseña': password,
            'Rol': self.var_admin_rol.get().strip(),
            'tipoDocumento': self.var_admin_tipo_doc.get().strip()
        }
        
        # Campos adicionales con valores por defecto
        campos_adicionales = {
            'Dirección': '.',
            'Teléfono': '.',
            'Género': 'Prefiero no decirlo'
        }
        
        datos_admin.update(campos_adicionales)
        
        # Guardar según el modo
        if self.var_form_mode.get() == "nuevo":
            resultado = self.admin_menu.agregar_administrador(datos_admin)
        else:  # modo editar
            resultado = self.admin_menu.modificar_administrador(datos_admin)
        
        if resultado["success"]:
            messagebox.showinfo("Éxito", resultado["message"])
            self.mostrar_todos_administradores()
            self.nuevo_administrador()  # Volver a modo nuevo
        else:
            messagebox.showerror("Error", resultado["message"])
    
    def eliminar_administrador(self):
        """Elimina el administrador seleccionado"""
        selected_item = self.tree_administradores.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar", "Seleccione un administrador para eliminar")
            return
        
        item = self.tree_administradores.item(selected_item[0])
        valores = item['values']
        
        if not valores or len(valores) < 8:
            return
        
        identificacion = valores[2]
        nombres = valores[3]
        apellidos = valores[4]
        rol = valores[6]
        
        # No permitir eliminar al administrador principal del sistema
        if rol == "Sistema":
            messagebox.showerror("Error", "No se puede eliminar al administrador principal del sistema")
            return
        
        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                     f"¿Está seguro de eliminar al administrador:\n\n"
                                     f"{nombres} {apellidos}\n"
                                     f"Rol: {rol}\n"
                                     f"Identificación: {identificacion}\n\n"
                                     f"Esta acción no se puede deshacer.")
        
        if confirm:
            resultado = self.admin_menu.eliminar_administrador(identificacion)
            
            if resultado["success"]:
                messagebox.showinfo("Éxito", resultado["message"])
                self.mostrar_todos_administradores()
                self.nuevo_administrador()  # Volver a modo nuevo
            else:
                messagebox.showerror("Error", resultado["message"])
    
    def cancelar_form_admin(self):
        """Cancela la operación actual y vuelve al modo nuevo"""
        self.nuevo_administrador()
    
    def generar_password_admin(self):
        """Genera una nueva contraseña aleatoria para administradores"""
        import random
        import string
        
        # Generar contraseña segura de 10 caracteres
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        nueva_password = ''.join(random.choice(caracteres) for _ in range(10))
        
        self.var_admin_password.set(nueva_password)
        messagebox.showinfo("Nueva Contraseña", 
                           f"Contraseña generada: {nueva_password}\n\n"
                           f"Guarde esta contraseña en un lugar seguro.")
        
    def cargar_administradores_en_treeview(self):
        """Carga los administradores desde el archivo JSON correcto"""
        # Limpiar treeview
        for item in self.tree_administradores.get_children():
            self.tree_administradores.delete(item)
        
        # Cargar administradores desde JSON - Ruta corregida
        admin_path = os.path.join(self.base_dir, "..", "..", "data", "registros", "admin.json")
        
        if os.path.exists(admin_path):
            try:
                with open(admin_path, 'r', encoding='utf-8') as f:
                    contenido = f.read().strip()
                    
                    if contenido:
                        # Intentar cargar como lista
                        try:
                            administradores = json.loads(contenido)
                            if isinstance(administradores, dict):
                                administradores = [administradores]
                        except:
                            # Si falla, intentar cargar como diccionario
                            try:
                                administradores = [json.loads(contenido)]
                            except:
                                administradores = []
                        
                        for i, admin in enumerate(administradores, 1):
                            ci = admin.get('C.I.', '')
                            tipo_doc = "Cédula" if ci.isdigit() and len(ci) == 10 else "Pasaporte"
                            
                            self.tree_administradores.insert("", "end", values=(
                                i,
                                tipo_doc,
                                ci,
                                admin.get('Nombre', ''),
                                admin.get('Apellido', ''),
                                admin.get('Correo', ''),
                                admin.get('Rol', 'Sistema'),
                                'Activo'
                            ))
            except Exception as e:
                print(f"Error al cargar administradores: {e}")
    
    def _crear_tab_oferta(self):
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.tab_oferta, bg="#ffffff")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para scroll horizontal y vertical
        canvas = tk.Canvas(main_frame, bg="#ffffff", highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Contenido de la pestaña
        content_frame = tk.Frame(scrollable_frame, bg="#ffffff", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Gestión de Oferta Académica", 
                 font=("Arial", 16, "bold"), fg="#2a4f80", bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Formulario para crear oferta (campos iguales a oferta.csv)
        form_frame = tk.LabelFrame(content_frame, text="Crear Nueva Oferta Académica", 
                                  bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                  padx=15, pady=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Campos del formulario según oferta.csv
        campos = [
            ("IES ID:", self.var_ies_id),
            ("IES Nombre:", self.var_ies_nombre),
            ("Carrera:", self.var_carrera_nombre),
            ("Área:", self.var_area_nombre),
            ("Subárea:", self.var_subarea_nombre),
            ("Nivel:", self.var_nivel),
            ("Modalidad:", self.var_modalidad),
            ("Jornada:", self.var_jornada),
            ("Total Cupos:", self.var_cupos_total),
            ("Focalizada (S/N):", self.var_focalizada)
        ]
        
        for i, (label, variable) in enumerate(campos):
            tk.Label(form_frame, text=label, bg="#ffffff").grid(row=i, column=0, sticky="w", pady=5)
            ttk.Entry(form_frame, textvariable=variable, width=30).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Crear Oferta", 
                  command=self.crear_oferta).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", 
                  command=self.limpiar_form_oferta).pack(side="left", padx=5)
        
        # Lista de ofertas
        lista_frame = tk.LabelFrame(content_frame, text="Ofertas Académicas Registradas", 
                                   bg="#ffffff", fg="#2a4f80", font=("Arial", 12, "bold"),
                                   padx=15, pady=15)
        lista_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Treeview para ofertas (más columnas)
        columns = (
            "ID", "IES ID", "IES Nombre", "Carrera", "Área", "Subárea",
            "Nivel", "Modalidad", "Jornada", "Total Cupos", "Focalizada"
        )
        self.tree_ofertas = ttk.Treeview(lista_frame, columns=columns, show="headings", height=10)
        
        # Configurar anchos de columnas
        column_widths = {
            "ID": 50,
            "IES ID": 70,
            "IES Nombre": 150,
            "Carrera": 180,
            "Área": 120,
            "Subárea": 100,
            "Nivel": 80,
            "Modalidad": 80,
            "Jornada": 80,
            "Total Cupos": 80,
            "Focalizada": 70
        }
        
        for col in columns:
            self.tree_ofertas.heading(col, text=col)
            self.tree_ofertas.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar_tree = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree_ofertas.yview)
        h_scrollbar_tree = ttk.Scrollbar(lista_frame, orient="horizontal", command=self.tree_ofertas.xview)
        self.tree_ofertas.configure(yscrollcommand=v_scrollbar_tree.set, xscrollcommand=h_scrollbar_tree.set)
        
        self.tree_ofertas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar_tree.grid(row=0, column=1, sticky="ns")
        h_scrollbar_tree.grid(row=1, column=0, sticky="ew")
        
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Botones de acción
        action_frame = tk.Frame(lista_frame, bg="#ffffff")
        action_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Button(action_frame, text="Eliminar Oferta", 
                  command=self.eliminar_oferta).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Actualizar Lista", 
                  command=self.actualizar_lista_ofertas).pack(side="left", padx=5)
        
        # Cargar lista inicial de ofertas
        self.actualizar_lista_ofertas()
    
    # ─────────────────────────────
    # MÉTODOS PARA PERÍODOS
    # ─────────────────────────────
    def agregar_periodo(self):
        try:
            nombre = self.var_periodo_nombre.get().strip()
            fecha_inicio = self.var_periodo_inicio.get().strip()
            fecha_fin = self.var_periodo_fin.get().strip()
            
            if not nombre or not fecha_inicio or not fecha_fin:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            # Validar formato de fecha
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            # Agregar usando AdminMenu
            resultado = self.admin_menu.agregar_periodo(nombre, fecha_inicio, fecha_fin)
            
            if resultado["success"]:
                messagebox.showinfo("Éxito", "Período agregado correctamente")
                self.limpiar_form_periodo()
                self.actualizar_lista_periodos()
            else:
                messagebox.showerror("Error", resultado["message"])
                
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar período: {str(e)}")
    
    def eliminar_periodo(self):
        selected_item = self.tree_periodos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un período para eliminar")
            return
        
        item = self.tree_periodos.item(selected_item[0])
        periodo_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el período {periodo_id}?")
        if confirm:
            resultado = self.admin_menu.eliminar_periodo(periodo_id)
            if resultado["success"]:
                messagebox.showinfo("Éxito", "Período eliminado correctamente")
                self.actualizar_lista_periodos()
            else:
                messagebox.showerror("Error", resultado["message"])
    
    def actualizar_lista_periodos(self):
        # Limpiar treeview
        for item in self.tree_periodos.get_children():
            self.tree_periodos.delete(item)
        
        # Obtener y mostrar períodos
        periodos = self.admin_menu.obtener_periodos()
        for periodo in periodos:
            # Calcular duración
            try:
                inicio = datetime.strptime(periodo['fecha_inicio'], "%Y-%m-%d")
                fin = datetime.strptime(periodo['fecha_fin'], "%Y-%m-%d")
                duracion = (fin - inicio).days
                estado = periodo.get('estado', 'ABIERTO')
            except:
                duracion = 0
                estado = 'ERROR'
            
            self.tree_periodos.insert("", "end", values=(
                periodo['id'],
                periodo.get('nombre', ''),
                periodo['fecha_inicio'],
                periodo['fecha_fin'],
                estado,
                f"{duracion} días"
            ))
    
    def limpiar_form_periodo(self):
        self.var_periodo_nombre.set("")
        self.var_periodo_inicio.set("")
        self.var_periodo_fin.set("")
    
    # ─────────────────────────────
    # MÉTODOS PARA OFERTAS
    # ─────────────────────────────
    def crear_oferta(self):
        try:
            # Validar campos requeridos
            campos_requeridos = [
                ('IES ID', self.var_ies_id.get().strip()),
                ('IES Nombre', self.var_ies_nombre.get().strip()),
                ('Carrera', self.var_carrera_nombre.get().strip()),
                ('Total Cupos', self.var_cupos_total.get().strip())
            ]
            
            campos_vacios = [nombre for nombre, valor in campos_requeridos if not valor]
            if campos_vacios:
                messagebox.showerror("Error", f"Campos requeridos vacíos: {', '.join(campos_vacios)}")
                return
            
            try:
                cupos = int(self.var_cupos_total.get())
                if cupos <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Los cupos deben ser un número entero positivo")
                return
            
            # Crear diccionario con todos los campos de oferta.csv
            datos_oferta = {
                'IES_ID': self.var_ies_id.get(),
                'IES_NOMBRE_INSTIT': self.var_ies_nombre.get(),
                'CAR_NOMBRE_CARRERA': self.var_carrera_nombre.get(),
                'AREA_NOMBRE': self.var_area_nombre.get() or '',
                'SUBAREA_NOMBRE': self.var_subarea_nombre.get() or '',
                'NIVEL': self.var_nivel.get() or 'TERCER NIVEL',
                'MODALIDAD': self.var_modalidad.get() or 'PRESENCIAL',
                'JORNADA': self.var_jornada.get() or 'NO APLICA JORNADA',
                'CUS_TOTAL_CUPOS': cupos,
                'FOCALIZADA': self.var_focalizada.get().upper() or 'N',
                # Campos con valores por defecto
                'IES_ID_SNIESE': '1016',
                'PRO_NOMBRE': 'MANABÍ',
                'CAN_NOMBRE': self.var_carrera_nombre.get()[:20] if self.var_carrera_nombre.get() else '',
                'PRQ_NOMBRE': self.var_carrera_nombre.get()[:20] if self.var_carrera_nombre.get() else '',
                'OFA_TITULO': '',
                'OFA_ID': '',
                'CUS_ID': '',
                'CUS_CUPOS_NIVELACION': '0',
                'CUS_CUPOS_PRIMER_SEMESTRE': '0',
                'CUS_CUPOS_PC': '0',
                'DESCRIPCION_TIPO_CUPO': 'CUPOS_NIVELACIÓN' if cupos > 0 else 'CUPOS_PRIMER_SEMESTRE'
            }
            
            # Crear oferta usando AdminMenu
            resultado = self.admin_menu.crear_oferta(datos_oferta)
            
            if resultado["success"]:
                messagebox.showinfo("Éxito", "Oferta creada correctamente")
                self.limpiar_form_oferta()
                self.actualizar_lista_ofertas()
            else:
                messagebox.showerror("Error", resultado["message"])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear oferta: {str(e)}")
    
    def eliminar_oferta(self):
        selected_item = self.tree_ofertas.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una oferta para eliminar")
            return
        
        item = self.tree_ofertas.item(selected_item[0])
        oferta_id = item['values'][0]
        
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la oferta {oferta_id}?")
        if confirm:
            resultado = self.admin_menu.eliminar_oferta(oferta_id)
            if resultado["success"]:
                messagebox.showinfo("Éxito", "Oferta eliminada correctamente")
                self.actualizar_lista_ofertas()
            else:
                messagebox.showerror("Error", resultado["message"])
    
    def actualizar_lista_ofertas(self):
        # Limpiar treeview
        for item in self.tree_ofertas.get_children():
            self.tree_ofertas.delete(item)
        
        # Obtener y mostrar ofertas
        ofertas = self.admin_menu.obtener_ofertas()
        for oferta in ofertas:
            self.tree_ofertas.insert("", "end", values=(
                oferta.get('id', ''),
                oferta.get('IES_ID', ''),
                oferta.get('IES_NOMBRE_INSTIT', ''),
                oferta.get('CAR_NOMBRE_CARRERA', ''),
                oferta.get('AREA_NOMBRE', ''),
                oferta.get('SUBAREA_NOMBRE', ''),
                oferta.get('NIVEL', ''),
                oferta.get('MODALIDAD', ''),
                oferta.get('JORNADA', ''),
                oferta.get('CUS_TOTAL_CUPOS', ''),
                oferta.get('FOCALIZADA', '')
            ))
    
    def limpiar_form_oferta(self):
        self.var_ies_id.set("")
        self.var_ies_nombre.set("")
        self.var_carrera_nombre.set("")
        self.var_area_nombre.set("")
        self.var_subarea_nombre.set("")
        self.var_nivel.set("TERCER NIVEL")
        self.var_modalidad.set("PRESENCIAL")
        self.var_jornada.set("NO APLICA JORNADA")
        self.var_cupos_total.set("")
        self.var_focalizada.set("N")
    
    # ─────────────────────────────
    # MÉTODOS PARA ARCHIVOS CSV
    # ─────────────────────────────
    def buscar_archivo(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.var_file_path.set(filename)
    
    def subir_oferta_csv(self):
        filepath = self.var_file_path.get().strip()
        if not filepath:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return
        
        try:
            resultado = self.admin_menu.subir_oferta_csv(filepath)
            if resultado["success"]:
                messagebox.showinfo("Éxito", resultado["message"])
                self.actualizar_lista_ofertas()
            else:
                messagebox.showerror("Error", resultado["message"])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al subir archivo: {str(e)}")

# Clase AdminMenu que maneja la lógica de negocio
class AdminMenu:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "..", "..", "data", "universidad")
        self.postulaciones_dir = os.path.join(self.base_dir, "..", "..", "data", "postulaciones")
        
        # Crear directorios si no existen
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.postulaciones_dir, exist_ok=True)
        
        self.periodos_file = os.path.join(self.data_dir, "periodos.csv")
        self.ofertas_file = os.path.join(self.data_dir, "oferta_academica.csv")
        self.postulaciones_config_file = os.path.join(self.data_dir, "postulaciones_config.csv")

        # Inicializar archivos si no existen
        self._inicializar_archivos()
        self.gestor_admin = GestorAdministradores()
    
    def _inicializar_archivos(self):
        # Inicializar archivo de períodos
        if not os.path.exists(self.periodos_file):
            with open(self.periodos_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_creacion'])
        
        # Inicializar archivo de ofertas (con las mismas columnas que oferta.csv)
        if not os.path.exists(self.ofertas_file):
            with open(self.ofertas_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'id', 'IES_ID', 'IES_ID_SNIESE', 'IES_NOMBRE_INSTIT', 'PRO_NOMBRE',
                    'CAN_NOMBRE', 'PRQ_NOMBRE', 'CAR_NOMBRE_CARRERA', 'AREA_NOMBRE',
                    'SUBAREA_NOMBRE', 'NIVEL', 'MODALIDAD', 'JORNADA', 'OFA_TITULO',
                    'OFA_ID', 'CUS_ID', 'CUS_CUPOS_NIVELACION', 'CUS_CUPOS_PRIMER_SEMESTRE',
                    'CUS_CUPOS_PC', 'CUS_TOTAL_CUPOS', 'DESCRIPCION_TIPO_CUPO', 'FOCALIZADA',
                    'fecha_registro'
                ])

        # Inicializar archivo de configuración de postulaciones
        if not os.path.exists(self.postulaciones_config_file):
            with open(self.postulaciones_config_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    'id', 'periodo_id', 'periodo_nombre', 'intenciones', 
                    'fecha_limite', 'hora_limite', 'fecha_creacion', 'estado'
                ])
    
    # ─────────────────────────────
    # MÉTODOS PARA PERÍODOS
    # ─────────────────────────────
    def obtener_periodos(self):
        periodos = []
        try:
            if os.path.exists(self.periodos_file):
                with open(self.periodos_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    periodos = list(reader)
        except Exception as e:
            print(f"Error al leer períodos: {e}")
        
        return periodos
    
    def agregar_periodo(self, nombre, fecha_inicio, fecha_fin):
        try:
            # Validar fechas
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            if fecha_inicio_dt >= fecha_fin_dt:
                return {"success": False, "message": "La fecha de inicio debe ser anterior a la fecha de fin"}
            
            # Obtener siguiente ID
            periodos = self.obtener_periodos()
            if periodos:
                # Encontrar el máximo ID numérico
                max_id = 0
                for p in periodos:
                    try:
                        id_num = int(p['id'])
                        if id_num > max_id:
                            max_id = id_num
                    except ValueError:
                        continue
                new_id = str(max_id + 1)
            else:
                new_id = "1"
            
            # Determinar estado
            hoy = datetime.now().date()
            if fecha_inicio_dt.date() > hoy:
                estado = "ABIERTO" #planificado
            else:
                estado = "ABIERTO"
            
            # Guardar período
            with open(self.periodos_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    new_id,
                    nombre,
                    fecha_inicio,
                    fecha_fin,
                    estado,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
            
            return {"success": True, "message": "Período agregado correctamente", "id": new_id}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def eliminar_periodo(self, periodo_id):
        try:
            periodos = self.obtener_periodos()
            
            # Filtrar el período a eliminar
            periodos_filtrados = [p for p in periodos if p['id'] != str(periodo_id)]
            
            if len(periodos_filtrados) == len(periodos):
                return {"success": False, "message": "Período no encontrado"}
            
            # Guardar períodos actualizados
            with open(self.periodos_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_creacion'])
                writer.writeheader()
                writer.writerows(periodos_filtrados)
            
            return {"success": True, "message": "Período eliminado correctamente"}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    # ─────────────────────────────
    # MÉTODOS PARA OFERTAS
    # ─────────────────────────────
    def obtener_ofertas(self):
        ofertas = []
        try:
            if os.path.exists(self.ofertas_file):
                with open(self.ofertas_file, 'r', encoding='utf-8', newline='') as f:
                    # Detecta automáticamente el delimitador
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)  # Regresa al inicio del archivo
                    reader = csv.DictReader(f, dialect=dialect)
                    ofertas = list(reader)
        except Exception as e:
            print(f"Error al leer ofertas: {e}")
            # Si falla la detección, intenta con punto y coma
            try:
                with open(self.ofertas_file, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    ofertas = list(reader)
            except Exception as e2:
                print(f"Error al leer ofertas con ;: {e2}")
        
        return ofertas
    
    def crear_oferta(self, datos_oferta):
        try:
            # Validar datos mínimos
            required_fields = ['IES_ID', 'IES_NOMBRE_INSTIT', 'CAR_NOMBRE_CARRERA', 'CUS_TOTAL_CUPOS']
            for field in required_fields:
                if field not in datos_oferta or not datos_oferta[field]:
                    return {"success": False, "message": f"Campo requerido: {field}"}
            
            # Obtener siguiente ID
            ofertas = self.obtener_ofertas()
            if ofertas:
                # Encontrar el máximo ID numérico
                max_id = 0
                for o in ofertas:
                    try:
                        id_num = int(o['id']) if 'id' in o and o['id'].isdigit() else 0
                        if id_num > max_id:
                            max_id = id_num
                    except ValueError:
                        continue
                new_id = str(max_id + 1)
            else:
                new_id = "1"
            
            # Preparar datos completos con valores por defecto
            datos_completos = {
                'id': new_id,
                'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Campos con valores por defecto si no están en datos_oferta
            campos_con_valores = {
                'IES_ID_SNIESE': datos_oferta.get('IES_ID_SNIESE', '1016'),
                'PRO_NOMBRE': datos_oferta.get('PRO_NOMBRE', 'MANABÍ'),
                'CAN_NOMBRE': datos_oferta.get('CAN_NOMBRE', datos_oferta.get('CAR_NOMBRE_CARRERA', '')[:20]),
                'PRQ_NOMBRE': datos_oferta.get('PRQ_NOMBRE', datos_oferta.get('CAR_NOMBRE_CARRERA', '')[:20]),
                'AREA_NOMBRE': datos_oferta.get('AREA_NOMBRE', ''),
                'SUBAREA_NOMBRE': datos_oferta.get('SUBAREA_NOMBRE', ''),
                'NIVEL': datos_oferta.get('NIVEL', 'TERCER NIVEL'),
                'MODALIDAD': datos_oferta.get('MODALIDAD', 'PRESENCIAL'),
                'JORNADA': datos_oferta.get('JORNADA', 'NO APLICA JORNADA'),
                'OFA_TITULO': datos_oferta.get('OFA_TITULO', ''),
                'OFA_ID': datos_oferta.get('OFA_ID', ''),
                'CUS_ID': datos_oferta.get('CUS_ID', ''),
                'CUS_CUPOS_NIVELACION': datos_oferta.get('CUS_CUPOS_NIVELACION', '0'),
                'CUS_CUPOS_PRIMER_SEMESTRE': datos_oferta.get('CUS_CUPOS_PRIMER_SEMESTRE', '0'),
                'CUS_CUPOS_PC': datos_oferta.get('CUS_CUPOS_PC', '0'),
                'DESCRIPCION_TIPO_CUPO': datos_oferta.get('DESCRIPCION_TIPO_CUPO', 'CUPOS_NIVELACIÓN'),
                'FOCALIZADA': datos_oferta.get('FOCALIZADA', 'N').upper()
            }
            
            # Combinar todos los datos
            datos_completos.update(datos_oferta)
            datos_completos.update(campos_con_valores)
            
            # Escribir en CSV (usando todos los campos en orden)
            fieldnames = [
                'id', 'IES_ID', 'IES_ID_SNIESE', 'IES_NOMBRE_INSTIT', 'PRO_NOMBRE',
                'CAN_NOMBRE', 'PRQ_NOMBRE', 'CAR_NOMBRE_CARRERA', 'AREA_NOMBRE',
                'SUBAREA_NOMBRE', 'NIVEL', 'MODALIDAD', 'JORNADA', 'OFA_TITULO',
                'OFA_ID', 'CUS_ID', 'CUS_CUPOS_NIVELACION', 'CUS_CUPOS_PRIMER_SEMESTRE',
                'CUS_CUPOS_PC', 'CUS_TOTAL_CUPOS', 'DESCRIPCION_TIPO_CUPO', 'FOCALIZADA',
                'fecha_registro'
            ]
            
            with open(self.ofertas_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                
                # Si el archivo está vacío, escribir encabezados
                if f.tell() == 0:
                    writer.writeheader()
                
                # Escribir fila con datos ordenados
                fila_ordenada = {field: datos_completos.get(field, '') for field in fieldnames}
                writer.writerow(fila_ordenada)
            
            return {"success": True, "message": "Oferta creada correctamente", "id": new_id}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def eliminar_oferta(self, oferta_id):
        try:
            ofertas = self.obtener_ofertas()
            
            # Filtrar la oferta a eliminar
            ofertas_filtradas = [o for o in ofertas if o.get('id') != str(oferta_id)]
            
            if len(ofertas_filtradas) == len(ofertas):
                return {"success": False, "message": "Oferta no encontrada"}
            
            # Guardar ofertas actualizadas
            with open(self.ofertas_file, 'w', newline='', encoding='utf-8') as f:
                if ofertas_filtradas:
                    fieldnames = list(ofertas_filtradas[0].keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    writer.writerows(ofertas_filtradas)
            
            return {"success": True, "message": "Oferta eliminada correctamente"}
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def subir_oferta_csv(self, filepath):
        try:
            # Leer archivo CSV
            ofertas_nuevas = []
            with open(filepath, 'r', encoding='utf-8', newline='') as f:
                try:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)  # Regresa al inicio del archivo
                    reader = csv.DictReader(f, dialect=dialect)
                except:
                    # Si no puede detectar, intenta con punto y coma
                    f.seek(0)
                    reader = csv.DictReader(f, delimiter=';')
                
                for row in reader:
                    ofertas_nuevas.append(row)
            
            if not ofertas_nuevas:
                return {"success": False, "message": "El archivo CSV está vacío"}
            
            # Obtener ofertas existentes
            ofertas_existentes = self.obtener_ofertas()
            
            # Generar nuevos IDs
            max_id = 0
            for oferta in ofertas_existentes:
                try:
                    id_num = int(oferta.get('id', 0))
                    max_id = max(max_id, id_num)
                except:
                    pass
            
            # Procesar nuevas ofertas
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ofertas_agregadas = 0
            
            for i, oferta in enumerate(ofertas_nuevas, 1):
                nuevo_id = str(max_id + i)
                
                # Asegurar que tenga todos los campos necesarios
                oferta['id'] = nuevo_id
                
                # Agregar campos faltantes con valores por defecto
                campos_faltantes = {
                    'fecha_registro': fecha_actual,
                    'IES_ID_SNIESE': oferta.get('IES_ID_SNIESE', '1016'),
                    'PRO_NOMBRE': oferta.get('PRO_NOMBRE', 'MANABÍ'),
                    'DESCRIPCION_TIPO_CUPO': oferta.get('DESCRIPCION_TIPO_CUPO', 'CUPOS_NIVELACIÓN'),
                    'FOCALIZADA': oferta.get('FOCALIZADA', 'N').upper()
                }
                
                for campo, valor in campos_faltantes.items():
                    if campo not in oferta or not oferta[campo]:
                        oferta[campo] = valor
                
                # Agregar a existentes
                ofertas_existentes.append(oferta)
                ofertas_agregadas += 1
            
            # Guardar todas las ofertas
            with open(self.ofertas_file, 'w', newline='', encoding='utf-8') as f:
                if ofertas_existentes:
                    fieldnames = list(ofertas_existentes[0].keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    writer.writerows(ofertas_existentes)
            
            return {"success": True, "message": f"Se agregaron {ofertas_agregadas} nuevas ofertas"}
            
        except Exception as e:
            return {"success": False, "message": f"Error al procesar archivo: {str(e)}"}
        
    # ─────────────────────────────
    # MÉTODOS PARA POSTULACIONES
    # ─────────────────────────────
    
    def obtener_postulaciones_config(self):
        """Obtiene todas las configuraciones de postulaciones"""
        configs = []
        try:
            if os.path.exists(self.postulaciones_config_file):
                with open(self.postulaciones_config_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    configs = list(reader)
        except Exception as e:
            print(f"Error al leer configuraciones de postulaciones: {e}")
        
        return configs
    
    def obtener_postulaciones_activas(self):
        """Obtiene postulaciones activas con información del archivo"""
        configs = self.obtener_postulaciones_config()
        postulaciones = []
        
        for config in configs:
            if config.get('estado', '') == 'ACTIVA':
                periodo_id = config.get('periodo_id', '')
                archivo = f"postulacion_{periodo_id}.csv"
                archivo_path = os.path.join(self.postulaciones_dir, archivo)
                
                # Verificar si el archivo existe
                archivo_existe = os.path.exists(archivo_path)
                
                postulacion = {
                    'id': config.get('id', ''),
                    'periodo_id': periodo_id,
                    'periodo_nombre': config.get('periodo_nombre', ''),
                    'intenciones': config.get('intenciones', ''),
                    'fecha_limite': config.get('fecha_limite', ''),
                    'hora_limite': config.get('hora_limite', ''),
                    'fecha_creacion': config.get('fecha_creacion', ''),
                    'estado': 'ACTIVA' if archivo_existe else 'ARCHIVO FALTANTE',
                    'archivo': archivo
                }
                postulaciones.append(postulacion)
        
        return postulaciones
    
    def limpiar_form_postulacion(self):
        """Limpia el formulario de postulación"""
        self.var_postulacion_periodo.set("")
        self.var_postulacion_intenciones.set("")  # Vaciar en lugar de "1"
        
        # Sugerir fecha actual + 30 días
        fecha_sugerida = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.var_postulacion_fecha_limite.set(fecha_sugerida)
        
        self.var_postulacion_hora_limite.set("23:59")
    
    def eliminar_postulacion(self, periodo_id):
        """Elimina una postulación y su archivo correspondiente"""
        try:
            # Obtener configuraciones
            configs = self.obtener_postulaciones_config()
            
            # Buscar y eliminar la configuración
            configs_filtradas = []
            config_encontrada = None
            
            for config in configs:
                if config.get('periodo_id') == str(periodo_id):
                    config_encontrada = config
                else:
                    configs_filtradas.append(config)
            
            if not config_encontrada:
                return {"success": False, "message": "Postulación no encontrada"}
            
            # Eliminar archivo de postulación
            archivo_nombre = f"postulacion_{periodo_id}.csv"
            archivo_path = os.path.join(self.postulaciones_dir, archivo_nombre)
            
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
            
            # Guardar configuraciones actualizadas
            with open(self.postulaciones_config_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'id', 'periodo_id', 'periodo_nombre', 'intenciones', 
                    'fecha_limite', 'hora_limite', 'fecha_creacion', 'estado'
                ], delimiter=';')
                writer.writeheader()
                writer.writerows(configs_filtradas)
            
            # Cambiar estado del período a PLANIFICADO
            self.actualizar_estado_periodo(periodo_id, 'ABIERTO') #PLANIFICADO
            
            return {
                "success": True, 
                "message": f"Postulación eliminada exitosamente. Archivo {archivo_nombre} eliminado."
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def actualizar_estado_periodo(self, periodo_id, nuevo_estado):
        """Actualiza el estado de un período"""
        try:
            periodos = self.obtener_periodos()
            
            for periodo in periodos:
                if periodo.get('id') == str(periodo_id):
                    periodo['estado'] = nuevo_estado
                    break
            
            # Guardar períodos actualizados
            with open(self.periodos_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_creacion'])
                writer.writeheader()
                writer.writerows(periodos)
            
            return True
            
        except Exception as e:
            print(f"Error al actualizar estado del período: {e}")
            return False
        
    def obtener_todos_usuarios(self):
        """Obtiene todos los usuarios del sistema"""
        print("DEBUG: Obteniendo todos los usuarios...")
        
        usuarios = []
        usuarios_path = os.path.join(self.base_dir, "..", "..", "data", "registros", "usuarios_registrados.csv")
        
        print(f"DEBUG: Ruta del archivo: {usuarios_path}")
        print(f"DEBUG: ¿Existe el archivo? {os.path.exists(usuarios_path)}")
        
        if not os.path.exists(usuarios_path):
            print("DEBUG: El archivo no existe")
            return usuarios
        
        try:
            with open(usuarios_path, 'r', encoding='utf-8', newline='') as f:
                # Leer archivo CSV
                reader = csv.DictReader(f)
                print(f"DEBUG: Encabezados encontrados: {reader.fieldnames}")
                
                usuarios_list = list(reader)
                print(f"DEBUG: Número de usuarios leídos: {len(usuarios_list)}")
                
                for i, row in enumerate(usuarios_list, 1):
                    # Asignar ID automático si no existe
                    usuario = dict(row)
                    usuario['id'] = str(i)
                    usuarios.append(usuario)
                    
                    if i <= 3:  # Mostrar solo primeros 3 para depuración
                        print(f"DEBUG: Usuario {i}: {usuario}")
                
                print(f"DEBUG: Total de usuarios procesados: {len(usuarios)}")
                
        except Exception as e:
            print(f"DEBUG: Error al leer usuarios: {e}")
        
        return usuarios
    
    def obtener_usuario_por_id(self, usuario_id):
        """Obtiene un usuario específico por su ID"""
        usuarios = self.obtener_todos_usuarios()
        
        for usuario in usuarios:
            if usuario.get('id') == str(usuario_id):
                return usuario
        
        return None
    
    def obtener_usuario_por_identificacion(self, identificacion):
        """Obtiene un usuario por su identificación"""
        print(f"DEBUG: Buscando usuario con identificación: {identificacion}")
        
        usuarios = self.obtener_todos_usuarios()
        print(f"DEBUG: Total de usuarios encontrados: {len(usuarios)}")
        
        for usuario in usuarios:
            if str(usuario.get('identificacion', '')).strip() == str(identificacion).strip():
                print(f"DEBUG: Usuario encontrado: {usuario}")
                return usuario
        
        print(f"DEBUG: Usuario NO encontrado con identificación: {identificacion}")
        return None
    
    def modificar_usuario(self, datos_usuario):
        """Modifica los datos de un usuario existente por identificación"""
        try:
            identificacion_original = datos_usuario.get('identificacion_original')
            nueva_identificacion = datos_usuario.get('identificacion')
            
            if not identificacion_original:
                return {"success": False, "message": "Identificación original no especificada"}
            
            # Obtener todos los usuarios
            usuarios = self.obtener_todos_usuarios()
            
            # Buscar usuario a modificar
            usuario_index = -1
            for i, usuario in enumerate(usuarios):
                if usuario.get('identificacion') == identificacion_original:
                    usuario_index = i
                    break
            
            if usuario_index == -1:
                return {"success": False, "message": "Usuario no encontrado"}
            
            # Verificar si la nueva identificación ya existe (si cambió)
            if identificacion_original != nueva_identificacion:
                for usuario in usuarios:
                    if usuario.get('identificacion') == nueva_identificacion:
                        return {"success": False, 
                                "message": f"Ya existe otro usuario con la identificación: {nueva_identificacion}"}
            
            # Verificar si el nuevo correo ya existe (excluyendo el usuario actual)
            nuevo_correo = datos_usuario.get('correo')
            for i, usuario in enumerate(usuarios):
                if i != usuario_index and usuario.get('correo') == nuevo_correo:
                    return {"success": False, 
                            "message": f"Ya existe otro usuario con el correo: {nuevo_correo}"}
            
            # Actualizar datos del usuario
            usuarios[usuario_index]['tipoDocumento'] = datos_usuario['tipoDocumento']
            usuarios[usuario_index]['identificacion'] = nueva_identificacion
            usuarios[usuario_index]['nombres'] = datos_usuario['nombres']
            usuarios[usuario_index]['apellidos'] = datos_usuario['apellidos']
            usuarios[usuario_index]['correo'] = nuevo_correo
            usuarios[usuario_index]['contraseña'] = datos_usuario['contraseña']
            
            # Guardar usuarios actualizados
            usuarios_path = os.path.join(self.base_dir, "..", "..", "data", "registros", "usuarios_registrados.csv")
            
            # Definir encabezados en el orden correcto
            fieldnames = ['tipoDocumento', 'identificacion', 'correo', 'nombres', 'apellidos', 'contraseña']
            
            with open(usuarios_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for usuario in usuarios:
                    # Crear diccionario solo con los campos necesarios
                    usuario_data = {
                        'tipoDocumento': usuario.get('tipoDocumento', ''),
                        'identificacion': usuario.get('identificacion', ''),
                        'correo': usuario.get('correo', ''),
                        'nombres': usuario.get('nombres', ''),
                        'apellidos': usuario.get('apellidos', ''),
                        'contraseña': usuario.get('contraseña', '')
                    }
                    writer.writerow(usuario_data)
            
            return {
                "success": True, 
                "message": f"Usuario {datos_usuario['nombres']} {datos_usuario['apellidos']} modificado correctamente"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error al modificar usuario: {str(e)}"}
    
    def eliminar_usuario_por_identificacion(self, identificacion):
        """Elimina un usuario por su identificación"""
        try:
            # Obtener todos los usuarios
            usuarios = self.obtener_todos_usuarios()
            
            # Filtrar usuario a eliminar
            usuarios_filtrados = []
            usuario_eliminado = None
            
            for usuario in usuarios:
                if usuario.get('identificacion') != identificacion:
                    usuarios_filtrados.append(usuario)
                else:
                    usuario_eliminado = usuario
            
            if not usuario_eliminado:
                return {"success": False, "message": "Usuario no encontrado"}
            
            # Guardar usuarios actualizados
            usuarios_path = os.path.join(self.base_dir, "..", "..", "data", "registros", "usuarios_registrados.csv")
            
            if usuarios_filtrados:
                # Definir encabezados en el orden correcto
                fieldnames = ['tipoDocumento', 'identificacion', 'correo', 'nombres', 'apellidos', 'contraseña']
                
                with open(usuarios_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for usuario in usuarios_filtrados:
                        usuario_data = {
                            'tipoDocumento': usuario.get('tipoDocumento', ''),
                            'identificacion': usuario.get('identificacion', ''),
                            'correo': usuario.get('correo', ''),
                            'nombres': usuario.get('nombres', ''),
                            'apellidos': usuario.get('apellidos', ''),
                            'contraseña': usuario.get('contraseña', '')
                        }
                        writer.writerow(usuario_data)
            else:
                # Si no quedan usuarios, crear archivo vacío
                with open(usuarios_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['tipoDocumento', 'identificacion', 'correo', 'nombres', 'apellidos', 'contraseña'])
            
            return {
                "success": True, 
                "message": f"Usuario {usuario_eliminado.get('nombres', '')} {usuario_eliminado.get('apellidos', '')} eliminado correctamente"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar usuario: {str(e)}"}
        
    # ─────────────────────────────
    # MÉTODOS PARA ADMINISTRADORES
    # ─────────────────────────────
    
    def obtener_todos_administradores(self):
        """Obtiene todos los administradores del sistema"""
        return self.gestor_admin.obtener_todos()
    
    def obtener_administrador_por_ci(self, ci):
        """Obtiene un administrador por su C.I."""
        return self.gestor_admin.obtener_por_ci(ci)
    
    def obtener_administrador_por_correo(self, correo):
        """Obtiene un administrador por su correo"""
        return self.gestor_admin.obtener_por_correo(correo)
    
    def agregar_administrador(self, datos_admin):
        """Agrega un nuevo administrador"""
        success, message = self.gestor_admin.agregar(datos_admin)
        return {"success": success, "message": message}
    
    def modificar_administrador(self, datos_admin):
        """Modifica un administrador existente"""
        success, message = self.gestor_admin.modificar(datos_admin)
        return {"success": success, "message": message}
    
    def eliminar_administrador(self, ci):
        """Elimina un administrador por su C.I."""
        success, message = self.gestor_admin.eliminar(ci)
        return {"success": success, "message": message}
    
    def verificar_credenciales_admin(self, correo, contraseña):
        """Verifica las credenciales de un administrador"""
        success, admin = self.gestor_admin.verificar_credenciales(correo, contraseña)
        return success, admin
    
    def generar_password_admin(self):
        """Genera una nueva contraseña segura"""
        return self.gestor_admin.generar_contraseña_segura()