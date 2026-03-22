# Random Auth Python Script

Este repositorio contiene un pequeño script de ejemplo `main.py` que construye una cabecera HTTP Basic a partir de un usuario y contraseña, consulta el endpoint de `httpbin.org` que valida autenticación básica y opcionalmente guarda la respuesta en un fichero.

Contenido relevante
- `main.py` — script principal que acepta parámetros por línea de comandos.
- `requirements.txt` — dependencias necesarias.

Requisitos
- Python 3.8+ (se probó con 3.10).
- Instalar dependencias:

```bash
python -m venv .venv   # opcional, recomendado
source .venv/bin/activate
pip install -r requirements.txt
```

Uso
- Ejecutar el script directamente:

```bash
python main.py [OPCIONES]
```

Opciones importantes
- `-u`, `--username` — usuario a usar (opcional).
- `-p`, `--password` — contraseña a usar (opcional).
- `-s`, `--save` — ruta de fichero donde guardar la respuesta (opcional).
- `-v`, `--verbose` — activar logging detallado (pon `True`).

Comportamiento
- Si no se proporcionan `-u` o `-p`, el script intenta obtener credenciales aleatorias desde una API externa y las usa para autenticarse contra `https://httpbin.org/basic-auth/{username}/{password}`.
- Si la petición a `httpbin.org` es exitosa, el JSON devuelto se imprime por pantalla y, si se pasó `-s`, se escribe en el fichero indicado.
- Es posible guadar el resultado en un archivo.
- Si no se incluyen credenciales, el script intentará obtenerlas de una API externa y usarlas para autenticarse contra `httpbin.org`.

