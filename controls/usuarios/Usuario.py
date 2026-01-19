
from abc import ABC, abstractmethod
import csv
import os

class Usuario(ABC):
    def __init__(self, id_usuario=None, nombre=None, apellido=None, CI=None, email=None, contraseña=None):
        # Atributos privados/protegidos
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._apellido = apellido
        self._CI = CI
        self._email = email
        self._contrasena = contraseña
    
    # Getters y Setters (propiedades)
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        # Validación podría ir aquí
        self._email = value
    
    # Método abstracto (debe implementarse en subclases)
    @abstractmethod
    def autenticar(self, contrasena: str) -> bool:
        pass
    
    # Método privado para uso interno
    def _validar_email(self, email: str) -> bool:
        return "@" in email and "." in email
    
    # Método protegido (para uso de subclases)
    def _generar_id_unico(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]
    
    # Método estático (no accede a estado de instancia)
    @staticmethod
    def _leer_csv(ruta_archivo: str) -> list:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return []