# Entendiendo la Arquitectura de la Aplicación EnForma

## Preguntas clave

### 1. **¿Cuáles son los componentes funcionales de la aplicación y cómo se relacionan entre sí?**

La aplicación "EnForma" es un sistema de gestión de entrenamientos físicos que sigue un patrón arquitectónico de 3 capas (3-tier architecture):

**Componentes principales:**
- **Capa de Presentación (Vista)**: Interfaces gráficas implementadas con PyQt5
  - `InterfazEnForma.py`: Controlador principal de la aplicación
  - `VistaListaPersonas.py`: Gestión de lista de personas
  - `VistaPersona.py`: Creación/edición de personas
  - `VistaListaEjercicios.py`: Gestión de ejercicios
  - `VistaListaEntrenamientos.py`: Gestión de entrenamientos
  - `VistaReporte.py`: Generación de reportes

- **Capa de Lógica de Negocio**: Procesamiento de reglas de negocio
  - `FachadaEnForma.py`: Interfaz abstracta que define contratos
  - `LogicaEnForma.py`: Implementación real de la lógica de negocio
  - `LogicaMock.py`: Implementación mock para pruebas

- **Capa de Datos (Modelo)**: Persistencia y modelos de datos
  - `declarative_base.py`: Configuración de SQLAlchemy
  - `persona.py`: Modelo de datos para personas
  - `ejercicio.py`: Modelo de datos para ejercicios
  - `ejercicioEntrenado.py`: Modelo de relación persona-ejercicio

**Relaciones:**
- La vista se comunica únicamente con la lógica a través de la fachada
- La lógica accede a los datos mediante SQLAlchemy ORM
- Implementa el patrón Facade para simplificar la comunicación entre capas

### 2. **¿Cómo es el despliegue de los componentes en el entorno productivo?**

**Estrategia de despliegue:**
- **Containerización**: Utiliza Docker con imagen Python 3.7.6 -- Alucinación no tener en cuenta

- **CI/CD Pipeline**: Jenkins configurado con las siguientes etapas:
  - Checkout del código desde GitHub
  - Análisis de código con GitInspector
  - Instalación de dependencias
  - Ejecución de pruebas unitarias
  - Generación de reportes de cobertura
  - Limpieza automática del workspace

**Infraestructura:**
- Servidor Jenkins: `http://157.253.238.75:8080/jenkins-misovirtual/`
- Base de datos SQLite local (`identifier.sqlite`)
- Aplicación de escritorio (no requiere servidor web)

### 3. **¿Cómo interactúan los componentes con las fuentes de datos?**

**Patrón de acceso a datos:**
- **ORM**: SQLAlchemy como Object-Relational Mapping
- **Base de datos**: SQLite para persistencia local
- **Patrón Session**: Gestión de transacciones mediante sesiones de SQLAlchemy

**Configuración de datos:**
```python
engine = create_engine('sqlite:///identifier.sqlite')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()
```

**Modelos de datos:**
- `Persona`: Datos personales y medidas corporales
- `Ejercicio`: Catálogo de ejercicios con información de YouTube
- `EjercicioEntrenado`: Registro de entrenamientos realizados

### 4. **¿Qué patrones y tácticas de arquitectura se están utilizando?**

**Patrones arquitectónicos:**
- **Model-View-Controller (MVC)**: Separación clara de responsabilidades
- **Facade Pattern**: `FachadaEnForma` como punto único de entrada
- **Strategy Pattern**: Intercambio entre `LogicaEnForma` y `LogicaMock`
- **Repository Pattern**: Encapsulación del acceso a datos mediante SQLAlchemy
- **3-Layer Architecture**: Presentación, Lógica, Datos

**Tácticas de arquitectura:**
- **Loose Coupling**: Dependencias através de interfaces abstractas
- **Separation of Concerns**: Cada capa tiene responsabilidades específicas
- **Dependency Injection**: Inyección de la lógica en la interfaz
- **Template Method**: Métodos abstractos en `FachadaEnForma`

