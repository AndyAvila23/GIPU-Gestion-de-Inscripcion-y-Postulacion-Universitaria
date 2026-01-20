from abc import ABC, abstractmethod
import csv
import os

class Usuario(ABC):
    def __init__(self, id_usuario=None, nombre=None, apellido=None, CI=None, email=None, contrasena=None):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__apellido = apellido
        self.__CI = CI
        self.__email = email
        self.__contrasena = contrasena
    
    # GETTERS Y SETTERS (propiedades)
    @property
    def id_usuario(self):
        return self.__id_usuario
    
    @id_usuario.setter
    def id_usuario(self, value):
        self.__id_usuario = value
    
    @property
    def nombre(self):
        """Getter para nombre"""
        return self.__nombre
    
    @nombre.setter
    def nombre(self, value):
        """Setter para nombre"""
        self.__nombre = value
    
    @property
    def apellido(self):
        """Getter para apellido"""
        return self.__apellido
    
    @apellido.setter
    def apellido(self, value):
        """Setter para apellido"""
        self.__apellido = value
    
    @property
    def CI(self):
        """Getter para CI"""
        return self.__CI
    
    @CI.setter
    def CI(self, value):
        """Setter para CI"""
        self.__CI = value
    
    @property
    def email(self):
        """Getter para email"""
        return self.__email
    
    @email.setter
    def email(self, value):
        """Setter para email"""
        self.__email = value
    
    @property
    def contrasena(self):
        """Getter para contrasena"""
        return self.__contrasena
    
    @contrasena.setter
    def contrasena(self, value):
        """Setter para contrasena"""
        self.__contrasena = value
    
    # Método abstracto (debe implementarse en subclases)
    @abstractmethod
    def autenticar(self, contrasena: str) -> bool:
        pass
    
    @staticmethod
    def verificar_registro_unico(email):
        """Verifica si el email existe en Registro_Unico.csv y tiene estado 'Completo'"""
        try:
            if not os.path.exists("Registro_Unico.csv"):
                return False
            
            with open("Registro_Unico.csv", 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                headers = next(reader)  # Saltar encabezados
                
                # Buscar índices de las columnas necesarias
                correo_index = headers.index('correo') if 'correo' in headers else -1
                estado_index = headers.index('estado') if 'estado' in headers else -1
                
                if correo_index == -1 or estado_index == -1:
                    return False
                
                for row in reader:
                    if len(row) > max(correo_index, estado_index):
                        correo_registro = row[correo_index].strip().lower()
                        estado = row[estado_index].strip()
                        
                        if correo_registro == email.lower() and estado.upper() == "COMPLETO":
                            return True
            return False
        except Exception as e:
            print(f"Error al verificar registro único: {e}")
            return False
    
    @staticmethod
    def guardar_usuario_registrado(tipo_documento, identificacion, correo, nombres, apellidos, contraseña):
        """Guarda un nuevo usuario en usuarios_registrados.csv"""
        try:
            # Verificar si el archivo existe
            file_exists = os.path.exists("usuarios_registrados.csv")
            
            with open("usuarios_registrados.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Escribir encabezados si el archivo no existe
                if not file_exists:
                    writer.writerow(['tipoDocumento', 'identificacion', 'correo', 'nombres', 'apellidos', 'contraseña'])
                
                # Escribir datos del usuario
                writer.writerow([tipo_documento, identificacion, correo, nombres, apellidos, contraseña])
            
            return True
        except Exception as e:
            print(f"Error al guardar usuario: {e}")
            return False
    
    @staticmethod
    def obtener_datos_registro_unico(email):
        """Obtiene los datos del usuario desde Registro_Unico.csv"""
        try:
            if not os.path.exists("Registro_Unico.csv"):
                return None
            
            with open("Registro_Unico.csv", 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                headers = next(reader)
                
                # Buscar índices de las columnas necesarias
                tipo_doc_index = headers.index('tipoDocumento') if 'tipoDocumento' in headers else -1
                ident_index = headers.index('identificacion') if 'identificacion' in headers else -1
                correo_index = headers.index('correo') if 'correo' in headers else -1
                nombres_index = headers.index('nombres') if 'nombres' in headers else -1
                apellidos_index = headers.index('apellidos') if 'apellidos' in headers else -1
                
                for row in reader:
                    if len(row) > max(tipo_doc_index, ident_index, correo_index, nombres_index, apellidos_index):
                        correo_registro = row[correo_index].strip().lower()
                        
                        if correo_registro == email.lower():
                            return {
                                'tipoDocumento': row[tipo_doc_index],
                                'identificacion': row[ident_index],
                                'correo': row[correo_index],
                                'nombres': row[nombres_index],
                                'apellidos': row[apellidos_index]
                            }
            return None
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None