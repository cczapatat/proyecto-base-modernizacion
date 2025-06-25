# Estructura de Carpetas y Archivos - Proyecto EnForma

## Diagrama Completo de la Arquitectura del Proyecto

```
proyecto-base-modernizacion/
│
├── 📁 .git/                                    # Control de versiones Git
├── 📁 .github/                                 # Configuración GitHub Actions
│   └── 📁 workflows/                           # Flujos de trabajo CI/CD
│       ├── 📄 merge_on_develop.yml             # Pipeline para merge en develop
│       ├── 📄 merge_on_main.yml                # Pipeline para merge en main
│       └── 📄 push_feature_fix_branch.yml      # Pipeline para ramas feature/fix
│
├── 📁 src/                                     # Código fuente principal (Arquitectura en 3 capas)
│   │
│   ├── 📁 vista/                               # 🔴 CAPA DE PRESENTACIÓN (UI Layer)
│   │   ├── 📄 __init__.py                      # Inicializador del módulo vista
│   │   ├── 📄 InterfazEnForma.py              # Controlador principal de la aplicación (MVC)
│   │   ├── 📄 VistaListaPersonas.py           # Ventana principal - Lista y gestión de personas
│   │   ├── 📄 VistaPersona.py                 # Ventana para crear/editar una persona individual
│   │   ├── 📄 VistaListaEjercicios.py         # Ventana para gestionar catálogo de ejercicios
│   │   ├── 📄 VistaCrearEjercicio.py          # Diálogo modal para crear/editar ejercicios
│   │   ├── 📄 VistaListaEntrenamientos.py     # Ventana para mostrar entrenamientos de una persona
│   │   ├── 📄 VistaCrearEntrenamiento.py      # Diálogo modal para registrar entrenamientos
│   │   ├── 📄 VistaDejarDeEntrenarPersona.py  # Ventana para dar de baja a personas
│   │   └── 📄 VistaReporte.py                 # Ventana para mostrar reportes de progreso
│   │
│   ├── 📁 logica/                              # 🟡 CAPA DE LÓGICA DE NEGOCIO (Business Layer)
│   │   ├── 📄 __init__.py                      # Inicializador del módulo lógica
│   │   ├── 📄 FachadaEnForma.py               # Interfaz abstracta - Patrón Facade (Contrato)
│   │   ├── 📄 LogicaEnForma.py                # Implementación real de reglas de negocio
│   │   └── 📄 LogicaMock.py                   # Implementación mock para testing y desarrollo
│   │
│   ├── 📁 modelo/                              # 🟢 CAPA DE DATOS (Data Access Layer)
│   │   ├── 📄 declarative_base.py             # Configuración SQLAlchemy - Engine y Session
│   │   ├── 📄 persona.py                      # Modelo de datos ORM - Entidad Persona
│   │   ├── 📄 ejercicio.py                    # Modelo de datos ORM - Entidad Ejercicio
│   │   └── 📄 ejercicioEntrenado.py           # Modelo de datos ORM - Entidad EjercicioEntrenado (relación)
│   │
│   └── 📁 recursos/                            # 🎨 RECURSOS ESTÁTICOS (Assets)
│       ├── 📄 Attributions.txt                # Créditos y atribuciones de iconos
│       ├── 🖼️ EnFormaLogo.png                  # Logo principal de la aplicación
│       ├── 🖼️ 002-door-open-fill-icon.png     # Icono para salir/cerrar sesión
│       ├── 🖼️ 004-edit-button.png             # Icono para editar registros
│       ├── 🖼️ 005-delete.png                  # Icono para eliminar registros
│       ├── 🖼️ 006-add.png                     # Icono para agregar nuevos registros
│       ├── 🖼️ 007-back-button.png             # Icono para volver/regresar
│       ├── 🖼️ 010-ejercicio.png               # Icono para ejercicios
│       ├── 🖼️ floppy-disk.png                 # Icono para guardar datos
│       └── 🖼️ reporte.png                     # Icono para generar reportes
│
├── 📁 tests/                                   # 🧪 MÓDULO DE PRUEBAS (Testing Layer)
│   ├── 📄 __init__.py                          # Inicializador del módulo tests
│   ├── 📄 test_logica_enforma.py              # Pruebas unitarias para LogicaEnForma (791 líneas)
│   ├── 📄 test_logica_mock.py                 # Pruebas unitarias para LogicaMock
│   └── 📄 test_ci_rebase.py                   # Pruebas básicas para CI/CD pipeline
│
├── 📄 __main__.py                              # 🚀 PUNTO DE ENTRADA PRINCIPAL de la aplicación
├── 📄 requirements.txt                         # 📦 Dependencias del proyecto (PyQt5, SQLAlchemy, etc.)
├── 📄 identifier.sqlite                        # 🗄️ Base de datos SQLite (persistencia local)
├── 📄 README.md                               # 📖 Documentación del proyecto
├── 📄 architecture.md                         # 🏗️ Análisis arquitectónico del sistema
├── 📄 Jenkinsfile                             # ⚙️ Pipeline de CI/CD para Jenkins
├── 📄 .gitignore                              # 🚫 Archivos ignorados por Git
├── 📄 .gitattributes                          # ⚙️ Configuración de atributos Git
└── 📄 .coveragerc                             # 📊 Configuración para cobertura de código
```

