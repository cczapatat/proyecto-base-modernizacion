1.
```
Actúa como un arquitecto de software experto y analiza la arquitectura de esta aplicación con base en su código.

Responde las siguientes preguntas de manera detallada y estructurada. Luego, guarda tu análisis dentro de un archivo architecture.md, manteniendo el formato Markdown.

Preguntas a analizar:

¿Cuáles son los componentes funcionales de la aplicación y cómo se relacionan entre sí?
¿Cómo es el despliegue de los componentes en el entorno productivo?
¿Cómo interactúan los componentes con las fuentes de datos?
¿Qué patrones y tácticas de arquitectura se están utilizando?
¿Qué tecnologías y frameworks forman parte de la arquitectura?
¿Cuáles son los principales módulos o capas en la aplicación?
¿Existen dependencias entre los servicios o microservicios?
¿Cómo se gestionan la seguridad y la autenticación dentro de la aplicación?
¿Existen mecanismos de escalabilidad y balanceo de carga?
¿Cómo se manejan los errores y la resiliencia del sistema?
¿Cómo se entienden las capas de la aplicación y cómo se manejan?
¿Cómo me puedo comunicar con esta aplicación?:API? mecanismo de comunicación. Si es un api generar el código para entender cuales son los endpoints
Instrucciones:

Escribe las respuestas en architecture.md.
Utiliza Markdown para estructurar la información con títulos (##), listas (-), y código (```) si es necesario.
Añade la sección "Respuestas" debajo de las preguntas.
Ejemplo de Formato Esperado en architecture.md:
```

2.
```
Genera **una estructura de carpetas** del proyecto, que muestre **todas las carpetas y archivos relevantes**. Sé extremadamente preciso.
**Instrucciones:** 
- Incluye **todas las carpetas principales**, como: `logica`, `modelo`, `recursos`, `vista`, etc.
- Dentro de cada carpeta, **lista todos los archivos .py, , etc.** que estén presentes.
- Para **cada archivo**, añade una breve descripción de su función al lado (comentario).
- **No te saltes ningún archivo.** Si hay 3 vistas, 2 modelos, etc., **todos deben aparecer**.
- Se coherente con una arquitectura basada en capas: vista, logica, modelos, etc.
- Guarda los resultados en el archivo diagrams.md
```

3.
```
Basándose en la estructura de carpetas del sistema y en el análisis de arquitectura previamente generado en `architecture.md`, actúa como un arquitecto de software experto y genera diagramas en formato Mermaid.js.
 **Diagramas requeridos:**
- **Diagrama de Componentes**: Muestra los módulos principales y cómo se comunican entre sí.
- **Diagrama de Despliegue**: Representa dónde están alojados los diferentes componentes de la aplicación.
- **Diagrama de Flujo de Datos**: Explica cómo los datos se mueven entre los diferentes módulos.
- **Diagrama de Clases**: Muestra la estructura de clases/archivos y sus relaciones.
- **Diagrama de Paquetes**: Organiza los paquetes y sus dependencias. Basado en la ## Estructura de Carpetas de la Aplicación Completa
- **Diagramas de Clases/Archivos por Carpeta**:
Crea un diagrama de clases por cada carpeta lógica:
- `Persona`: incluye las vistas, logica, modelos, , etc.
- `Ejercicio`: lo mismo que el dominio de persona.
- `EjercicioEntrenado`, etc.
Cada clase debe tener:
- Sus atributos (nombre, tipo)
- Sus métodos públicos
- Relaciones con otras clases (asociaciones, composiciones)
Genera estos diagramas en formato Mermaid.js y ponlos al final del archivo `diagrams.md`,  en Markdown.
```