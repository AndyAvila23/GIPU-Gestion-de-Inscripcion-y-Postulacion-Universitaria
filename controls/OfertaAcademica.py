import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid

class OfertaAcademica:
    def __init__(self, 
                 id_oferta: str = None,
                 ies_id: str = "",
                 ies_id_sniese: str = "1016",
                 ies_nombre_instit: str = "",
                 pro_nombre: str = "MANABÍ",
                 can_nombre: str = "",
                 prq_nombre: str = "",
                 car_nombre_carrera: str = "",
                 area_nombre: str = "",
                 subarea_nombre: str = "",
                 nivel: str = "TERCER NIVEL",
                 modalidad: str = "PRESENCIAL",
                 jornada: str = "NO APLICA JORNADA",
                 ofa_titulo: str = "",
                 ofa_id: str = "",
                 cus_id: str = "",
                 cus_cupos_nivelacion: int = 0,
                 cus_cupos_primer_semestre: int = 0,
                 cus_cupos_pc: int = 0,
                 cus_total_cupos: int = 0,
                 descripcion_tipo_cupo: str = "CUPOS_NIVELACIÓN",
                 focalizada: str = "N",
                 id_registro: str = None,
                 fecha_registro: str = None,
                 publicada: bool = False):
        
        self.id_oferta = id_oferta or str(uuid.uuid4())[:8]
        self.ies_id = ies_id
        self.ies_id_sniese = ies_id_sniese
        self.ies_nombre_instit = ies_nombre_instit
        self.pro_nombre = pro_nombre
        self.can_nombre = can_nombre
        self.prq_nombre = prq_nombre
        self.car_nombre_carrera = car_nombre_carrera
        self.area_nombre = area_nombre
        self.subarea_nombre = subarea_nombre
        self.nivel = nivel
        self.modalidad = modalidad
        self.jornada = jornada
        self.ofa_titulo = ofa_titulo
        self.ofa_id = ofa_id
        self.cus_id = cus_id
        self.cus_cupos_nivelacion = cus_cupos_nivelacion
        self.cus_cupos_primer_semestre = cus_cupos_primer_semestre
        self.cus_cupos_pc = cus_cupos_pc
        self.cus_total_cupos = cus_total_cupos or (cus_cupos_nivelacion + cus_cupos_primer_semestre + cus_cupos_pc)
        self.descripcion_tipo_cupo = descripcion_tipo_cupo
        self.focalizada = focalizada
        self.id_registro = id_registro
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.publicada = publicada
        
        # Calcular automáticamente el tipo de cupo
        self._calcular_tipo_cupo()
    
    def _calcular_tipo_cupo(self):
        """Calcula automáticamente el tipo de cupo basado en los cupos disponibles"""
        if self.cus_cupos_nivelacion > 0 and self.cus_cupos_nivelacion >= self.cus_cupos_primer_semestre:
            self.descripcion_tipo_cupo = "CUPOS_NIVELACIÓN"
        elif self.cus_cupos_primer_semestre > 0:
            self.descripcion_tipo_cupo = "CUPOS_PRIMER_SEMESTRE"
        else:
            self.descripcion_tipo_cupo = "CUPOS_NIVELACIÓN"
    
    def calcular_total_cupos(self):
        """Calcula el total de cupos automáticamente"""
        self.cus_total_cupos = self.cus_cupos_nivelacion + self.cus_cupos_primer_semestre + self.cus_cupos_pc
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crear una instancia desde un diccionario"""
        # Calcular total de cupos si no está presente
        cus_nivelacion = int(data.get('CUS_CUPOS_NIVELACION', 0))
        cus_primer_sem = int(data.get('CUS_CUPOS_PRIMER_SEMESTRE', 0))
        cus_pc = int(data.get('CUS_CUPOS_PC', 0))
        total_cupos = int(data.get('CUS_TOTAL_CUPOS', cus_nivelacion + cus_primer_sem + cus_pc))
        
        return cls(
            id_oferta=data.get('id', data.get('id_oferta')),
            ies_id=data.get('IES_ID', ''),
            ies_id_sniese=data.get('IES_ID_SNIESE', '1016'),
            ies_nombre_instit=data.get('IES_NOMBRE_INSTIT', ''),
            pro_nombre=data.get('PRO_NOMBRE', 'MANABÍ'),
            can_nombre=data.get('CAN_NOMBRE', ''),
            prq_nombre=data.get('PRQ_NOMBRE', ''),
            car_nombre_carrera=data.get('CAR_NOMBRE_CARRERA', ''),
            area_nombre=data.get('AREA_NOMBRE', ''),
            subarea_nombre=data.get('SUBAREA_NOMBRE', ''),
            nivel=data.get('NIVEL', 'TERCER NIVEL'),
            modalidad=data.get('MODALIDAD', 'PRESENCIAL'),
            jornada=data.get('JORNADA', 'NO APLICA JORNADA'),
            ofa_titulo=data.get('OFA_TITULO', ''),
            ofa_id=data.get('OFA_ID', ''),
            cus_id=data.get('CUS_ID', ''),
            cus_cupos_nivelacion=cus_nivelacion,
            cus_cupos_primer_semestre=cus_primer_sem,
            cus_cupos_pc=cus_pc,
            cus_total_cupos=total_cupos,
            descripcion_tipo_cupo=data.get('DESCRIPCION_TIPO_CUPO', 'CUPOS_NIVELACIÓN'),
            focalizada=data.get('FOCALIZADA', 'N'),
            id_registro=data.get('id', ''),
            fecha_registro=data.get('fecha_registro'),
            publicada=data.get('publicada', 'False').lower() == 'true'
        )
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario para guardar en CSV"""
        self.calcular_total_cupos()
        self._calcular_tipo_cupo()
        
        return {
            'id': self.id_registro or '',
            'IES_ID': self.ies_id,
            'IES_ID_SNIESE': self.ies_id_sniese,
            'IES_NOMBRE_INSTIT': self.ies_nombre_instit,
            'PRO_NOMBRE': self.pro_nombre,
            'CAN_NOMBRE': self.can_nombre,
            'PRQ_NOMBRE': self.prq_nombre,
            'CAR_NOMBRE_CARRERA': self.car_nombre_carrera,
            'AREA_NOMBRE': self.area_nombre,
            'SUBAREA_NOMBRE': self.subarea_nombre,
            'NIVEL': self.nivel,
            'MODALIDAD': self.modalidad,
            'JORNADA': self.jornada,
            'OFA_TITULO': self.ofa_titulo,
            'OFA_ID': self.ofa_id,
            'CUS_ID': self.cus_id,
            'CUS_CUPOS_NIVELACION': self.cus_cupos_nivelacion,
            'CUS_CUPOS_PRIMER_SEMESTRE': self.cus_cupos_primer_semestre,
            'CUS_CUPOS_PC': self.cus_cupos_pc,
            'CUS_TOTAL_CUPOS': self.cus_total_cupos,
            'DESCRIPCION_TIPO_CUPO': self.descripcion_tipo_cupo,
            'FOCALIZADA': self.focalizada,
            'fecha_registro': self.fecha_registro,
            'publicada': 'True' if self.publicada else 'False'
        }
    
    def validar(self) -> bool:
        """Validar que todos los campos requeridos estén presentes"""
        campos_requeridos = [
            self.ies_nombre_instit.strip(),
            self.car_nombre_carrera.strip(),
            self.cus_total_cupos >= 0,
            self.modalidad.strip() in ['PRESENCIAL', 'VIRTUAL', 'HÍBRIDA', 'SEMI-PRESENCIAL', ''],
            self.jornada.strip() in ['MATUTINA', 'VESPERTINA', 'NOCTURNA', 'NO APLICA JORNADA', ''],
            self.focalizada.strip() in ['S', 'N']
        ]
        
        return all(campos_requeridos)
    
    def __str__(self) -> str:
        return f"{self.car_nombre_carrera} - {self.ies_nombre_instit} ({self.cus_total_cupos} cupos, {self.modalidad})"

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
        
        # Inicializar archivo si no existe
        self._inicializar_archivo()
    
    def _inicializar_archivo(self):
        """Inicializar el archivo CSV con los encabezados correctos si no existe"""
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    'IES_ID', 'IES_ID_SNIESE', 'IES_NOMBRE_INSTIT', 'PRO_NOMBRE', 'CAN_NOMBRE',
                    'PRQ_NOMBRE', 'CAR_NOMBRE_CARRERA', 'AREA_NOMBRE', 'SUBAREA_NOMBRE', 'NIVEL',
                    'MODALIDAD', 'JORNADA', 'OFA_TITULO', 'OFA_ID', 'CUS_ID', 'CUS_CUPOS_NIVELACION',
                    'CUS_CUPOS_PRIMER_SEMESTRE', 'CUS_CUPOS_PC', 'CUS_TOTAL_CUPOS', 'DESCRIPCION_TIPO_CUPO',
                    'FOCALIZADA', 'id', 'fecha_registro'
                ])
    
    def cargar_ofertas(self) -> List[OfertaAcademica]:
        """Cargar todas las ofertas desde el archivo CSV"""
        ofertas = []
        
        if not os.path.exists(self.archivo_csv):
            return ofertas
        
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8', newline='') as f:
                # Intentar detectar el delimitador
                try:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)
                    reader = csv.DictReader(f, dialect=dialect, delimiter=';')
                except:
                    f.seek(0)
                    reader = csv.DictReader(f, delimiter=';')
                
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
    
    def obtener_proximo_id(self) -> int:
        """Obtener el próximo ID para la nueva oferta"""
        ofertas = self.cargar_ofertas()
        if not ofertas:
            return 1
        
        # Encontrar el máximo ID numérico
        max_id = 0
        for oferta in ofertas:
            try:
                if oferta.id_registro and oferta.id_registro.isdigit():
                    id_num = int(oferta.id_registro)
                    max_id = max(max_id, id_num)
            except:
                continue
        
        return max_id + 1
    
    def obtener_proximo_ies_id(self) -> str:
        """Obtener el próximo IES_ID"""
        ofertas = self.cargar_ofertas()
        if not ofertas:
            return "1"
        
        # Encontrar el máximo IES_ID numérico
        max_id = 0
        for oferta in ofertas:
            try:
                if oferta.ies_id and oferta.ies_id.isdigit():
                    id_num = int(oferta.ies_id)
                    max_id = max(max_id, id_num)
            except:
                continue
        
        return str(max_id + 1)
    
    def obtener_valores_unicos(self, campo: str) -> List[str]:
        """Obtener valores únicos para un campo específico (para combobox)"""
        ofertas = self.cargar_ofertas()
        valores = set()
        
        for oferta in ofertas:
            valor = getattr(oferta, campo.lower(), '')
            if valor:
                valores.add(valor)
        
        return sorted(list(valores))
    
    def guardar_ofertas(self, ofertas: List[OfertaAcademica]) -> bool:
        """Guardar todas las ofertas en el archivo CSV"""
        try:
            # Convertir a diccionarios
            datos = [oferta.to_dict() for oferta in ofertas]
            
            if not datos:
                return False
            
            # Escribir en CSV con delimitador punto y coma
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'IES_ID', 'IES_ID_SNIESE', 'IES_NOMBRE_INSTIT', 'PRO_NOMBRE', 'CAN_NOMBRE',
                    'PRQ_NOMBRE', 'CAR_NOMBRE_CARRERA', 'AREA_NOMBRE', 'SUBAREA_NOMBRE', 'NIVEL',
                    'MODALIDAD', 'JORNADA', 'OFA_TITULO', 'OFA_ID', 'CUS_ID', 'CUS_CUPOS_NIVELACION',
                    'CUS_CUPOS_PRIMER_SEMESTRE', 'CUS_CUPOS_PC', 'CUS_TOTAL_CUPOS', 'DESCRIPCION_TIPO_CUPO',
                    'FOCALIZADA', 'id', 'fecha_registro'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
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
            
            # Asignar ID progresivo
            proximo_id = self.obtener_proximo_id()
            oferta.id_registro = str(proximo_id)
            
            # Asignar IES_ID progresivo si no tiene
            if not oferta.ies_id:
                proximo_ies_id = self.obtener_proximo_ies_id()
                oferta.ies_id = proximo_ies_id
            
            # Generar IDs consecutivos si no tienen
            if not oferta.ofa_id:
                oferta.ofa_id = f"{str(proximo_id).zfill(6)}"
            if not oferta.cus_id:
                oferta.cus_id = f"{str(proximo_id).zfill(6)}"
            
            # Calcular total de cupos y tipo de cupo
            oferta.calcular_total_cupos()
            oferta._calcular_tipo_cupo()
            
            # Agregar nueva oferta
            ofertas.append(oferta)
            
            # Guardar todas las ofertas
            return self.guardar_ofertas(ofertas)
            
        except Exception as e:
            print(f"Error al agregar oferta: {e}")
            return False
    
    def eliminar_oferta(self, id_registro: str) -> bool:
        """Eliminar una oferta por ID de registro"""
        try:
            # Cargar ofertas existentes
            ofertas = self.cargar_ofertas()
            
            # Filtrar la oferta a eliminar
            ofertas_filtradas = [o for o in ofertas if o.id_registro != id_registro]
            
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
            if criterio == 'id' and oferta.id_registro == valor:
                resultados.append(oferta)
            elif criterio == 'carrera' and valor.lower() in oferta.car_nombre_carrera.lower():
                resultados.append(oferta)
            elif criterio == 'universidad' and valor.lower() in oferta.ies_nombre_instit.lower():
                resultados.append(oferta)
            elif criterio == 'area' and valor.lower() in oferta.area_nombre.lower():
                resultados.append(oferta)
            elif criterio == 'provincia' and valor.lower() in oferta.pro_nombre.lower():
                resultados.append(oferta)
        
        return resultados
    
    def actualizar_oferta(self, id_registro: str, datos_actualizados: Dict) -> bool:
        """Actualizar una oferta existente"""
        try:
            # Cargar ofertas existentes
            ofertas = self.cargar_ofertas()
            
            # Buscar y actualizar la oferta
            for i, oferta in enumerate(ofertas):
                if oferta.id_registro == id_registro:
                    # Actualizar campos
                    for key, value in datos_actualizados.items():
                        if hasattr(oferta, key):
                            setattr(oferta, key, value)
                    
                    # Recalcular total de cupos y tipo de cupo
                    oferta.calcular_total_cupos()
                    oferta._calcular_tipo_cupo()
                    
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
            
            with open(ruta_csv, 'r', encoding='utf-8', newline='') as f:
                # Intentar detectar delimitador
                try:
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)
                    reader = csv.DictReader(f, dialect=dialect)
                except:
                    f.seek(0)
                    reader = csv.DictReader(f, delimiter=';')
                
                for row in reader:
                    try:
                        # Crear oferta desde diccionario
                        oferta = OfertaAcademica.from_dict(row)
                        
                        if oferta.validar():
                            ofertas_importadas.append(oferta)
                            
                    except Exception as e:
                        print(f"Error al procesar fila: {e}")
                        continue
            
            # Agregar todas las ofertas importadas
            ofertas_existentes = self.cargar_ofertas()
            todas_ofertas = ofertas_existentes + ofertas_importadas
            
            # Asignar IDs progresivos a las nuevas ofertas
            for i, oferta in enumerate(ofertas_importadas):
                if not oferta.id_registro:
                    proximo_id = self.obtener_proximo_id() + i
                    oferta.id_registro = str(proximo_id)
            
            # Guardar
            if self.guardar_ofertas(todas_ofertas):
                return len(ofertas_importadas)
            else:
                return 0
                
        except Exception as e:
            print(f"Error al importar CSV: {e}")
            return 0