### 5. **¿Qué tecnologías y frameworks forman parte de la arquitectura?**

**Stack tecnológico:**
- **Lenguaje**: Python 3.7.6
- **Framework de UI**: PyQt5 5.15.2 para interfaces gráficas
- **ORM**: SQLAlchemy 1.3.20 para mapeo objeto-relacional
- **Base de datos**: SQLite (embebida)
- **Testing**: unittest (biblioteca estándar de Python)
- **Cobertura**: coverage 5.3
- **Validación**: validators, faker para pruebas
- **CI/CD**: Jenkins
- **Containerización**: Docker

**Dependencias adicionales:**
- `datetime`: Manejo de fechas
- `enum`: Enumeraciones para clasificaciones
- `re`: Expresiones regulares para validaciones

### 6. **¿Cuáles son los principales módulos o capas en la aplicación?**

**Estructura modular:**

```
src/
├── vista/           # Capa de Presentación
├── logica/          # Capa de Lógica de Negocio  
├── modelo/          # Capa de Datos
└── recursos/        # Recursos estáticos
```

**Funcionalidades por módulo:**
- **Vista**: Gestión de interfaces, eventos de usuario, validaciones de entrada
- **Lógica**: Reglas de negocio, validaciones, cálculos (IMC, reportes)
- **Modelo**: Definición de entidades, relaciones, persistencia
- **Recursos**: Iconos, imágenes, archivos estáticos

### 7. **¿Existen dependencias entre los servicios o microservicios?**

**Arquitectura monolítica:**
- La aplicación es un monolito de escritorio, no utiliza microservicios
- Las dependencias son internas entre capas:
  - Vista → Lógica
  - Lógica → Modelo
  - Modelo → Base de datos

**Dependencias externas:**
- SQLite para persistencia
- PyQt5 para interfaz gráfica
- No hay comunicación con servicios externos excepto YouTube (enlaces)

### 8. **¿Cómo se gestionan la seguridad y la autenticación dentro de la aplicación?**

**Estado actual de seguridad:**
- **No implementa autenticación**: Es una aplicación de escritorio sin usuarios
- **No hay autorización**: Acceso completo a todas las funcionalidades
- **Validación de datos**: Se implementan validaciones de entrada:
  - Formato de URLs de YouTube
  - Validación de fechas
  - Validación de números enteros
  - Longitud de strings

**Vulnerabilidades potenciales:**
- Base de datos SQLite sin cifrado
- No hay logs de auditoría
- Acceso directo a archivos del sistema

### 9. **¿Existen mecanismos de escalabilidad y balanceo de carga?**

**Limitaciones de escalabilidad:**
- **Aplicación monolítica de escritorio**: No soporta múltiples usuarios concurrentes
- **Base de datos SQLite**: Limitada para entornos multiusuario
- **Sin balanceadores de carga**: No aplicable para aplicaciones de escritorio

**Consideraciones futuras para escalabilidad:**
- Migración a arquitectura web
- Cambio a base de datos PostgreSQL/MySQL
- Implementación de APIs REST
- Containerización con Kubernetes

### 10. **¿Cómo se manejan los errores y la resiliencia del sistema?**

**Manejo de errores:**
- **Validaciones de entrada**: Mensajes de error descriptivos en español
- **Try-catch blocks**: Manejo de excepciones en conversiones de datos
- **Validaciones de negocio**: Verificación de reglas antes de persistir

**Ejemplos de validaciones:**
```python
try:
    calorias_int = int(calorias)
except ValueError:
    error = "Error, el campo calorias debe ser un número entero"
```

**Limitaciones en resiliencia:**
- No hay reintentos automáticos
- No hay logs estructurados
- Falta manejo de errores de base de datos

### 11. **¿Cómo se entienden las capas de la aplicación y cómo se manejan?**

**Arquitectura en capas:**

1. **Capa de Presentación (Vista)**:
   - **Responsabilidad**: Interfaz de usuario, captura de eventos
   - **Tecnología**: PyQt5
   - **Comunicación**: Solo hacia la capa de lógica

