from Usuario import Usuario
import csv
import os

class Estudiante(Usuario):
    def __init__(self, id_usuario=None, nombre=None, apellido=None, CI=None, email=None, contrasena=None):
        super().__init__(id_usuario, nombre, apellido, CI, email, contrasena)
    
    def registrarse(self, email, contrasena):
        """Registra un nuevo estudiante validando con Registro_Unico.csv"""
        # Verificar si el correo existe en Registro_Unico.csv con estado Completo
        if not self.verificar_registro_unico(email):
            return False, "El correo no está registrado en el sistema o no tiene estado 'Completo'"
        
        # Verificar si el usuario ya está registrado
        if self.verificar_usuario_existente(email):
            return False, "El usuario ya está registrado"
        
        # Obtener datos del usuario desde Registro_Unico.csv
        datos_usuario = self.obtener_datos_registro_unico(email)
        if not datos_usuario:
            return False, "No se pudieron obtener los datos del usuario"
        
        # Guardar en usuarios_registrados.csv
        resultado = self.guardar_usuario_registrado(
            datos_usuario['tipoDocumento'],
            datos_usuario['identificacion'],
            datos_usuario['correo'],
            datos_usuario['nombres'],
            datos_usuario['apellidos'],
            contrasena
        )
        
        if resultado:
            # Establecer los datos del objeto estudiante
            self.email = email
            self.contrasena = contrasena
            self.nombre = datos_usuario['nombres']
            self.apellido = datos_usuario['apellidos']
            self.CI = datos_usuario['identificacion']
            return True, "Registro exitoso"
        else:
            return False, "Error al guardar el registro"
    
    def iniciar_sesion(self, email, contrasena):
        """Inicia sesión verificando en usuarios_registrados.csv"""
        return self.verificar_credenciales(email, contrasena)
    
    @staticmethod
    def verificar_usuario_existente(email):
        """Verifica si el usuario ya está registrado en usuarios_registrados.csv"""
        try:
            if not os.path.exists("usuarios_registrados.csv"):
                return False
            
            with open("usuarios_registrados.csv", 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['correo'].strip().lower() == email.lower():
                        return True
            return False
        except Exception as e:
            print(f"Error al verificar usuario: {e}")
            return False
    
    @staticmethod
    def verificar_credenciales(email, contrasena):
        """Verifica las credenciales en usuarios_registrados.csv"""
        try:
            if not os.path.exists("usuarios_registrados.csv"):
                return False, None
            
            with open("usuarios_registrados.csv", 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    correo_db = row['correo'].strip().lower()
                    contrasena_db = row['contraseña'].strip()
                    
                    if correo_db == email.lower() and contrasena_db == contrasena:
                        # Retornar True y los datos del usuario
                        return True, {
                            'nombres': row['nombres'],
                            'apellidos': row['apellidos'],
                            'identificacion': row['identificacion'],
                            'correo': row['correo']
                        }
            return False, None
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return False, None  
