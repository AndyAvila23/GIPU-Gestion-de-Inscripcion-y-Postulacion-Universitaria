import hashlib
import re
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

class Autenticador(ABC):
    @abstractmethod
    def autenticar(self, credenciales: dict) -> bool:
        pass

class GestionContraseña(ABC):
    @abstractmethod
    def cambiar_contraseña(self, nueva_contraseña: str) -> bool:
        pass

class ValidadorDatos(ABC):
    @abstractmethod
    def validar(self) -> bool:
        pass

class RepositorioUsuario(ABC):
    @abstractmethod
    def guardar(self) -> bool:
        pass
    
    @abstractmethod
    def eliminar(self) -> bool:
        pass

class ValidadorCI:
    def __init__(self, ci: str):
        self.ci = ci
    
    def validar(self) -> bool:
        if not self.ci:
            return False
        
        patron = r'^\d{6,10}$'
        return bool(re.match(patron, self.ci))

class ValidadorCorreo:
    def __init__(self, correo: str):
        self.correo = correo
    
    def validar(self) -> bool:
        if not self.correo:
            return False
        
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, self.correo))

class ValidadorContraseña:
    def __init__(self, contraseña: str):
        self.contraseña = contraseña
    
    def validar(self) -> bool:
        if not self.contraseña or len(self.contraseña) < 8:
            return False
        
        tiene_letra = any(c.isalpha() for c in self.contraseña)
        tiene_numero = any(c.isdigit() for c in self.contraseña)
        
        return tiene_letra and tiene_numero

@dataclass
class EntidadBase:
    id: int
    fecha_creacion: datetime = datetime.now()
    fecha_actualizacion: datetime = datetime.now()
    
    def actualizar_fecha_modificacion(self):
        self.fecha_actualizacion = datetime.now()

class Usuario(EntidadBase, Autenticador, GestionContraseña, ValidadorDatos, RepositorioUsuario):
    
    def __init__(self, id_usuario: int, nombre: str, apellido: str, 
                 correo: str, contraseña: str, ci: str):
        super().__init__(id_usuario)
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo
        self._contraseña_hash = self._encriptar_contraseña(contraseña)
        self._ci = ci
        self._activo = True
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        self._nombre = valor.strip()
        self.actualizar_fecha_modificacion()
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @apellido.setter
    def apellido(self, valor: str):
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El apellido debe tener al menos 2 caracteres")
        self._apellido = valor.strip()
        self.actualizar_fecha_modificacion()
    
    @property
    def correo(self) -> str:
        return self._correo
    
    @correo.setter
    def correo(self, valor: str):
        validador = ValidadorCorreo(valor)
        if not validador.validar():
            raise ValueError("El correo electrónico no tiene un formato válido")
        self._correo = valor.strip()
        self.actualizar_fecha_modificacion()
    
    @property
    def ci(self) -> str:
        return self._ci
    
    @ci.setter
    def ci(self, valor: str):
        validador = ValidadorCI(valor)
        if not validador.validar():
            raise ValueError("La CI no tiene un formato válido")
        self._ci = valor.strip()
        self.actualizar_fecha_modificacion()
    
    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def autenticar(self, credenciales: dict) -> bool:
        correo = credenciales.get('correo', '')
        contraseña = credenciales.get('contraseña', '')
        
        if not correo or not contraseña:
            return False
        
        contraseña_hash = self._encriptar_contraseña(contraseña)
        return (self._correo == correo and 
                self._contraseña_hash == contraseña_hash and
                self._activo)
    
    def cambiar_contraseña(self, nueva_contraseña: str) -> bool:
        validador = ValidadorContraseña(nueva_contraseña)
        if not validador.validar():
            raise ValueError("La contraseña no cumple con los requisitos de seguridad")
        
        self._contraseña_hash = self._encriptar_contraseña(nueva_contraseña)
        self.actualizar_fecha_modificacion()
        return True
    
    def verificar_contraseña(self, contraseña: str) -> bool:
        return self._contraseña_hash == self._encriptar_contraseña(contraseña)
    
    def validar(self) -> bool:
        validadores = [
            ValidadorCI(self._ci),
            ValidadorCorreo(self._correo),
            ValidadorContraseña("dummy")
        ]
        
        if len(self._nombre.strip()) < 2 or len(self._apellido.strip()) < 2:
            return False
        
        return all(v.validar() for v in validadores[:-1])
    
    def guardar(self) -> bool:
        if not self.validar():
            return False
        
        print(f"Usuario {self.nombre_completo} guardado exitosamente")
        return True
    
    def eliminar(self) -> bool:
        self._activo = False
        self.actualizar_fecha_modificacion()
        print(f"Usuario {self.nombre_completo} marcado como inactivo")
        return True
    
    def editar_perfil(self, **kwargs) -> bool:
        campos_permitidos = {'nombre', 'apellido', 'correo', 'ci'}
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                setattr(self, campo, valor)
        
        self.actualizar_fecha_modificacion()
        return True
    
    def activar(self) -> None:
        self._activo = True
        self.actualizar_fecha_modificacion()
    
    def desactivar(self) -> None:
        self._activo = False
        self.actualizar_fecha_modificacion()
    
    def _encriptar_contraseña(self, contraseña: str) -> str:
        return hashlib.sha256(contraseña.encode('utf-8')).hexdigest()
    
    def __str__(self) -> str:
        return f"Usuario(ID={self.id}, Nombre={self.nombre_completo}, Correo={self.correo}, Activo={self.activo})"
    
    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}')"

class FabricaUsuarios:
    @staticmethod
    def crear_usuario(id_usuario: int, nombre: str, apellido: str, 
                     correo: str, contraseña: str, ci: str) -> Usuario:
        usuario = Usuario(id_usuario, nombre, apellido, correo, contraseña, ci)
        
        if not usuario.validar():
            raise ValueError("Los datos del usuario no son válidos")
        
        return usuario