## Descripción Detallada por Capas

### 🔴 **Capa de Presentación (Vista)** - 10 archivos
**Responsabilidad**: Interfaz gráfica de usuario, manejo de eventos, validaciones de entrada

| Archivo | Líneas | Función Principal |
|---------|--------|-------------------|
| `InterfazEnForma.py` | 179 | **Controlador principal** - Coordina todas las ventanas y maneja la comunicación con la lógica |
| `VistaListaPersonas.py` | 210 | **Ventana principal** - Muestra tabla de personas registradas con opciones CRUD |
| `VistaPersona.py` | 173 | **Formulario de persona** - Crear/editar datos personales y medidas corporales |
| `VistaListaEjercicios.py` | 186 | **Gestión de ejercicios** - Catálogo de ejercicios disponibles con enlaces YouTube |
| `VistaCrearEjercicio.py` | 107 | **Diálogo de ejercicio** - Modal para crear/editar ejercicios individuales |
| `VistaListaEntrenamientos.py` | 238 | **Historial de entrenamientos** - Muestra entrenamientos de una persona específica |
| `VistaCrearEntrenamiento.py` | 114 | **Registro de entrenamiento** - Modal para agregar nuevas sesiones de ejercicio |
| `VistaDejarDeEntrenarPersona.py` | 120 | **Baja de persona** - Formulario para dar de baja personas con fecha y motivo |
| `VistaReporte.py` | 194 | **Reportes de progreso** - Muestra estadísticas, IMC y gráficos de rendimiento |
| `__init__.py` | - | **Inicializador** - Configura el módulo de vista como paquete Python |

### 🟡 **Capa de Lógica de Negocio** - 4 archivos
**Responsabilidad**: Reglas de negocio, validaciones, cálculos, patrón Facade

| Archivo | Líneas | Función Principal |
|---------|--------|-------------------|
| `FachadaEnForma.py` | 210 | **Interfaz abstracta** - Define contratos y métodos que deben implementar las clases de lógica |
| `LogicaEnForma.py` | 332 | **Implementación real** - Lógica de negocio completa, validaciones, cálculos IMC, acceso a BD |
| `LogicaMock.py` | 118 | **Implementación mock** - Datos falsos para desarrollo y testing sin base de datos |
| `__init__.py` | - | **Inicializador** - Configura el módulo de lógica como paquete Python |

### 🟢 **Capa de Datos (Modelo)** - 4 archivos
**Responsabilidad**: Persistencia, modelos ORM, relaciones entre entidades

| Archivo | Líneas | Función Principal |
|---------|--------|-------------------|
| `declarative_base.py` | 10 | **Configuración ORM** - Engine SQLAlchemy, Session factory, Base declarativa |
| `persona.py` | 20 | **Entidad Persona** - Modelo ORM con datos personales, medidas, fechas de entrenamiento |
| `ejercicio.py` | 12 | **Entidad Ejercicio** - Modelo ORM para catálogo de ejercicios con enlaces YouTube |
| `ejercicioEntrenado.py` | 13 | **Entidad Relacional** - Modelo ORM que relaciona persona-ejercicio con métricas |

