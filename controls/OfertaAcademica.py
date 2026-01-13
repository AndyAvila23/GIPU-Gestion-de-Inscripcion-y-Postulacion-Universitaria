import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid

class OfertaAcademica:
    def __init__(self, id_oferta: str = None, carrera: str = "", facultad: str = "",
                 cupos_disponibles: int = 0, modalidad: str = "", 
                 fecha_registro: str = None, publicada: bool = False):
        
        self.id_oferta = id_oferta or str(uuid.uuid4())[:8]
        self.carrera = carrera
        self.facultad = facultad
        self.cupos_disponibles = cupos_disponibles
        self.modalidad = modalidad
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.publicada = publicada
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id_oferta=data.get('id', data.get('id_oferta')),
            carrera=data.get('carrera', ''),
            facultad=data.get('facultad', ''),
            cupos_disponibles=int(data.get('cupos_disponibles', 0)),
            modalidad=data.get('modalidad', ''),
            fecha_registro=data.get('fecha_registro'),
            publicada=data.get('publicada', 'False').lower() == 'true'
        )
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id_oferta,
            'carrera': self.carrera,
            'facultad': self.facultad,
            'cupos_disponibles': self.cupos_disponibles,
            'modalidad': self.modalidad,
            'fecha_registro': self.fecha_registro,
            'publicada': 'True' if self.publicada else 'False'
        }
    
    def validar(self) -> bool:
        """Validar que todos los campos requeridos estén presentes"""
        return all([
            self.id_oferta,
            self.carrera.strip(),
            self.facultad.strip(),
            self.cupos_disponibles >= 0,
            self.modalidad.strip() in ['presencial', 'virtual', 'híbrida', 'semipresencial', '']
        ])
    
    def __str__(self) -> str:
        return f"{self.carrera} - {self.facultad} ({self.cupos_disponibles} cupos, {self.modalidad})"

class GestorOfertas:
    def __init__(self, archivo_csv: str = None):
        if archivo_csv is None:
            # Ruta por defecto
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.archivo_csv = os.path.join(base_dir, "..", "data", "universidad", "oferta_academica.csv")
        else:
            self.archivo_csv = archivo_csv
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
    
    def cargar_ofertas(self) -> List[OfertaAcademica]:
        """Cargar todas las ofertas desde el archivo CSV"""
        ofertas = []
        
        if not os.path.exists(self.archivo_csv):
            return ofertas
        
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        oferta = OfertaAcademica.from_dict(row)
                        if oferta.validar():
                            ofertas.append(oferta)
                    except Exception as e:
                        print(f"Error al cargar oferta: {e}")
                        continue
        except Exception as e:
            print(f"Error al leer archivo CSV: {e}")
        
        return ofertas
    
    def guardar_ofertas(self, ofertas: List[OfertaAcademica]) -> bool:
        """Guardar todas las ofertas en el archivo CSV"""
        try:
            # Convertir a diccionarios
            datos = [oferta.to_dict() for oferta in ofertas]
            
            if not datos:
                return False
            
            # Escribir en CSV
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'carrera', 'facultad', 'cupos_disponibles', 
                            'modalidad', 'fecha_registro', 'publicada']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(datos)
            
            return True
            
        except Exception as e:
            print(f"Error al guardar ofertas: {e}")
            return False
    
    def agregar_oferta(self, oferta: OfertaAcademica) -> bool:
        """Agregar una nueva oferta"""
        try:
            # Cargar ofertas existentes
            ofertas = self.cargar_ofertas()
            
            # Verificar si ya existe una oferta con el mismo ID
            for o in ofertas:
                if o.id_oferta == oferta.id_oferta:
                    # Actualizar ID si es necesario
                    oferta.id_oferta = str(uuid.uuid4())[:8]
                    break
            
            # Agregar nueva oferta
            ofertas.append(oferta)
            
            # Guardar todas las ofertas
            return self.guardar_ofertas(ofertas)
            
        except Exception as e:
            print(f"Error al agregar oferta: {e}")
            return False
    
    def eliminar_oferta(self, id_oferta: str) -> bool:
        """Eliminar una oferta por ID"""
        try:
            # Cargar ofertas existentes
            ofertas = self.cargar_ofertas()
            
            # Filtrar la oferta a eliminar
            ofertas_filtradas = [o for o in ofertas if o.id_oferta != id_oferta]
            
            if len(ofertas_filtradas) == len(ofertas):
                # No se encontró la oferta
                return False
            
            # Guardar ofertas actualizadas
            return self.guardar_ofertas(ofertas_filtradas)
            
        except Exception as e:
            print(f"Error al eliminar oferta: {e}")
            return False
    
    def buscar_oferta(self, criterio: str, valor: str) -> List[OfertaAcademica]:
        """Buscar ofertas por criterio"""
        ofertas = self.cargar_ofertas()
        resultados = []
        
        for oferta in ofertas:
            if criterio == 'id' and oferta.id_oferta == valor:
                resultados.append(oferta)
            elif criterio == 'carrera' and valor.lower() in oferta.carrera.lower():
                resultados.append(oferta)
            elif criterio == 'facultad' and valor.lower() in oferta.facultad.lower():
                resultados.append(oferta)
            elif criterio == 'modalidad' and valor.lower() == oferta.modalidad.lower():
                resultados.append(oferta)
        
        return resultados
    
    def actualizar_oferta(self, id_oferta: str, datos_actualizados: Dict) -> bool:
        """Actualizar una oferta existente"""
        try:
            # Cargar ofertas existentes
            ofertas = self.cargar_ofertas()
            
            # Buscar y actualizar la oferta
            for i, oferta in enumerate(ofertas):
                if oferta.id_oferta == id_oferta:
                    # Actualizar campos
                    for key, value in datos_actualizados.items():
                        if hasattr(oferta, key):
                            setattr(oferta, key, value)
                    
                    # Guardar ofertas actualizadas
                    return self.guardar_ofertas(ofertas)
            
            return False  # No se encontró la oferta
            
        except Exception as e:
            print(f"Error al actualizar oferta: {e}")
            return False
    
    def importar_csv(self, ruta_csv: str) -> int:
        """Importar ofertas desde un archivo CSV externo"""
        try:
            ofertas_importadas = []
            
            with open(ruta_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Mapear campos si es necesario
                        oferta_dict = {
                            'carrera': row.get('CAR_NOMBRE_CARRERA', row.get('carrera', '')),
                            'facultad': row.get('IES_NOMBRE_INSTIT', row.get('facultad', '')),
                            'cupos_disponibles': int(row.get('CUS_TOTAL_CUPOS', row.get('cupos', 0))),
                            'modalidad': row.get('MODALIDAD', row.get('modalidad', 'presencial')).lower()
                        }
                        
                        # Crear oferta
                        oferta = OfertaAcademica(
                            carrera=oferta_dict['carrera'],
                            facultad=oferta_dict['facultad'],
                            cupos_disponibles=oferta_dict['cupos_disponibles'],
                            modalidad=oferta_dict['modalidad']
                        )
                        
                        if oferta.validar():
                            ofertas_importadas.append(oferta)
                            
                    except Exception as e:
                        print(f"Error al procesar fila: {e}")
                        continue
            
            # Agregar todas las ofertas importadas
            ofertas_existentes = self.cargar_ofertas()
            todas_ofertas = ofertas_existentes + ofertas_importadas
            
            # Guardar
            if self.guardar_ofertas(todas_ofertas):
                return len(ofertas_importadas)
            else:
                return 0
                
        except Exception as e:
            print(f"Error al importar CSV: {e}")
            return 0