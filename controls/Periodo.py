import datetime
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import csv
import os

class EstadoPeriodo(Enum):
    PLANIFICADO = "PLANIFICADO"
    ABIERTO = "ABIERTO"
    CERRADO = "CERRADO"

class GestionPeriodo(ABC):
    @abstractmethod
    def abrir_periodo(self) -> bool:
        pass
    
    @abstractmethod
    def cerrar_periodo(self) -> bool:
        pass
    
    @abstractmethod
    def cambiar_periodo(self, nueva_fecha_inicio: datetime.date, nueva_fecha_fin: datetime.date) -> bool:
        pass

class ValidadorFechas:
    def __init__(self, fecha_inicio: datetime.date, fecha_fin: datetime.date):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
    
    def validar(self) -> bool:
        if not self.fecha_inicio or not self.fecha_fin:
            return False
        
        if self.fecha_inicio > self.fecha_fin:
            return False
        
        return True

@dataclass
class EntidadBase:
    id: int
    fecha_creacion: datetime.datetime = datetime.datetime.now()
    fecha_actualizacion: datetime.datetime = datetime.datetime.now()
    
    def actualizar_fecha_modificacion(self):
        self.fecha_actualizacion = datetime.datetime.now()

class Periodo(EntidadBase, GestionPeriodo):
    
    def __init__(self, id_periodo: int, fecha_inicio: datetime.date, fecha_fin: datetime.date):
        super().__init__(id_periodo)
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = EstadoPeriodo.PLANIFICADO
        self._validar_fechas_iniciales()
    
    def _validar_fechas_iniciales(self):
        validador = ValidadorFechas(self._fecha_inicio, self._fecha_fin)
        if not validador.validar():
            raise ValueError("Las fechas del período no son válidas")
    
    @property
    def fecha_inicio(self) -> datetime.date:
        return self._fecha_inicio
    
    @fecha_inicio.setter
    def fecha_inicio(self, valor: datetime.date):
        if not valor:
            raise ValueError("La fecha de inicio no puede estar vacía")
        
        if self._estado == EstadoPeriodo.ABIERTO:
            raise ValueError("No se puede modificar la fecha de inicio de un período abierto")
        
        validador = ValidadorFechas(valor, self._fecha_fin)
        if not validador.validar():
            raise ValueError("La nueva fecha de inicio no es válida")
        
        self._fecha_inicio = valor
        self.actualizar_fecha_modificacion()
    
    @property
    def fecha_fin(self) -> datetime.date:
        return self._fecha_fin
    
    @fecha_fin.setter
    def fecha_fin(self, valor: datetime.date):
        if not valor:
            raise ValueError("La fecha de fin no puede estar vacía")
        
        if self._estado == EstadoPeriodo.ABIERTO:
            raise ValueError("No se puede modificar la fecha de fin de un período abierto")
        
        validador = ValidadorFechas(self._fecha_inicio, valor)
        if not validador.validar():
            raise ValueError("La nueva fecha de fin no es válida")
        
        self._fecha_fin = valor
        self.actualizar_fecha_modificacion()
    
    @property
    def estado(self) -> EstadoPeriodo:
        return self._estado
    
    @property
    def duracion_dias(self) -> int:
        return (self._fecha_fin - self._fecha_inicio).days
    
    @property
    def dias_restantes(self) -> Optional[int]:
        if self._estado != EstadoPeriodo.ABIERTO:
            return None
        
        hoy = datetime.date.today()
        if hoy > self._fecha_fin:
            return 0
        
        return (self._fecha_fin - hoy).days
    
    def abrir_periodo(self) -> bool:
        if self._estado != EstadoPeriodo.PLANIFICADO:
            raise ValueError(f"No se puede abrir un período en estado {self._estado.value}")
        
        hoy = datetime.date.today()
        if hoy < self._fecha_inicio:
            raise ValueError("No se puede abrir un período antes de su fecha de inicio")
        
        self._estado = EstadoPeriodo.ABIERTO
        self.actualizar_fecha_modificacion()
        return True
    
    def cerrar_periodo(self) -> bool:
        if self._estado != EstadoPeriodo.ABIERTO:
            raise ValueError(f"No se puede cerrar un período en estado {self._estado.value}")
        
        hoy = datetime.date.today()
        if hoy < self._fecha_fin:
            raise ValueError("No se puede cerrar un período antes de su fecha de fin")
        
        self._estado = EstadoPeriodo.CERRADO
        self.actualizar_fecha_modificacion()
        return True
    
    def cambiar_periodo(self, nueva_fecha_inicio: datetime.date, nueva_fecha_fin: datetime.date) -> bool:
        if self._estado == EstadoPeriodo.ABIERTO:
            raise ValueError("No se puede cambiar un período que está abierto")
        
        if self._estado == EstadoPeriodo.CERRADO:
            raise ValueError("No se puede cambiar un período que está cerrado")
        
        validador = ValidadorFechas(nueva_fecha_inicio, nueva_fecha_fin)
        if not validador.validar():
            raise ValueError("Las nuevas fechas no son válidas")
        
        self._fecha_inicio = nueva_fecha_inicio
        self._fecha_fin = nueva_fecha_fin
        self.actualizar_fecha_modificacion()
        return True
    
    def esta_activo(self) -> bool:
        if self._estado != EstadoPeriodo.ABIERTO:
            return False
        
        hoy = datetime.date.today()
        return self._fecha_inicio <= hoy <= self._fecha_fin
    
    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'fecha_inicio': self.fecha_inicio.strftime("%Y-%m-%d"),
            'fecha_fin': self.fecha_fin.strftime("%Y-%m-%d"),
            'estado': self.estado.value,
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        try:
            id_periodo = int(data.get('id', 0))
            fecha_inicio = datetime.datetime.strptime(data.get('fecha_inicio'), "%Y-%m-%d").date()
            fecha_fin = datetime.datetime.strptime(data.get('fecha_fin'), "%Y-%m-%d").date()
            
            periodo = cls(id_periodo, fecha_inicio, fecha_fin)
            
            # Establecer estado
            estado_str = data.get('estado', 'PLANIFICADO')
            periodo._estado = EstadoPeriodo(estado_str)
            
            return periodo
        except Exception as e:
            raise ValueError(f"Error al crear periodo desde dict: {e}")
    
    def __str__(self) -> str:
        return f"Periodo(ID={self.id}, Inicio={self.fecha_inicio}, Fin={self.fecha_fin}, Estado={self.estado.value})"
    
    def __repr__(self) -> str:
        return f"Periodo(id={self.id}, fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin})"