2. **Capa de Lógica de Negocio**:
   - **Responsabilidad**: Reglas de negocio, validaciones, cálculos
   - **Patrón**: Facade pattern con `FachadaEnForma`
   - **Implementaciones**: `LogicaEnForma` (real), `LogicaMock` (testing)

3. **Capa de Datos (Modelo)**:
   - **Responsabilidad**: Persistencia, modelos de datos
   - **Tecnología**: SQLAlchemy ORM + SQLite
   - **Patrones**: Active Record, Repository

**Flujo de datos:**
```
Usuario → Vista → Lógica → Modelo → Base de Datos
```

### 12. **¿Cómo me puedo comunicar con esta aplicación?: API? mecanismo de comunicación**

**Mecanismo de comunicación actual:**
- **Interfaz gráfica de escritorio**: PyQt5 como único punto de entrada
- **No expone APIs**: Es una aplicación standalone sin servicios web
- **Comunicación interna**: Llamadas a métodos directas entre capas

**Puntos de entrada principales:**

```python
# Aplicación principal
class App_EnForma(QApplication):
    def __init__(self, sys_argv, logica):
        self.logica = logica
        
# Métodos principales de la lógica
class LogicaEnForma(FachadaEnForma):
    # Gestión de personas
    def dar_personas(self) -> list
    def crear_persona(self, ...) -> bool
    def editar_persona(self, ...) -> bool
    def eliminar_persona(self, id_persona) -> bool
    
    # Gestión de ejercicios  
    def dar_ejercicios(self) -> list
    def crear_ejercicio(self, ...) -> bool
    def editar_ejercicio(self, ...) -> bool
    def eliminar_ejercicio(self, id_ejercicio) -> bool
    
    # Gestión de entrenamientos
    def dar_entrenamientos(self, id_persona) -> list
    def crear_entrenamiento(self, ...) -> bool
    def editar_entrenamiento(self, ...) -> bool
    def eliminar_entrenamiento(self, ...) -> bool
    
    # Reportes
    def dar_reporte(self, id_persona) -> dict
```

**Para convertir a API REST (propuesta futura):**

```python
# Endpoints propuestos para modernización
GET    /api/personas                    # Listar personas
POST   /api/personas                    # Crear persona
GET    /api/personas/{id}               # Obtener persona
PUT    /api/personas/{id}               # Actualizar persona
DELETE /api/personas/{id}               # Eliminar persona

GET    /api/ejercicios                  # Listar ejercicios
POST   /api/ejercicios                  # Crear ejercicio
GET    /api/ejercicios/{id}             # Obtener ejercicio
PUT    /api/ejercicios/{id}             # Actualizar ejercicio
DELETE /api/ejercicios/{id}             # Eliminar ejercicio

GET    /api/personas/{id}/entrenamientos    # Entrenamientos de persona
POST   /api/personas/{id}/entrenamientos    # Crear entrenamiento
PUT    /api/entrenamientos/{id}             # Actualizar entrenamiento
DELETE /api/entrenamientos/{id}             # Eliminar entrenamiento

GET    /api/personas/{id}/reporte           # Generar reporte
```

## Resumen Arquitectónico

La aplicación "EnForma" es una **aplicación monolítica de escritorio** basada en Python que implementa un **patrón MVC de 3 capas** para la gestión de entrenamientos físicos. Utiliza **PyQt5** para la interfaz, **SQLAlchemy** como ORM y **SQLite** para persistencia. La arquitectura es robusta para un entorno de usuario único, pero requeriría refactorización significativa para escalabilidad web y multiusuario.

**Puntos fuertes:**
- Separación clara de responsabilidades
- Patrón Facade bien implementado
- Cobertura de pruebas con CI/CD
- Validaciones de negocio sólidas

**Áreas de mejora:**
- Implementación de autenticación y seguridad
- Migración hacia arquitectura web/API
- Mejora en manejo de errores y logging
- Escalabilidad para múltiples usuarios
