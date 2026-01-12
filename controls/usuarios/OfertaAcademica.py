import csv
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

class OfertaAcademica:
    _archivo_csv = "oferta.csv"
    _encabezados_csv = ["id_oferta_academica", "facultad", "carrera", "carrera_ter", "cupos_disponibles", "modalidad", "fecha_registro", "publicada"]
    
    def __init__(self, id_oferta_academica: str, facultad: str, carrera: str, carrera_ter: str, 
                 cupos_disponibles: int, modalidad: str, publicada: bool = False):
        if not id_oferta_academica or not isinstance(id_oferta_academica, str):
            raise ValueError("El ID de oferta académica es obligatorio y debe ser una cadena de texto")
        
        if cupos_disponibles < 0:
            raise ValueError("Los cupos disponibles no pueden ser negativos")
        
        modalidades_validas = ["presencial", "virtual", "híbrida", "semipresencial"]
        if modalidad.lower() not in modalidades_validas:
            raise ValueError(f"Modalidad no válida. Debe ser una de: {', '.join(modalidades_validas)}")
        
        self._id_oferta_academica = id_oferta_academica
        self._facultad = facultad
        self._carrera = carrera
        self._carrera_ter = carrera_ter
        self._cupos_disponibles = cupos_disponibles
        self._modalidad = modalidad.lower()
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._publicada = publicada
    
    @property
    def id_oferta_academica(self) -> str:
        return self._id_oferta_academica
    
    @property
    def facultad(self) -> str:
        return self._facultad
    
    @property
    def carrera(self) -> str:
        return self._carrera
    
    @property
    def carrera_ter(self) -> str:
        return self._carrera_ter
    
    @property
    def cupos_disponibles(self) -> int:
        return self._cupos_disponibles
    
    @property
    def modalidad(self) -> str:
        return self._modalidad
    
    @property
    def fecha_registro(self) -> str:
        return self._fecha_registro
    
    @property
    def publicada(self) -> bool:
        return self._publicada
    
    @facultad.setter
    def facultad(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("La facultad es obligatoria y debe ser una cadena de texto")
        self._facultad = value
    
    @carrera.setter
    def carrera(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("La carrera es obligatoria y debe ser una cadena de texto")
        self._carrera = value
    
    @carrera_ter.setter
    def carrera_ter(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("El campo carrera_ter es obligatorio y debe ser una cadena de texto")
        self._carrera_ter = value
    
    @cupos_disponibles.setter
    def cupos_disponibles(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Los cupos disponibles deben ser un número entero")
        if value < 0:
            raise ValueError("Los cupos disponibles no pueden ser negativos")
        self._cupos_disponibles = value
    
    @modalidad.setter
    def modalidad(self, value: str):
        modalidades_validas = ["presencial", "virtual", "híbrida", "semipresencial"]
        if value.lower() not in modalidades_validas:
            raise ValueError(f"Modalidad no válida. Debe ser una de: {', '.join(modalidades_validas)}")
        self._modalidad = value.lower()
    
    @publicada.setter
    def publicada(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("El estado de publicación debe ser un valor booleano")
        self._publicada = value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_oferta_academica": self._id_oferta_academica,
            "facultad": self._facultad,
            "carrera": self._carrera,
            "carrera_ter": self._carrera_ter,
            "cupos_disponibles": self._cupos_disponibles,
            "modalidad": self._modalidad,
            "fecha_registro": self._fecha_registro,
            "publicada": self._publicada
        }
    
    def __str__(self) -> str:
        estado = "Publicada" if self._publicada else "No publicada"
        return (f"Oferta Académica ID: {self._id_oferta_academica}\n"
                f"Facultad: {self._facultad}\n"
                f"Carrera: {self._carrera}\n"
                f"Carrera Ter: {self._carrera_ter}\n"
                f"Cupos disponibles: {self._cupos_disponibles}\n"
                f"Modalidad: {self._modalidad}\n"
                f"Fecha de registro: {self._fecha_registro}\n"
                f"Estado: {estado}")
    
    @classmethod
    def registrar_oferta(cls, oferta: 'OfertaAcademica') -> bool:
        try:
            archivo_existe = os.path.exists(cls._archivo_csv)
            datos = oferta.to_dict()
            
            with open(cls._archivo_csv, 'a', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=cls._encabezados_csv)
                
                if not archivo_existe:
                    writer.writeheader()
                
                writer.writerow(datos)
            
            print(f"Oferta académica {oferta.id_oferta_academica} registrada exitosamente.")
            return True
        
        except Exception as e:
            print(f"Error al registrar la oferta académica: {e}")
            return False
    
    @classmethod
    def modificar_oferta(cls, id_oferta: str, **kwargs) -> bool:
        try:
            ofertas = cls._leer_ofertas_desde_csv()
            
            oferta_encontrada = None
            for oferta in ofertas:
                if oferta["id_oferta_academica"] == id_oferta:
                    oferta_encontrada = oferta
                    break
            
            if not oferta_encontrada:
                print(f"No se encontró la oferta académica con ID: {id_oferta}")
                return False
            
            campos_validos = ["facultad", "carrera", "carrera_ter", "cupos_disponibles", "modalidad", "publicada"]
            for campo, valor in kwargs.items():
                if campo in campos_validos:
                    oferta_encontrada[campo] = valor
            
            with open(cls._archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=cls._encabezados_csv)
                writer.writeheader()
                writer.writerows(ofertas)
            
            print(f"Oferta académica {id_oferta} modificada exitosamente.")
            return True
        
        except Exception as e:
            print(f"Error al modificar la oferta académica: {e}")
            return False
    
    @classmethod
    def eliminar_oferta(cls, id_oferta: str) -> bool:
        try:
            ofertas = cls._leer_ofertas_desde_csv()
            ofertas_originales = len(ofertas)
            ofertas = [oferta for oferta in ofertas if oferta["id_oferta_academica"] != id_oferta]
            
            if len(ofertas) == ofertas_originales:
                print(f"No se encontró la oferta académica con ID: {id_oferta}")
                return False
            
            with open(cls._archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.DictWriter(archivo, fieldnames=cls._encabezados_csv)
                writer.writeheader()
                writer.writerows(ofertas)
            
            print(f"Oferta académica {id_oferta} eliminada exitosamente.")
            return True
        
        except Exception as e:
            print(f"Error al eliminar la oferta académica: {e}")
            return False
    
    @classmethod
    def publicar_oferta(cls, id_oferta: str) -> bool:
        return cls.modificar_oferta(id_oferta, publicada=True)
    
    @classmethod
    def obtener_oferta_por_id(cls, id_oferta: str) -> Optional['OfertaAcademica']:
        try:
            ofertas = cls._leer_ofertas_desde_csv()
            
            for oferta_dict in ofertas:
                if oferta_dict["id_oferta_academica"] == id_oferta:
                    return OfertaAcademica(
                        id_oferta_academica=oferta_dict["id_oferta_academica"],
                        facultad=oferta_dict["facultad"],
                        carrera=oferta_dict["carrera"],
                        carrera_ter=oferta_dict["carrera_ter"],
                        cupos_disponibles=int(oferta_dict["cupos_disponibles"]),
                        modalidad=oferta_dict["modalidad"],
                        publicada=oferta_dict["publicada"].lower() == "true"
                    )
            
            return None
        
        except Exception as e:
            print(f"Error al obtener la oferta académica: {e}")
            return None
    
    @classmethod
    def obtener_todas_ofertas(cls) -> List['OfertaAcademica']:
        try:
            ofertas_dict = cls._leer_ofertas_desde_csv()
            ofertas = []
            
            for oferta_dict in ofertas_dict:
                oferta = OfertaAcademica(
                    id_oferta_academica=oferta_dict["id_oferta_academica"],
                    facultad=oferta_dict["facultad"],
                    carrera=oferta_dict["carrera"],
                    carrera_ter=oferta_dict["carrera_ter"],
                    cupos_disponibles=int(oferta_dict["cupos_disponibles"]),
                    modalidad=oferta_dict["modalidad"],
                    publicada=oferta_dict["publicada"].lower() == "true"
                )
                ofertas.append(oferta)
            
            return ofertas
        
        except Exception as e:
            print(f"Error al obtener todas las ofertas académicas: {e}")
            return []
    
    @classmethod
    def _leer_ofertas_desde_csv(cls) -> List[Dict[str, str]]:
        if not os.path.exists(cls._archivo_csv):
            return []
        
        ofertas = []
        with open(cls._archivo_csv, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                ofertas.append(fila)
        
        return ofertas

class SistemaOfertasAcademicas:
    @staticmethod
    def mostrar_menu():
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE OFERTAS ACADÉMICAS")
        print("="*50)
        print("1. Registrar nueva oferta académica")
        print("2. Modificar oferta académica")
        print("3. Eliminar oferta académica")
        print("4. Publicar oferta académica")
        print("5. Consultar oferta por ID")
        print("6. Mostrar todas las ofertas")
        print("7. Salir")
        print("="*50)
    
    @staticmethod
    def registrar_oferta_interactivo():
        print("\n--- REGISTRAR NUEVA OFERTA ACADÉMICA ---")
        
        try:
            id_oferta = input("ID de la oferta académica: ").strip()
            facultad = input("Facultad: ").strip()
            carrera = input("Carrera: ").strip()
            carrera_ter = input("Carrera Ter: ").strip()
            cupos = int(input("Cupos disponibles: ").strip())
            modalidad = input("Modalidad (presencial/virtual/híbrida/semipresencial): ").strip()
            
            nueva_oferta = OfertaAcademica(
                id_oferta_academica=id_oferta,
                facultad=facultad,
                carrera=carrera,
                carrera_ter=carrera_ter,
                cupos_disponibles=cupos,
                modalidad=modalidad
            )
            
            if OfertaAcademica.registrar_oferta(nueva_oferta):
                print("¡Oferta académica registrada exitosamente!")
        
        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    @staticmethod
    def modificar_oferta_interactivo():
        print("\n--- MODIFICAR OFERTA ACADÉMICA ---")
        
        id_oferta = input("ID de la oferta académica a modificar: ").strip()
        
        oferta = OfertaAcademica.obtener_oferta_por_id(id_oferta)
        if not oferta:
            print(f"No se encontró la oferta académica con ID: {id_oferta}")
            return
        
        print(f"\nOferta actual: {oferta}")
        print("\nIngrese los nuevos valores (deje en blanco para mantener el valor actual):")
        
        cambios = {}
        
        facultad = input(f"Facultad [{oferta.facultad}]: ").strip()
        if facultad:
            cambios["facultad"] = facultad
        
        carrera = input(f"Carrera [{oferta.carrera}]: ").strip()
        if carrera:
            cambios["carrera"] = carrera
        
        carrera_ter = input(f"Carrera Ter [{oferta.carrera_ter}]: ").strip()
        if carrera_ter:
            cambios["carrera_ter"] = carrera_ter
        
        cupos = input(f"Cupos disponibles [{oferta.cupos_disponibles}]: ").strip()
        if cupos:
            cambios["cupos_disponibles"] = int(cupos)
        
        modalidad = input(f"Modalidad [{oferta.modalidad}]: ").strip()
        if modalidad:
            cambios["modalidad"] = modalidad
        
        if cambios:
            if OfertaAcademica.modificar_oferta(id_oferta, **cambios):
                print("¡Oferta académica modificada exitosamente!")
        else:
            print("No se realizaron cambios.")
    
    @staticmethod
    def eliminar_oferta_interactivo():
        print("\n--- ELIMINAR OFERTA ACADÉMICA ---")
        
        id_oferta = input("ID de la oferta académica a eliminar: ").strip()
        
        confirmacion = input(f"¿Está seguro de eliminar la oferta {id_oferta}? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            if OfertaAcademica.eliminar_oferta(id_oferta):
                print("¡Oferta académica eliminada exitosamente!")
        else:
            print("Operación cancelada.")
    
    @staticmethod
    def publicar_oferta_interactivo():
        print("\n--- PUBLICAR OFERTA ACADÉMICA ---")
        
        id_oferta = input("ID de la oferta académica a publicar: ").strip()
        
        if OfertaAcademica.publicar_oferta(id_oferta):
            print("¡Oferta académica publicada exitosamente!")
    
    @staticmethod
    def consultar_oferta_interactivo():
        print("\n--- CONSULTAR OFERTA ACADÉMICA ---")
        
        id_oferta = input("ID de la oferta académica a consultar: ").strip()
        
        oferta = OfertaAcademica.obtener_oferta_por_id(id_oferta)
        
        if oferta:
            print(f"\n{oferta}")
        else:
            print(f"No se encontró la oferta académica con ID: {id_oferta}")
    
    @staticmethod
    def mostrar_todas_ofertas():
        print("\n--- TODAS LAS OFERTAS ACADÉMICAS ---")
        
        ofertas = OfertaAcademica.obtener_todas_ofertas()
        
        if not ofertas:
            print("No hay ofertas académicas registradas.")
            return
        
        for i, oferta in enumerate(ofertas, 1):
            print(f"\n{i}. {oferta}")
            print("-" * 40)