### 🎨 **Recursos Estáticos** - 10 archivos
**Responsabilidad**: Assets visuales, iconografía, documentación de créditos

| Archivo | Tipo | Función |
|---------|------|---------|
| `EnFormaLogo.png` | Imagen | Logo principal de la aplicación |
| `002-door-open-fill-icon.png` | Icono | Salir/cerrar aplicación |
| `004-edit-button.png` | Icono | Editar registros |
| `005-delete.png` | Icono | Eliminar registros |
| `006-add.png` | Icono | Agregar nuevos registros |
| `007-back-button.png` | Icono | Volver/regresar |
| `010-ejercicio.png` | Icono | Representar ejercicios |
| `floppy-disk.png` | Icono | Guardar datos |
| `reporte.png` | Icono | Generar reportes |
| `Attributions.txt` | Texto | Créditos de iconos de Flaticon |

### 🧪 **Módulo de Pruebas** - 4 archivos
**Responsabilidad**: Testing unitario, integración, CI/CD validation

| Archivo | Líneas | Función Principal |
|---------|--------|-------------------|
| `test_logica_enforma.py` | 791 | **Pruebas completas** - Test exhaustivos de toda la lógica real con SQLAlchemy |
| `test_logica_mock.py` | 17 | **Pruebas mock** - Validación de implementación mock y datos de prueba |
| `test_ci_rebase.py` | 17 | **Pruebas CI/CD** - Tests básicos para validar pipeline de integración |
| `__init__.py` | - | **Inicializador** - Configura el módulo de tests como paquete Python |

### 📄 **Archivos de Configuración y Raíz**

| Archivo | Tipo | Función Principal |
|---------|------|-------------------|
| `__main__.py` | Python | **Punto de entrada** - Inicializa la aplicación, configura BD, inyecta dependencias |
| `requirements.txt` | Config | **Dependencias** - PyQt5, SQLAlchemy, coverage, faker, validators |
| `identifier.sqlite` | Database | **Base de datos** - SQLite con datos persistentes de personas, ejercicios, entrenamientos |
| `Jenkinsfile` | Pipeline | **CI/CD** - Pipeline con checkout, tests, cobertura, análisis de código |
| `.coveragerc` | Config | **Cobertura** - Configuración para medir cobertura de código en tests |
| `.gitignore` | Config | **Git ignore** - Archivos excluidos del control de versiones |
| `.gitattributes` | Config | **Git attributes** - Configuración de normalización de archivos |

## Diagramas de Arquitectura en Mermaid.js

### 1. Diagrama de Componentes

```mermaid
graph TD
    subgraph "🔴 Capa de Presentación"
        UI[InterfazEnForma<br/>Controlador Principal]
        VP[VistaListaPersonas<br/>Gestión Personas]
        VE[VistaListaEjercicios<br/>Gestión Ejercicios]
        VT[VistaListaEntrenamientos<br/>Gestión Entrenamientos]
        VR[VistaReporte<br/>Reportes]
        VCP[VistaPersona<br/>CRUD Persona]
        VCE[VistaCrearEjercicio<br/>CRUD Ejercicio]
        VCT[VistaCrearEntrenamiento<br/>CRUD Entrenamiento]
        VD[VistaDejarDeEntrenar<br/>Baja Persona]
    end

    subgraph "🟡 Capa de Lógica de Negocio"
        F[FachadaEnForma<br/>Interface]
        L[LogicaEnForma<br/>Implementación Real]
        M[LogicaMock<br/>Implementación Mock]
    end

    subgraph "🟢 Capa de Datos"
        DB[declarative_base<br/>Configuración SQLAlchemy]
        P[Persona<br/>Entidad ORM]
        E[Ejercicio<br/>Entidad ORM]
        ET[EjercicioEntrenado<br/>Entidad Relacional]
        SQLITE[(identifier.sqlite<br/>Base de Datos)]
    end

    subgraph "🎨 Recursos"
        R[Iconos PNG<br/>Assets Visuales]
    end

    UI --> F
    VP --> UI
    VE --> UI
    VT --> UI
    VR --> UI
    VCP --> UI
    VCE --> UI
    VCT --> UI
    VD --> UI

    F --> L
    F --> M
    
    L --> DB
    L --> P
    L --> E
    L --> ET
    
    P --> SQLITE
    E --> SQLITE
    ET --> SQLITE
    
    UI -.-> R
```

