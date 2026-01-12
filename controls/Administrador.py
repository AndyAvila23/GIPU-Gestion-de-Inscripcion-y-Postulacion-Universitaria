
import os
import json
import csv

def mostrar_csv_formateado(ruta_csv, max_width=30):
    if not os.path.exists(ruta_csv):
        print(f"Archivo {ruta_csv} no encontrado.")
        return
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        filas = list(lector)
        if not filas:
            print("(Archivo CSV vacío)")
            return
        
        # Calcular ancho máximo por columna considerando truncamiento
        num_cols = max(len(fila) for fila in filas)
        col_widths = [0] * num_cols
        for fila in filas:
            for i, col in enumerate(fila):
                texto = col.strip()
                texto_corto = (texto[:max_width] + '...') if len(texto) > max_width else texto
                col_widths[i] = max(col_widths[i], len(texto_corto))
        
        # Imprimir filas con columnas alineadas y truncadas si es necesario
        for fila in filas:
            fila_a_imprimir = []
            for i in range(num_cols):
                if i < len(fila):
                    texto = fila[i].strip()
                    if len(texto) > max_width:
                        texto = texto[:max_width] + '...'
                else:
                    texto = ''
                fila_a_imprimir.append(texto.ljust(col_widths[i]))
            print(" | ".join(fila_a_imprimir))


class adminVentana:
    def __init__(self, master=None, iconos=None):
        self.logo = None
        self._crear_contenido()
        self.abrir_modal()

    def _crear_contenido(self):
        print("GIPU - Panel de Administración")
        print("=" * 50)
        logo_path = os.path.join("assets", "img", "Logo_GIPU.png")
        if os.path.exists(logo_path):
            self.logo = "[Logo cargado]"
            print(self.logo)
        else:
            self.logo = "[Logo no encontrado]"
            print(self.logo)
        print("GIPU")
        print("Panel de Administración")
        print("-" * 30)
        print("Presione Enter para abrir herramientas...")
        input()

    def _contenedor(self):
        archivo_oferta = os.path.join("data", "oferta.csv")
        print("\nContenido de oferta.csv:")
        print("-" * 80)
        mostrar_csv_formateado(archivo_oferta)
        print("-" * 80)

    def abrir_modal(self):
        herramienta_modal(self)


class herramienta_modal:
    def __init__(self, master=None):
        self._crear_contenido()

    def _crear_contenido(self):
        while True:
            print("\nHerramientas de Administración")
            print("=" * 40)
            print("1. Gestionar Inscripciones")
            print("2. Gestionar Postulaciones")
            print("3. Gestionar Usuarios")
            print("4. Gestionar Administradores")
            print("5. Mostrar Oferta Académica")
            print("6. Cerrar")
            opcion = input("Seleccione una opción (1-6): ").strip()

            if opcion == "1":
                Admin_menu().Gestionar_inscripciones()
            elif opcion == "2":
                Admin_menu().Gestionar_postulaciones()
            elif opcion == "3":
                Admin_menu().Gestionar_usuarios()
            elif opcion == "4":
                Admin_menu().Gestionar_administradores()
            elif opcion == "5":
                Admin_menu().Mostrar_oferta_academica()
            elif opcion == "6":
                print("Cerrando herramientas...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")


