import json
import os
import csv
from datetime import datetime
from .Usuario import Usuario

# PATRÓN CREACIONAL: SINGLETON (Mejorado y Corregido)
class SingletonMeta(type):
    """Metaclase para Singleton REAL"""
    _instancias = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]

class Administrador(Usuario):
    def __init__(self, CI="", Nombre="", Apellido="", Correo="", Contraseña="", 
                 Dirección=".", Teléfono=".", Género="Prefiero no decirlo", Rol="Sistema"):
        self.__CI = CI
        self.__Nombre = Nombre
        self.__Apellido = Apellido
        self.__Correo = Correo
        self.__Contraseña = Contraseña
        self.__Dirección = Dirección
        self.__Teléfono = Teléfono
        self.__Género = Género
        self.__Rol = Rol
    
    # Getters y Setters (sin cambios)
    @property
    def CI(self):
        return self.__CI
    
    @property
    def Nombre(self):
        return self.__Nombre
    
    @property
    def Correo(self):
        return self.__Correo
    
    @property
    def Rol(self):
        return self.__Rol
    
    def to_dict(self):
        return {
            "C.I.": self.__CI,
            "Nombre": self.__Nombre,
            "Apellido": self.__Apellido,
            "Correo": self.__Correo,
            "Contraseña": self.__Contraseña,
            "Dirección": self.__Dirección,
            "Teléfono": self.__Teléfono,
            "Género": self.__Género,
            "Rol": self.__Rol
        }
    
    @staticmethod
    def from_dict(data):
        return Administrador(
            CI=data.get("C.I.", ""),
            Nombre=data.get("Nombre", ""),
            Apellido=data.get("Apellido", ""),
            Correo=data.get("Correo", ""),
            Contraseña=data.get("Contraseña", ""),
            Dirección=data.get("Dirección", "."),
            Teléfono=data.get("Teléfono", "."),
            Género=data.get("Género", "Prefiero no decirlo"),
            Rol=data.get("Rol", "Sistema")
        )
    
    def autenticar(self, contraseña: str) -> bool:
        return self.__Contraseña == contraseña

# SINGLETON REAL - Solo UNA instancia de GestorAdministradores en toda la aplicación
class GestorAdministradores(metaclass=SingletonMeta):
    """SINGLETON: Solo existe UNA instancia en toda la aplicación"""
    
    def __init__(self):
        if not hasattr(self, '_inicializado'):  # Prevenir re-inicialización
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.admin_file = os.path.join(self.base_dir, "..", "..", "data", "registros", "admin.json")
            self._crear_archivo_si_no_existe()
            self._inicializado = True
            print("✅ SINGLETON: GestorAdministradores inicializado (una sola vez)")
    
    def _crear_archivo_si_no_existe(self):
        os.makedirs(os.path.dirname(self.admin_file), exist_ok=True)
        if not os.path.exists(self.admin_file):
            admin_por_defecto = Administrador(
                CI=".", Nombre="Admin", Apellido="Sistema",
                Correo="admin@system.com", Contraseña="admin",
                Dirección=".", Teléfono=".", 
                Género="Prefiero no decirlo", Rol="Sistema"
            )
            with open(self.admin_file, 'w', encoding='utf-8') as f:
                json.dump([admin_por_defecto.to_dict()], f, indent=4, ensure_ascii=False)
    
    def _leer_admin_json(self):
        try:
            if not os.path.exists(self.admin_file):
                return []
            with open(self.admin_file, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                data = json.loads(contenido)
                if isinstance(data, dict):
                    return [Administrador.from_dict(data)]
                return [Administrador.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def _escribir_admin_json(self, administradores):
        try:
            with open(self.admin_file, 'w', encoding='utf-8') as f:
                json.dump([admin.to_dict() for admin in administradores], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    # Métodos públicos (sin cambios)
    def obtener_todos(self):
        return self._leer_admin_json()
    
    def obtener_por_ci(self, ci):
        for admin in self._leer_admin_json():
            if admin.CI == ci:
                return admin
        return None
    
    def agregar(self, datos_admin):
        try:
            administradores = self._leer_admin_json()
            for admin in administradores:
                if admin.Correo.lower() == datos_admin['Correo'].lower():
                    return False, "Ya existe un administrador con ese correo"
            
            nuevo_admin = Administrador(
                CI=datos_admin.get('C.I.', ''),
                Nombre=datos_admin.get('Nombre', ''),
                Apellido=datos_admin.get('Apellido', ''),
                Correo=datos_admin.get('Correo', ''),
                Contraseña=datos_admin.get('Contraseña', ''),
                Dirección=datos_admin.get('Dirección', '.'),
                Teléfono=datos_admin.get('Teléfono', '.'),
                Género=datos_admin.get('Género', 'Prefiero no decirlo'),
                Rol=datos_admin.get('Rol', 'Administrador')
            )
            
            administradores.append(nuevo_admin)
            if self._escribir_admin_json(administradores):
                return True, f"Administrador {nuevo_admin.Nombre} agregado exitosamente"
            return False, "Error al guardar"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def verificar_credenciales(self, correo, contraseña):
        administradores = self._leer_admin_json()
        for admin in administradores:
            if admin.Correo.lower() == correo.lower() and admin.autenticar(contraseña):
                return True, admin
        return False, None

# Demostración del Singleton
def demostrar_singleton():
    
    gestor1 = GestorAdministradores()
    gestor2 = GestorAdministradores()
    
    print(f"¿Misma instancia? {gestor1 is gestor2}")  # True
    print(f"ID gestor1: {id(gestor1)}")
    print(f"ID gestor2: {id(gestor2)}")
    
    # Mismo archivo de configuración
    print(f"Archivo admin.json: {gestor1.admin_file}")
    print(f"¿Mismo archivo? {gestor1.admin_file == gestor2.admin_file}")  # True