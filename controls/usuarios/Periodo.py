import datetime
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class EstadoPeriodo(Enum):
    ABIERTO = "ABIERTO"
    CERRADO = "CERRADO"
    PLANIFICADO = "PLANIFICADO"

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
        
        if self.fecha_inicio < datetime.date.today() and self.fecha_fin < datetime.date.today():
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