### 2. Diagrama de Despliegue

```mermaid
graph TD
    subgraph "💻 Entorno de Desarrollo"
        DEV[Desarrollador<br/>Estación de Trabajo]
        GIT[GitHub Repository<br/>MISW4101-202314-Grupo028]
    end

    subgraph "🔧 Entorno de CI/CD"
        JENKINS[Jenkins Server<br/>157.253.238.75:8080]
        DOCKER[Docker Container<br/>Python 3.7.6]
        GA[GitHub Actions<br/>Workflows]
    end

    subgraph "🖥️ Entorno de Ejecución"
        DESKTOP[Aplicación de Escritorio<br/>PyQt5]
        SQLITE_LOCAL[SQLite Local<br/>identifier.sqlite]
        PYTHON_ENV[Python Runtime<br/>3.7.6]
    end

    subgraph "📊 Análisis y Reportes"
        CODE_ANALYZER[Code Analyzer<br/>GitInspector]
        COVERAGE[Coverage Reports<br/>HTML Output]
    end

    DEV --> GIT
    GIT --> JENKINS
    GIT --> GA
    
    JENKINS --> DOCKER
    JENKINS --> CODE_ANALYZER
    JENKINS --> COVERAGE
    
    DOCKER --> DESKTOP
    DESKTOP --> SQLITE_LOCAL
    DESKTOP --> PYTHON_ENV
```

### 3. Diagrama de Flujo de Datos

```mermaid
flowchart TD
    USER[👤 Usuario]
    subgraph "Capa Vista"
        MAIN[Ventana Principal<br/>Lista Personas]
        FORMS[Formularios<br/>Crear/Editar]
        REPORTS[Reportes<br/>Visualización]
    end
    subgraph "Lógica"
        CONTROLLER[Controlador<br/>InterfazEnForma]
        VALIDATOR[Validaciones<br/>Reglas de Negocio<br>Calculos]
        SESSIONS[Sesiones ORM]
    end
    subgraph "Modelos"
        ORM[SQLAlchemy<br>Modelos ORM]
        DATABASE[(SQLite<br/>identifier.sqlite)]
    end
    USER --> MAIN
    USER --> FORMS
    USER --> REPORTS
    MAIN --> CONTROLLER
    FORMS --> CONTROLLER
    REPORTS --> CONTROLLER
    CONTROLLER --> VALIDATOR
    VALIDATOR --> SESSIONS
    SESSIONS --> ORM
    ORM <--> DATABASE
    DATABASE --> ORM
    ORM --> SESSIONS
    SESSIONS --> VALIDATOR
    VALIDATOR --> CONTROLLER
    CONTROLLER --> REPORTS
```

### 4. Diagrama de Clases Principal