class FabricaPeriodos:
    @staticmethod
    def crear_periodo(id_periodo: int, fecha_inicio: datetime.date, fecha_fin: datetime.date) -> Periodo:
        periodo = Periodo(id_periodo, fecha_inicio, fecha_fin)
        return periodo
    
    @staticmethod
    def crear_periodo_anual(anio: int, id_base: int = 1) -> Periodo:
        fecha_inicio = datetime.date(anio, 1, 1)
        fecha_fin = datetime.date(anio, 12, 31)
        return Periodo(id_base, fecha_inicio, fecha_fin)
    
    @staticmethod
    def crear_periodo_trimestral(anio: int, trimestre: int, id_base: int = 1) -> Periodo:
        if trimestre < 1 or trimestre > 4:
            raise ValueError("El trimestre debe estar entre 1 y 4")
        
        trimestres = {
            1: (1, 31, 3),
            2: (1, 4, 30, 6),
            3: (1, 7, 30, 9),
            4: (1, 10, 31, 12)
        }
        
        mes_inicio, dia_inicio, mes_fin, dia_fin = trimestres[trimestre]
        fecha_inicio = datetime.date(anio, mes_inicio, dia_inicio)
        fecha_fin = datetime.date(anio, mes_fin, dia_fin)
        
        return Periodo(id_base, fecha_inicio, fecha_fin)

