from typing import List, Dict, Any, Optional

class Facultad:
    def __init__(self, id_facultad: str, nombre_facultad: str):
        if not id_facultad or not id_facultad.strip():
            raise ValueError("ID de facultad no puede estar vacío")
        if not nombre_facultad or not nombre_facultad.strip():
            raise ValueError("Nombre de facultad no puede estar vacío")
        
        self._id_facultad = id_facultad.strip()
        self._nombre_facultad = nombre_facultad.strip()
        self._carreras: List['Carrera'] = []
    
    @property
    def id_facultad(self) -> str:
        return self._id_facultad
    
    @property
    def nombre_facultad(self) -> str:
        return self._nombre_facultad
    
    @nombre_facultad.setter
    def nombre_facultad(self, value: str):
        if not value or not value.strip():
            raise ValueError("Nombre de facultad no puede estar vacío")
        self._nombre_facultad = value.strip()
    
    def agregarCarrera(self, carrera: 'Carrera'):
        if not carrera:
            raise ValueError("Debe proporcionar una carrera válida")
        
        for c in self._carreras:
            if c.id_carrera == carrera.id_carrera:
                raise ValueError(f"Ya existe una carrera con ID {carrera.id_carrera}")
        
        self._carreras.append(carrera)
        return True
    
    def eliminarCarrera(self, id_carrera: str):
        for i, carrera in enumerate(self._carreras):
            if carrera.id_carrera == id_carrera:
                self._carreras.pop(i)
                return True
        raise ValueError(f"No se encontró carrera con ID {id_carrera}")
    
    def listaCarreras(self) -> List['Carrera']:
        return self._carreras.copy()
    
    def obtener_carrera_por_id(self, id_carrera: str) -> Optional['Carrera']:
        for carrera in self._carreras:
            if carrera.id_carrera == id_carrera:
                return carrera
        return None
    
    def obtener_total_carreras(self) -> int:
        return len(self._carreras)
    
    def __str__(self):
        return f"{self._nombre_facultad} (ID: {self._id_facultad}, Carreras: {len(self._carreras)})"