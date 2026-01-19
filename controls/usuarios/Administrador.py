import json
import os
import csv
from datetime import datetime
from .Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, CI="", Nombre="", Apellido="", Correo="", Contraseña="", 
                 Dirección=".", Teléfono=".", Género="Prefiero no decirlo", Rol="Sistema"):
        self.CI = CI
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.Correo = Correo
        self._Contraseña = Contraseña
        self.Dirección = Dirección
        self.Teléfono = Teléfono
        self.Género = Género
        self._Rol = Rol
    
    def to_dict(self):
        """Convierte el administrador a diccionario"""
        return {
            "C.I.": self.CI,
            "Nombre": self.Nombre,
            "Apellido": self.Apellido,
            "Correo": self.Correo,
            "Contraseña": self._Contraseña,
            "Dirección": self.Dirección,
            "Teléfono": self.Teléfono,
            "Género": self.Género,
            "Rol": self._Rol
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un administrador desde un diccionario"""
        return Administrador(
            CI=data.get("C.I.", ""),
            Nombre=data.get("Nombre", ""),
            Apellido=data.get("Apellido", ""),
            Correo=data.get("Correo", ""),
            _Contraseña=data.get("Contraseña", ""),
            Dirección=data.get("Dirección", "."),
            Teléfono=data.get("Teléfono", "."),
            Género=data.get("Género", "Prefiero no decirlo"),
            _Rol=data.get("Rol", "Sistema")
        )

class GestorAdministradores:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.admin_file = os.path.join(self.base_dir, "..", "..", "data", "registros", "admin.json")
        self._crear_archivo_si_no_existe()
    
    def _crear_archivo_si_no_existe(self):
        """Crea el archivo admin.json si no existe con el admin por defecto"""
        os.makedirs(os.path.dirname(self.admin_file), exist_ok=True)
        
        if not os.path.exists(self.admin_file):
            admin_por_defecto = Administrador(
                CI=".",
                Nombre="Admin",
                Apellido="Sistema",
                Correo="admin@system.com",
                _Contraseña="admin",
                Dirección=".",
                Teléfono=".",
                Género="Prefiero no decirlo",
                _Rol="Sistema"
            )
            
            with open(self.admin_file, 'w', encoding='utf-8') as f:
                json.dump([admin_por_defecto.to_dict()], f, indent=4, ensure_ascii=False)
    
    def _leer_admin_json(self):
        """Lee y devuelve la lista de administradores del archivo JSON"""
        try:
            if not os.path.exists(self.admin_file):
                return []
            
            with open(self.admin_file, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                
                # Intentar cargar como lista
                try:
                    data = json.loads(contenido)
                    if isinstance(data, dict):
                        return [Administrador.from_dict(data)]
                    elif isinstance(data, list):
                        return [Administrador.from_dict(item) for item in data]
                    else:
                        return []
                except json.JSONDecodeError:
                    # Si falla, crear administrador por defecto
                    return [Administrador()]
        except Exception as e:
            print(f"Error al leer admin.json: {e}")
            return []
    
    def _escribir_admin_json(self, administradores):
        """Escribe la lista de administradores al archivo JSON"""
        try:
            with open(self.admin_file, 'w', encoding='utf-8') as f:
                json.dump([admin.to_dict() for admin in administradores], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al escribir admin.json: {e}")
            return False
    
    def obtener_todos(self):
        """Obtiene todos los administradores"""
        return self._leer_admin_json()
    
    def obtener_por_ci(self, ci):
        """Obtiene un administrador por su C.I."""
        administradores = self._leer_admin_json()
        for admin in administradores:
            if admin.CI == ci:
                return admin
        return None
    
    def obtener_por_correo(self, correo):
        """Obtiene un administrador por su correo"""
        administradores = self._leer_admin_json()
        for admin in administradores:
            if admin.Correo.lower() == correo.lower():
                return admin
        return None
    
    def agregar(self, datos_admin):
        """Agrega un nuevo administrador"""
        try:
            # Validar que no exista ya el correo o CI
            administradores = self._leer_admin_json()
            
            for admin in administradores:
                if admin.Correo.lower() == datos_admin['Correo'].lower():
                    return False, "Ya existe un administrador con ese correo"
                if admin.CI == datos_admin['C.I.'] and datos_admin['C.I.'] != ".":
                    return False, "Ya existe un administrador con esa identificación"
            
            # Crear nuevo administrador
            nuevo_admin = Administrador(
                CI=datos_admin.get('C.I.', ''),
                Nombre=datos_admin.get('Nombre', ''),
                Apellido=datos_admin.get('Apellido', ''),
                Correo=datos_admin.get('Correo', ''),
                _Contraseña=datos_admin.get('Contraseña', ''),
                Dirección=datos_admin.get('Dirección', '.'),
                Teléfono=datos_admin.get('Teléfono', '.'),
                Género=datos_admin.get('Género', 'Prefiero no decirlo'),
                _Rol=datos_admin.get('Rol', 'Administrador')
            )
            
            administradores.append(nuevo_admin)
            
            if self._escribir_admin_json(administradores):
                return True, f"Administrador {nuevo_admin.Nombre} agregado exitosamente"
            else:
                return False, "Error al guardar el administrador"
                
        except Exception as e:
            return False, f"Error al agregar administrador: {str(e)}"
    
    def modificar(self, datos_admin):
        """Modifica un administrador existente"""
        try:
            administradores = self._leer_admin_json()
            
            for i, admin in enumerate(administradores):
                if admin.CI == datos_admin['C.I.']:
                    # Actualizar datos
                    administradores[i].Nombre = datos_admin.get('Nombre', admin.Nombre)
                    administradores[i].Apellido = datos_admin.get('Apellido', admin.Apellido)
                    administradores[i].Correo = datos_admin.get('Correo', admin.Correo)
                    administradores[i]._Contraseña = datos_admin.get('Contraseña', admin._Contraseña)
                    administradores[i].Dirección = datos_admin.get('Dirección', admin.Dirección)
                    administradores[i].Teléfono = datos_admin.get('Teléfono', admin.Teléfono)
                    administradores[i].Género = datos_admin.get('Género', admin.Género)
                    administradores[i]._Rol = datos_admin.get('Rol', admin.Rol)
                    
                    if self._escribir_admin_json(administradores):
                        return True, f"Administrador {administradores[i].Nombre} modificado exitosamente"
                    else:
                        return False, "Error al guardar los cambios"
            
            return False, "Administrador no encontrado"
                
        except Exception as e:
            return False, f"Error al modificar administrador: {str(e)}"
    
    def eliminar(self, ci):
        """Elimina un administrador por su C.I."""
        try:
            if ci == ".":
                return False, "No se puede eliminar al administrador principal del sistema"
            
            administradores = self._leer_admin_json()
            administradores_filtrados = []
            admin_eliminado = None
            
            for admin in administradores:
                if admin.CI == ci:
                    admin_eliminado = admin
                else:
                    administradores_filtrados.append(admin)
            
            if not admin_eliminado:
                return False, "Administrador no encontrado"
            
            if self._escribir_admin_json(administradores_filtrados):
                return True, f"Administrador {admin_eliminado.Nombre} eliminado exitosamente"
            else:
                return False, "Error al eliminar el administrador"
                
        except Exception as e:
            return False, f"Error al eliminar administrador: {str(e)}"
    
    def verificar_credenciales(self, correo, contraseña):
        """Verifica las credenciales de un administrador"""
        administradores = self._leer_admin_json()
        
        for admin in administradores:
            if admin.Correo.lower() == correo.lower() and admin._Contraseña == contraseña:
                return True, admin
        
        return False, None
    
    def generar_contraseña_segura(self, longitud=10):
        """Genera una contraseña segura"""
        import random
        import string
        
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(caracteres) for _ in range(longitud))
    
    def cambiar_contraseña(self, ci, nueva_contraseña):
        """Cambia la contraseña de un administrador"""
        try:
            administradores = self._leer_admin_json()
            
            for i, admin in enumerate(administradores):
                if admin.CI == ci:
                    administradores[i]._Contraseña = nueva_contraseña
                    
                    if self._escribir_admin_json(administradores):
                        return True, "Contraseña cambiada exitosamente"
                    else:
                        return False, "Error al guardar la nueva contraseña"
            
            return False, "Administrador no encontrado"
                
        except Exception as e:
            return False, f"Error al cambiar contraseña: {str(e)}"

class Administrador(Usuario):
    
    def autenticar(self, contraseña: str) -> bool:
        return self.Contraseña == contraseña