
from typing import List, Dict, Any
from abc import ABC, abstractmethod

# ========== OBSERVER PATTERN ==========
class ObservadorCarrera(ABC):
    @abstractmethod
    def actualizar(self, carrera: 'Carrera', evento: str):
        pass

class ObservadorLog(ObservadorCarrera):
    def actualizar(self, carrera: 'Carrera', evento: str):
        print(f"[OBSERVADOR] Carrera '{carrera.nombre_carrera}': {evento}")

# ========== CLASE CARRERA ==========
class Carrera:
    def __init__(self, id_carrera: str, nombre_carrera: str, duracion: int, jornada: str):
        self._validar_datos(id_carrera, nombre_carrera, duracion, jornada)
        
        self._id_carrera = id_carrera.strip()
        self._nombre_carrera = nombre_carrera.strip()
        self._duracion = duracion
        self._jornada = jornada.strip().upper()
        
        self._cursos: List[Dict[str, Any]] = []
        self._observadores: List[ObservadorCarrera] = []
    
    def _validar_datos(self, id_carrera: str, nombre_carrera: str, duracion: int, jornada: str):
        if not id_carrera or not id_carrera.strip():
            raise ValueError("ID de carrera no puede estar vacío")
        if not nombre_carrera or not nombre_carrera.strip():
            raise ValueError("Nombre de carrera no puede estar vacío")
        if duracion <= 0 or duracion > 10:
            raise ValueError("Duración debe estar entre 1 y 10 años")
        if jornada.upper() not in ["MATUTINA", "VESPERTINA", "NOCTURNA", "MIXTA"]:
            raise ValueError("Jornada inválida. Use: MATUTINA, VESPERTINA, NOCTURNA, MIXTA")
    
    @property
    def id_carrera(self) -> str:
        return self._id_carrera
    
    @property
    def nombre_carrera(self) -> str:
        return self._nombre_carrera
    
    @nombre_carrera.setter
    def nombre_carrera(self, value: str):
        if not value or not value.strip():
            raise ValueError("Nombre de carrera no puede estar vacío")
        self._nombre_carrera = value.strip()
        self._notificar_observadores(f"Nombre cambiado a: {value}")
    
    @property
    def duracion(self) -> int:
        return self._duracion
    
    @duracion.setter
    def duracion(self, value: int):
        if value <= 0 or value > 10:
            raise ValueError("Duración debe estar entre 1 y 10 años")
        self._duracion = value
        self._notificar_observadores(f"Duración cambiada a: {value} años")
    
    @property
    def jornada(self) -> str:
        return self._jornada
    
    @jornada.setter
    def jornada(self, value: str):
        if value.upper() not in ["MATUTINA", "VESPERTINA", "NOCTURNA", "MIXTA"]:
            raise ValueError("Jornada inválida")
        self._jornada = value.strip().upper()
        self._notificar_observadores(f"Jornada cambiada a: {value}")
    
    # ========== MÉTODOS DE CURSOS ==========
    def listarCursos(self) -> List[Dict[str, Any]]:
        return self._cursos.copy()
    
    def agregar_curso(self, id_curso: str, nombre_curso: str, creditos: int):
        if not id_curso or not id_curso.strip():
            raise ValueError("ID del curso no puede estar vacío")
        if not nombre_curso or not nombre_curso.strip():
            raise ValueError("Nombre del curso no puede estar vacío")
        if creditos <= 0 or creditos > 10:
            raise ValueError("Créditos deben estar entre 1 y 10")
        
        for curso in self._cursos:
            if curso['id_curso'] == id_curso:
                raise ValueError(f"Ya existe un curso con ID {id_curso}")
        
        curso = {
            'id_curso': id_curso.strip(),
            'nombre': nombre_curso.strip(),
            'creditos': creditos
        }
        
        self._cursos.append(curso)
        self._notificar_observadores(f"Curso agregado: {nombre_curso}")
        return curso
    
    def eliminar_curso(self, id_curso: str):
        for i, curso in enumerate(self._cursos):
            if curso['id_curso'] == id_curso:
                curso_eliminado = self._cursos.pop(i)
                self._notificar_observadores(f"Curso eliminado: {curso_eliminado['nombre']}")
                return True
        raise ValueError(f"No se encontró curso con ID {id_curso}")
    
    def obtener_curso_por_id(self, id_curso: str) -> Dict[str, Any]:
        for curso in self._cursos:
            if curso['id_curso'] == id_curso:
                return curso
        raise ValueError(f"No se encontró curso con ID {id_curso}")
    
    # ========== MÉTODOS OBSERVADORES ==========
    def asignarObservador(self, observador: ObservadorCarrera):
        if not observador:
            raise ValueError("Debe proporcionar un observador válido")
        
        if observador not in self._observadores:
            self._observadores.append(observador)
            self._notificar_observadores("Nuevo observador asignado")
    
    def remover_observador(self, observador: ObservadorCarrera):
        if observador in self._observadores:
            self._observadores.remove(observador)
            self._notificar_observadores("Observador removido")
    
    def _notificar_observadores(self, evento: str):
        for observador in self._observadores:
            try:
                observador.actualizar(self, evento)
            except Exception as e:
                print(f"Error notificando observador: {e}")
    
    # ========== MÉTODOS ADICIONALES ==========
    def obtener_total_cursos(self) -> int:
        return len(self._cursos)
    
    def obtener_total_creditos(self) -> int:
        return sum(curso['creditos'] for curso in self._cursos)
    
    def obtener_resumen(self) -> Dict[str, Any]:
        return {
            'id_carrera': self._id_carrera,
            'nombre_carrera': self._nombre_carrera,
            'duracion': self._duracion,
            'jornada': self._jornada,
            'total_cursos': self.obtener_total_cursos(),
            'total_creditos': self.obtener_total_creditos(),
            'observadores': len(self._observadores)
        }
    
    def __str__(self):
        return f"{self._nombre_carrera} (ID: {self._id_carrera}, Duración: {self._duracion} años, Jornada: {self._jornada})"