class GestorPeriodosCSV:
    """Gestor para manejar periodos en archivo CSV"""
    
    def __init__(self, archivo_csv: str = None):
        if archivo_csv is None:
            # Ruta por defecto
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.archivo_csv = os.path.join(base_dir, "..", "data", "universidad", "periodos.csv")
        else:
            self.archivo_csv = archivo_csv
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.archivo_csv), exist_ok=True)
        
        # Inicializar archivo si no existe
        self._inicializar_archivo()
    
    def _inicializar_archivo(self):
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_creacion'])
    
    def cargar_periodos(self) -> list[Periodo]:
        """Cargar todos los periodos desde el archivo CSV"""
        periodos = []
        
        if not os.path.exists(self.archivo_csv):
            return periodos
        
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        periodo = Periodo.from_dict(row)
                        periodos.append(periodo)
                    except Exception as e:
                        print(f"Error al cargar periodo: {e}")
                        continue
        except Exception as e:
            print(f"Error al leer archivo CSV: {e}")
        
        return periodos
    
    def guardar_periodos(self, periodos: list[Periodo]) -> bool:
        """Guardar todos los periodos en el archivo CSV"""
        try:
            # Convertir periodos a diccionarios
            datos = []
            for periodo in periodos:
                datos.append(periodo.to_dict())
            
            if not datos:
                return False
            
            # Escribir en CSV
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_creacion']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(datos)
            
            return True
            
        except Exception as e:
            print(f"Error al guardar periodos: {e}")
            return False
    
    def agregar_periodo(self, fecha_inicio_str: str, fecha_fin_str: str) -> dict:
        """Agregar un nuevo periodo"""
        try:
            # Convertir strings a fechas
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
            
            # Validar fechas
            if fecha_inicio >= fecha_fin:
                return {"success": False, "message": "La fecha de inicio debe ser anterior a la fecha de fin"}
            
            # Cargar periodos existentes
            periodos = self.cargar_periodos()
            
            # Obtener siguiente ID
            if periodos:
                max_id = max(p.id for p in periodos)
                nuevo_id = max_id + 1
            else:
                nuevo_id = 1
            
            # Crear nuevo periodo
            nuevo_periodo = Periodo(nuevo_id, fecha_inicio, fecha_fin)
            
            # Determinar estado según fecha
            hoy = datetime.date.today()
            if fecha_inicio > hoy:
                nuevo_periodo._estado = EstadoPeriodo.PLANIFICADO
            else:
                nuevo_periodo._estado = EstadoPeriodo.ABIERTO
            
            # Agregar a la lista
            periodos.append(nuevo_periodo)
            
            # Guardar todos los periodos
            if self.guardar_periodos(periodos):
                return {
                    "success": True, 
                    "message": "Período agregado correctamente",
                    "periodo": nuevo_periodo
                }
            else:
                return {"success": False, "message": "Error al guardar el período"}
                
        except ValueError as e:
            return {"success": False, "message": f"Error en formato de fecha: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Error inesperado: {str(e)}"}
    
    def eliminar_periodo(self, periodo_id: str) -> dict:
        """Eliminar un periodo por ID"""
        try:
            # Cargar periodos existentes
            periodos = self.cargar_periodos()
            
            # Filtrar el periodo a eliminar
            periodos_filtrados = [p for p in periodos if str(p.id) != periodo_id]
            
            if len(periodos_filtrados) == len(periodos):
                return {"success": False, "message": "Período no encontrado"}
            
            # Verificar si el periodo está activo
            for p in periodos:
                if str(p.id) == periodo_id and p.esta_activo():
                    return {"success": False, "message": "No se puede eliminar un período activo"}
            
            # Guardar periodos actualizados
            if self.guardar_periodos(periodos_filtrados):
                return {"success": True, "message": "Período eliminado correctamente"}
            else:
                return {"success": False, "message": "Error al guardar los períodos"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def obtener_periodo_activo(self) -> Optional[Periodo]:
        """Obtener el periodo activo actual"""
        periodos = self.cargar_periodos()
        
        for periodo in periodos:
            if periodo.esta_activo():
                return periodo
        
        return None
    
    def actualizar_estados(self):
        """Actualizar estados de periodos según fecha actual"""
        periodos = self.cargar_periodos()
        hoy = datetime.date.today()
        cambios = False
        
        for periodo in periodos:
            # Si está PLANIFICADO y la fecha ya pasó, cambiarlo a ABIERTO
            if periodo.estado == EstadoPeriodo.PLANIFICADO and periodo.fecha_inicio <= hoy:
                periodo._estado = EstadoPeriodo.ABIERTO
                periodo.actualizar_fecha_modificacion()
                cambios = True
            
            # Si está ABIERTO y la fecha ya pasó, cambiarlo a CERRADO
            elif periodo.estado == EstadoPeriodo.ABIERTO and periodo.fecha_fin < hoy:
                periodo._estado = EstadoPeriodo.CERRADO
                periodo.actualizar_fecha_modificacion()
                cambios = True
        
        if cambios:
            self.guardar_periodos(periodos)