```mermaid
classDiagram
    class FachadaEnForma {
        <<interface>>
        +dar_personas() list
        +dar_persona(id) dict
        +crear_persona(...) bool
        +editar_persona(...) bool
        +eliminar_persona(id) bool
        +dar_ejercicios() list
        +crear_ejercicio(...) bool
        +editar_ejercicio(...) bool
        +eliminar_ejercicio(id) bool
        +dar_entrenamientos(id_persona) list
        +crear_entrenamiento(...) bool
        +editar_entrenamiento(...) bool
        +eliminar_entrenamiento(id, persona) bool
        +dar_reporte(id_persona) dict
        +validar_crear_editar_persona(...) string
        +validar_crear_editar_ejercicio(...) string
        +validar_crear_editar_entrenamiento(...) string
        +dejar_de_entrenar_persona(id, fecha, razon) bool
    }

    class LogicaEnForma {
        +__init__()
        +es_enlace_youtube(enlace) bool
        +calcular_imc(peso, talla) float
        +calcular_clasificacion_imc(imc) string
        +tiempo_tiene_formato_valido(tiempo) bool
        +fecha_menor_igual_dia_actual(fecha) bool
        +mapear_none_a_vacio(valor) string
        +es_diccionario_vacio(dict) bool
        +obtener_fecha_de_string(str_fecha, formato) datetime
    }

    class LogicaMock {
        -personas list
        -ejercicios list
        -entrenamientos list
        -reportes list
        +__init__()
    }

    class App_EnForma {
        -logica FachadaEnForma
        -persona_actual int
        +__init__(sys_argv, logica)
        +mostrar_vista_lista_personas()
        +crear_persona()
        +mostrar_persona(id_persona)
        +guardar_persona(...) string
        +eliminar_persona(indice)
        +mostrar_ejercicios()
        +crear_ejercicio(...) string
        +editar_ejercicio(...) 
        +eliminar_ejercicio(indice)
        +mostrar_entrenamientos(id_persona)
        +crear_entrenamiento(...) string
        +editar_entrenamiento(...)
        +eliminar_entrenamiento(id, id_persona)
        +mostrar_reporte(id_persona)
    }

    class Persona {
        +id Integer PK
        +nombre String
        +apellido String
        +fecha_inicio String
        +fecha_retiro String
        +razon_retiro String
        +talla REAL
        +peso REAL
        +edad Integer
        +brazo Integer
        +pierna Integer
        +pecho Integer
        +cintura Integer
    }

    class Ejercicio {
        +id Integer PK
        +nombre String
        +descripcion String
        +calorias Integer
        +youtube String
    }

    class EjercicioEntrenado {
        +id Integer PK
        +persona_id Integer FK
        +ejercicio_id Integer FK
        +fecha String
        +repeticiones Integer
        +tiempo String
    }

    FachadaEnForma <|-- LogicaEnForma
    FachadaEnForma <|-- LogicaMock
    App_EnForma --> FachadaEnForma
    LogicaEnForma --> Persona
    LogicaEnForma --> Ejercicio
    LogicaEnForma --> EjercicioEntrenado
    EjercicioEntrenado --> Persona
    EjercicioEntrenado --> Ejercicio
```

### 5. Diagrama de Paquetes

```mermaid
graph TD
    subgraph "proyecto-base-modernizacion"
        subgraph "src"
            VISTA[📁 vista<br/>10 archivos Python<br/>Interfaces PyQt5]
            LOGICA[📁 logica<br/>4 archivos Python<br/>Reglas de Negocio]
            MODELO[📁 modelo<br/>4 archivos Python<br/>Entidades ORM]
            RECURSOS[📁 recursos<br/>10 archivos<br/>Assets Visuales]
        end
        
        subgraph "tests"
            TEST_LOGICA[test_logica_enforma.py<br/>791 líneas]
            TEST_MOCK[test_logica_mock.py<br/>17 líneas]
            TEST_CI[test_ci_rebase.py<br/>17 líneas]
        end
        
        subgraph "config"
            REQUIREMENTS[requirements.txt<br/>Dependencias]
            JENKINS[Jenkinsfile<br/>CI/CD Pipeline]
            COVERAGE[.coveragerc<br/>Cobertura]
            GIT_CONFIG[.gitignore<br/>.gitattributes]
        end
        
        subgraph "data"
            DATABASE[identifier.sqlite<br/>Base de Datos]
        end
        
        MAIN[__main__.py<br/>Punto de Entrada]
    end

    VISTA --> LOGICA
    LOGICA --> MODELO
    MODELO --> DATABASE
    VISTA -.-> RECURSOS
    
    TEST_LOGICA --> LOGICA
    TEST_MOCK --> LOGICA
    
    MAIN --> VISTA
    MAIN --> LOGICA
    MAIN --> MODELO
    
    REQUIREMENTS -.-> MAIN
    JENKINS -.-> TEST_LOGICA
    JENKINS -.-> TEST_MOCK
    JENKINS -.-> TEST_CI
```

### 6. Diagrama de Clases por Dominio - Persona

