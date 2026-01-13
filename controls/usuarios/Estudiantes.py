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
                            'tipoDocumento': row.get('tipoDocumento', ''),
                            'identificacion': row.get('identificacion', ''),
                            'nombres': row.get('nombres', ''),
                            'apellidos': row.get('apellidos', ''),
                            'correo': row.get('correo', ''),
                            'contraseña': row.get('contraseña', '')
                        }
            return False, None
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return False, None
    
    @staticmethod
    def obtener_datos_registro_unico(email):
        """Obtiene los datos del usuario desde Registro_Unico.csv"""
        try:
            registro_path = os.path.join("data", "universidad", "Registro_Unico.csv")
            
            if not os.path.exists(registro_path):
                return None
            
            with open(registro_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('CORREO', '').strip().lower() == email.lower():
                        # Verificar si tiene estado 'Completo'
                        if row.get('ESTADO', '').strip().upper() == 'COMPLETO':
                            return {
                                'tipoDocumento': 'Cédula',  # Valor por defecto
                                'identificacion': row.get('IDENTIFICACION', ''),
                                'correo': row.get('CORREO', ''),
                                'nombres': row.get('NOMBRES', ''),
                                'apellidos': row.get('APELLIDOS', '')
                            }
            return None
        except Exception as e:
            print(f"Error al obtener datos de registro único: {e}")
            return None
    
    @staticmethod
    def verificar_registro_unico(email):
        """Verifica si el correo existe en Registro_Unico.csv con estado Completo"""
        try:
            registro_path = os.path.join("data", "universidad", "Registro_Unico.csv")
            
            if not os.path.exists(registro_path):
                return False
            
            with open(registro_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('CORREO', '').strip().lower() == email.lower():
                        if row.get('ESTADO', '').strip().upper() == 'COMPLETO':
                            return True
            return False
        except Exception as e:
            print(f"Error al verificar registro único: {e}")
            return False
    
    @staticmethod
    def guardar_usuario_registrado(tipoDocumento, identificacion, correo, nombres, apellidos, contraseña):
        """Guarda un usuario en usuarios_registrados.csv"""
        try:
            usuarios_path = os.path.join("data", "registros", "usuarios_registrados.csv")
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(usuarios_path), exist_ok=True)
            
            # Verificar si el archivo existe
            file_exists = os.path.exists(usuarios_path)
            
            with open(usuarios_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Escribir encabezado si el archivo no existe
                if not file_exists:
                    writer.writerow(['tipoDocumento', 'identificacion', 'correo', 'nombres', 'apellidos', 'contraseña'])
                
                # Escribir datos del usuario
                writer.writerow([tipoDocumento, identificacion, correo, nombres, apellidos, contraseña])
            
            return True
        except Exception as e:
            print(f"Error al guardar usuario: {e}")
            return False