class Admin_menu:
    def __init__(self, frame=None):
        self.frame = frame
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.archivo_usuarios = os.path.join(base_dir, "data", "datos_registro.json")
        self.archivo_administradores = os.path.join(base_dir, "data", "admin.json")

    def Gestionar_inscripciones(self):
        print("\nGestionar Inscripciones")
        print("-" * 25)
        print("Funcionalidad de gestionar inscripciones.")
        input("Presione Enter para continuar...")

    def Gestionar_postulaciones(self):
        print("\nGestionar Postulaciones")
        print("-" * 25)
        
        while True:
            print("Ingrese los datos para la postulación o presione 'S' para salir sin guardar.")
            
            periodo = input("Ingrese el periodo (o 'S' para salir): ").strip()
            if periodo.upper() == 'S':
                print("Salida de Gestionar Postulaciones sin guardar datos.")
                break
            
            porcentaje = input("Ingrese porcentaje de abanderados (o 'S' para salir): ").strip()
            if porcentaje.upper() == 'S':
                print("Salida de Gestionar Postulaciones sin guardar datos.")
                break
            
            if not periodo:
                print("El periodo no puede estar vacío. Intente nuevamente.")
                continue
            if not porcentaje or not porcentaje.replace('.', '', 1).isdigit():
                print("El porcentaje debe ser un número válido. Intente nuevamente.")
                continue
            
            print(f"Periodo establecido: {periodo}")
            print(f"Porcentaje modificado: {porcentaje}")
            
            input("Datos guardados. Presione Enter para continuar...")
            break  # Salir después de completar con éxito

    def Gestionar_usuarios(self):
        data = self._leer_json(self.archivo_usuarios)
        while True:
            print("\nGestionar Usuarios")
            print("=" * 30)
            print("1. Listar usuarios")
            print("2. Buscar usuario")
            print("3. Agregar usuario")
            print("4. Modificar usuario")
            print("5. Eliminar usuario")
            print("6. Volver al menú anterior")
            opcion = input("Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                self._listar(data)
            elif opcion == "2":
                self._buscar(data)
            elif opcion == "3":
                self._agregar(data, self.archivo_usuarios)
            elif opcion == "4":
                self._modificar(data, self.archivo_usuarios)
            elif opcion == "5":
                self._eliminar(data, self.archivo_usuarios)
            elif opcion == "6":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def Gestionar_administradores(self):
        data = self._leer_json(self.archivo_administradores)
        while True:
            print("\nGestionar Administradores")
            print("=" * 30)
            print("1. Listar administradores")
            print("2. Buscar administrador")
            print("3. Agregar administrador")
            print("4. Modificar administrador")
            print("5. Eliminar administrador")
            print("6. Volver al menú anterior")
            opcion = input("Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                self._listar(data)
            elif opcion == "2":
                self._buscar(data)
            elif opcion == "3":
                self._agregar(data, self.archivo_administradores)
            elif opcion == "4":
                self._modificar(data, self.archivo_administradores)
            elif opcion == "5":
                self._eliminar(data, self.archivo_administradores)
            elif opcion == "6":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def Mostrar_oferta_academica(self):
        print("\nMostrar Oferta Académica")
        print("-" * 80)
        archivo_oferta = os.path.join("data", "oferta.csv")
        mostrar_csv_formateado(archivo_oferta)
        print("-" * 80)
        input("Presione Enter para continuar...")

    # Métodos auxiliares para JSON
    
    def _leer_json(self, archivo):
        carpeta = os.path.dirname(archivo)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data = [data]
                    elif not isinstance(data, list):
                        data = []
                    return data
                except json.JSONDecodeError:
                    print(f"Error leyendo {archivo}. Formato JSON inválido.")
                    return []
        else:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []

    def _guardar_json(self, archivo, data):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _listar(self, data):
        if not data:
            print("No hay registros disponibles.")
        else:
            for i, item in enumerate(data, 1):
                print(f"{i}.")
                for k, v in item.items():
                    print(f"   {k}: {v}")
                print("-" * 30)
        input("Presione Enter para continuar...")

    def _buscar(self, data):
        clave = input("Ingrese término de búsqueda (ej. nombre o ID): ").strip().lower()
        resultados = []
        for item in data:
            if any(clave in str(valor).lower() for valor in item.values()):
                resultados.append(item)
        if resultados:
            print(f"Se encontraron {len(resultados)} resultados:")
            for res in resultados:
                for k, v in res.items():
                    print(f"  {k}: {v}")
                print("-" * 20)
        else:
            print("No se encontraron resultados.")
        input("Presione Enter para continuar...")

    def _agregar(self, data, archivo):
        print("Agregar nuevo registro")
        nuevo = {}
        while True:
            clave = input("Ingrese el nombre del campo (deje vacío para terminar): ").strip()
            if clave == "":
                break
            valor = input(f"Ingrese el valor para '{clave}': ").strip()
            nuevo[clave] = valor
        if nuevo:
            data.append(nuevo)
            self._guardar_json(archivo, data)
            print("Registro agregado correctamente.")
        else:
            print("No se agregó ningún registro.")
        input("Presione Enter para continuar...")

    def _modificar(self, data, archivo):
        if not data:
            print("No hay registros para modificar.")
            input("Presione Enter para continuar...")
            return
        self._listar(data)
        try:
            index = int(input("Ingrese el número del registro a modificar: ").strip()) - 1
            if 0 <= index < len(data):
                registro = data[index]
                print(f"Registro actual:")
                for k, v in registro.items():
                    print(f"   {k}: {v}")
                print("Ingrese nuevos valores (deje vacío para conservar valor actual):")
                for clave in list(registro.keys()):
                    nuevo_valor = input(f"Nuevo valor para '{clave}' (actual: '{registro[clave]}'): ").strip()
                    if nuevo_valor != "":
                        registro[clave] = nuevo_valor
                self._guardar_json(archivo, data)
                print("Registro modificado correctamente.")
            else:
                print("Número de registro inválido.")
        except ValueError:
            print("Entrada inválida.")
        input("Presione Enter para continuar...")

    def _eliminar(self, data, archivo):
        if not data:
            print("No hay registros para eliminar.")
            input("Presione Enter para continuar...")
            return
        self._listar(data)
        try:
            index = int(input("Ingrese el número del registro a eliminar: ").strip()) - 1
            if 0 <= index < len(data):
                eliminado = data.pop(index)
                self._guardar_json(archivo, data)
                print("Registro eliminado:")
                for k, v in eliminado.items():
                    print(f"   {k}: {v}")
            else:
                print("Número de registro inválido.")
        except ValueError:
            print("Entrada inválida.")
        input("Presione Enter para continuar...")

    def _contenedor_oferta(self):
        pass

# Ejecutar directamente:
adminVentana()