```mermaid
classDiagram
    class VistaListaPersonas {
        -interfaz App_EnForma
        -title string
        -width int
        -height int
        +__init__(interfaz)
        +mostrar_personas(lista_personas)
        +crear_persona_click()
        +mostrar_persona_click(indice)
        +eliminar_persona_click(indice)
        +mostrar_entrenamientos_click(indice)
        +mostrar_reporte_click(indice)
        +dejar_de_entrenar_click(indice)
    }

    class VistaPersona {
        -interfaz App_EnForma
        -titulo string
        -width int
        -height int
        -persona_actual dict
        +__init__(interfaz)
        +mostrar_persona(persona)
        +guardar_persona_click()
        +validar_campos() bool
        +limpiar_campos()
        +cancelar_click()
    }

    class VistaDejarDeEntrenarPersona {
        -interfaz App_EnForma
        -titulo string
        -persona_actual dict
        +__init__(principal)
        +mostrar_dejar_de_entrenar(persona)
        +guardar_retiro_click()
        +cancelar_click()
        +validar_fecha() bool
        +validar_razon() bool
    }

    class PersonaLogica {
        +dar_personas() list
        +dar_persona(id_persona) dict
        +validar_crear_editar_persona(...) string
        +crear_persona(...) bool
        +editar_persona(...) bool
        +eliminar_persona(id_persona) bool
        +dejar_de_entrenar_persona(id, fecha, razon) bool
        -validar_campos_persona(...) string
        -calcular_imc(peso, talla) float
        -calcular_clasificacion_imc(imc) string
    }

    class PersonaModelo {
        +id Integer PK
        +nombre String
        +apellido String
        +fecha_inicio String
        +fecha_retiro String
        +razon_retiro String
        +talla REAL
        +peso REAL
        +edad Integer
        +brazo Integer
        +pierna Integer
        +pecho Integer
        +cintura Integer
        +__init__(...)
        +__repr__() string
    }

    VistaListaPersonas --> PersonaLogica
    VistaPersona --> PersonaLogica
    VistaDejarDeEntrenarPersona --> PersonaLogica
    PersonaLogica --> PersonaModelo
```

### 7. Diagrama de Clases por Dominio - Ejercicio

```mermaid
classDiagram
    class VistaListaEjercicios {
        -interfaz App_EnForma
        -titulo string
        -ejercicios list
        +__init__(interfaz)
        +mostrar_ejercicios(lista_ejercicios)
        +crear_ejercicio_click()
        +editar_ejercicio_click(indice)
        +eliminar_ejercicio_click(indice)
        +terminar_click()
        +error(mensaje)
    }

    class VistaCrearEjercicio {
        -interfaz App_EnForma
        -ejercicio_actual dict
        -resultado string
        +__init__(ejercicio, interfaz)
        +mostrar_dialogo()
        +aceptar_click()
        +cancelar_click()
        +validar_campos() bool
        +limpiar_campos()
    }

    class EjercicioLogica {
        +dar_ejercicios() list
        +validar_crear_editar_ejercicio(...) string
        +crear_ejercicio(...) bool
        +editar_ejercicio(...) bool
        +eliminar_ejercicio(id_ejercicio) bool
        +dar_ejercicios_por_nombre(nombre, id) list
        +dar_ejercicio_por_nombre(nombre) Ejercicio
        -es_enlace_youtube(enlace) bool
        -validar_campos_ejercicio(...) string
    }

    class EjercicioModelo {
        +id Integer PK
        +nombre String
        +descripcion String
        +calorias Integer
        +youtube String
        +__init__(...)
        +__repr__() string
    }

    VistaListaEjercicios --> EjercicioLogica
    VistaCrearEjercicio --> EjercicioLogica
    EjercicioLogica --> EjercicioModelo
```

### 8. Diagrama de Clases por Dominio - Entrenamiento

