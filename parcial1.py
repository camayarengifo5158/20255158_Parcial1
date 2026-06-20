#Commit 2 Evolucion del dominio ante cambios 

class Bibliotecario:
    def __init__(self, nombre_empleado:str, codigo_usuario:str):
        self.nombre_empleado = nombre_empleado
        self.codigo_usuario = codigo_usuario

class Recurso:
    def __init__(self, codigo_identificador:str, horas_retraso:int, dias_retraso:int):
        self.codigo_identificador = codigo_identificador
        self.horas_retraso = 0
        self.dias_retraso = 0

    def calcular_multa(self, horas_retraso:int, dias_retraso:int, alumnos_espera:int):
        pass

class RegistroAtencion:
    def __init__(self, id, carnet_alumno:str, nombre_empleado:str, codigo_usuario:str):
        self.id = id    
        self.carnet_alumno = carnet_alumno
        self._recursos :list[Recurso] = []
        self.bibliotecario = Bibliotecario(nombre_empleado, codigo_usuario)
        self.estado = "CUENTA_ACTIVA"

    @property
    def recursos(self):
        return tuple(self._recursos)
    
    def ejecutar_auditoria(self, horas_retraso:int, dias_retraso:int, alumnos_espera:int):
        total_multa = 0
        for recurso in self._recursos:
            total_multa += recurso.calcular_multa(horas_retraso, dias_retraso, alumnos_espera)
        
        promedio_multas = total_multa / len(self._recursos) if len(self._recursos) > 0 else 0
        
        if promedio_multas > 15.00:
            self.estado = "CUENTA_SUSPENDIDA"
        
        elif self.bibliotecario.codigo_usuario.startswith('AUX'):
            for recurso in self._recursos:
                if isinstance(recurso, UsoSalaEstudio) and recurso.alumnos_espera > 10:
                    self.estado = "CUENTA_SUSPENDIDA"
                    break
        
        return total_multa
    
    def agregar_recurso(self, recurso:Recurso):
        if len(self._recursos) >= 4:
            raise ValueError("Limite de recursos por atencion alcanzado")
        self._recursos.append(recurso)

class PrestamoLibro(Recurso):
    def __init__(self, codigo_identificador:str, horas_retraso:int, dias_retraso:int):
        super().__init__(codigo_identificador, horas_retraso, dias_retraso)

    def calcular_multa(self, horas_retraso:int, dias_retraso:int, alumnos_espera:int):
        total_multa = 0
        if dias_retraso > 0:
            total_multa += dias_retraso * 2.50
        return total_multa

class UsoSalaEstudio(Recurso):
    def __init__(self, codigo_identificador:str, horas_retraso:int, dias_retraso:int, alumnos_espera:int = 0):
        super().__init__(codigo_identificador, horas_retraso, dias_retraso)
        self.alumnos_espera = alumnos_espera

    def calcular_multa(self, horas_retraso:int, dias_retraso:int, alumnos_espera:int):
        total_multa = 0
        if horas_retraso > 0:
            total_multa += horas_retraso * (alumnos_espera / 1000)
        return total_multa
