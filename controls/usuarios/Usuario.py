from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self,id_usuario, nombre, apellido, CI, email, contrasena):
        super().__init__(id_usuario,nombre, apellido, CI, email, contrasena)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena

    @abstractmethod
    def registrarse(self):
        pass

    @abstractmethod
    def iniciar_sesion(self):
        pass