```mermaid
classDiagram
    class VistaListaEntrenamientos {
        -interfaz App_EnForma
        -persona dict
        -ejercicios list
        -titulo string
        +__init__(interfaz, persona, ejercicios)
        +mostrar_entrenamientos(id_persona, lista)
        +crear_entrenamiento_click()
        +editar_entrenamiento_click(indice)
        +eliminar_entrenamiento_click(indice)
        +terminar_click()
        +error(mensaje)
    }

    class VistaCrearEntrenamiento {
        -interfaz App_EnForma
        -ejercicios list
        -entrenamiento_actual dict
        +__init__(entrenamiento, interfaz, ejercicios)
        +mostrar_dialogo()
        +aceptar_click()
        +cancelar_click()
        +validar_campos() bool
        +cargar_ejercicios()
    }

    class VistaReporte {
        -interfaz App_EnForma
        -persona dict
        -titulo string
        +__init__(interfaz, persona)
        +mostrar_datos(id_persona, datos_reporte)
        +mostrar_estadisticas(estadisticas)
        +mostrar_tabla_entrenamientos(entrenamientos)
        +terminar_click()
        +generar_reporte_click()
    }

    class EntrenamientoLogica {
        +dar_entrenamientos(id_persona) list
        +validar_crear_editar_entrenamiento(...) string
        +crear_entrenamiento(...) bool
        +editar_entrenamiento(...) bool
        +eliminar_entrenamiento(id, persona) bool
        +dar_reporte(id_persona) dict
        +dar_historial_ejercicios_entrenados_por_persona_id(id) list
        -tiempo_tiene_formato_valido(tiempo) bool
        -fecha_menor_igual_dia_actual(fecha) bool
        -mapear_objeto_entrenamiento(ejercicioEntrenado) dict
    }

    class EjercicioEntrenadoModelo {
        +id Integer PK
        +persona_id Integer FK
        +ejercicio_id Integer FK
        +fecha String
        +repeticiones Integer
        +tiempo String
        +__init__(...)
        +__repr__() string
    }

    VistaListaEntrenamientos --> EntrenamientoLogica
    VistaCrearEntrenamiento --> EntrenamientoLogica
    VistaReporte --> EntrenamientoLogica
    EntrenamientoLogica --> EjercicioEntrenadoModelo
    EjercicioEntrenadoModelo --> PersonaModelo
    EjercicioEntrenadoModelo --> EjercicioModelo
```

### 9. Diagrama de Secuencia - Crear Persona

```mermaid
sequenceDiagram
    participant U as Usuario
    participant VLP as VistaListaPersonas
    participant VP as VistaPersona
    participant IE as InterfazEnForma
    participant L as LogicaEnForma
    participant P as PersonaModelo
    participant DB as SQLite

    U->>VLP: Click "Crear Persona"
    VLP->>IE: crear_persona()
    IE->>VP: mostrar_persona(None)
    VP->>U: Mostrar formulario vacío
    
    U->>VP: Llenar datos + Click "Guardar"
    VP->>IE: guardar_persona(datos...)
    IE->>L: validar_crear_editar_persona(datos...)
    
    alt Validación exitosa
        L->>IE: "" (sin errores)
        IE->>L: crear_persona(datos...)
        L->>P: Persona(datos...)
        P->>DB: INSERT INTO personas
        DB->>P: OK
        P->>L: True
        L->>IE: True
        IE->>VLP: mostrar_personas(lista_actualizada)
        VLP->>U: Actualizar tabla
    else Validación fallida
        L->>IE: "Error: mensaje"
        IE->>VP: return error
        VP->>U: Mostrar mensaje error
    end
```

### 10. Diagrama de Estados - Gestión de Persona

```mermaid
stateDiagram-v2
    [*] --> ListaPersonas: Inicio Aplicación
    
    ListaPersonas --> CrearPersona: Click "Crear"
    ListaPersonas --> EditarPersona: Click "Editar"
    ListaPersonas --> ConfirmarEliminar: Click "Eliminar"
    ListaPersonas --> VerEntrenamientos: Click "Entrenamientos"
    ListaPersonas --> VerReporte: Click "Reporte"
    ListaPersonas --> DejarEntrenar: Click "Dejar de Entrenar"
    
    CrearPersona --> ValidandoPersona: Click "Guardar"
    EditarPersona --> ValidandoPersona: Click "Guardar"
    
    ValidandoPersona --> ListaPersonas: Validación OK
    ValidandoPersona --> CrearPersona: Error en crear
    ValidandoPersona --> EditarPersona: Error en editar
    
    ConfirmarEliminar --> ListaPersonas: Confirmar/Cancelar
    
    VerEntrenamientos --> ListaPersonas: Click "Volver"
    VerReporte --> ListaPersonas: Click "Volver"
    DejarEntrenar --> ListaPersonas: Guardar/Cancelar
    
    CrearPersona --> ListaPersonas: Click "Cancelar"
    EditarPersona --> ListaPersonas: Click "Cancelar"
```
