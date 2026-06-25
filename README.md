# XONILAB - Sistema de Gestión de Laboratorio

**Advertencia:** Sistema para fines educativos y gestión interna de laboratorios. No debe usarse para actividades malintencionadas ni para acceder a sistemas no autorizados. El autor no se hace responsable del uso indebido.

## ¿Qué es XONILAB?

XONILAB es un sistema web desarrollado en Python con Flask para la gestión integral de laboratorios educativos. Permite administrar inventario, préstamos, alumnos, deudas y reservas sin necesidad de base de datos, almacenando toda la información en archivos CSV.

El sistema incluye generación de códigos QR, calendario de reservas y sistema de copias de seguridad automáticas.

## Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xonilab.git
cd xonilab
```

## Requisitos

- Python 3.8+ instalado
- Dependencias Python listadas en `requisitos.txt`
- Navegador web moderno

## Métodos de Instalación y Ejecución

### Método 1: Usando el lanzador universal (Recomendado)

```bash
python start.py
```

El lanzador detectará automáticamente tu sistema operativo, verificará e instalará las dependencias necesarias y abrirá el navegador.

### Método 2: Ejecución directa

```bash
python xonilab.py
```

### Método 3: Windows - Usando el archivo .bat (Recomendado para Windows)

Ejecuta directamente el archivo incluido en el proyecto:

```bash
INICIAR_XONILAB.bat
```

Este archivo:
- Solicita permisos de administrador automáticamente
- Verifica que Python esté instalado
- Instala las dependencias necesarias
- Inicia el servidor y abre el navegador

### Método 4: Windows - Doble clic en el ejecutable generado

Al ejecutar `start.py` en Windows, se generan automáticamente:
- `XONILAB.bat` - Doble clic para ejecutar el sistema
- `XONILAB_ADMIN.bat` - Ejecutar como administrador (para instalar dependencias)

### Método 5: Linux - Script de inicio

Crea un script de inicio personalizado:

```bash
#!/bin/bash
cd /ruta/a/xonilab
python3 start.py
```

Guarda como `xonilab.sh` y hazlo ejecutable:
```bash
chmod +x xonilab.sh
./xonilab.sh
```

### Método 6: macOS - Script de inicio

Crea un script de inicio personalizado:

```bash
#!/bin/bash
cd /ruta/a/xonilab
python3 start.py
```

Guarda como `xonilab.command` y hazlo ejecutable:
```bash
chmod +x xonilab.command
```

### Método 7: Usando el comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonilab
cd xonilab
pip install -r requisitos.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonicli`).

### Método 8: Crear acceso directo en el escritorio (Windows)

1. Haz clic derecho en el escritorio
2. Selecciona "Nuevo" → "Acceso directo"
3. En la ubicación, escribe: `cmd /k "cd C:\ruta\xonilab && INICIAR_XONILAB.bat"`
4. Asigna un nombre: "XONILAB"
5. Haz clic en "Finalizar"

### Método 9: Variable de entorno (Windows)

Agrega la carpeta de XONILAB al PATH y ejecuta desde cualquier lugar:

```batch
setx PATH "%PATH%;C:\ruta\xonilab"
```

Luego puedes ejecutar desde cualquier terminal:
```bash
start.py
```

### Método 10: Usando Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5005
CMD ["python", "xonilab.py"]
```

Construye y ejecuta:
```bash
docker build -t xonilab .
docker run -p 5005:5005 xonilab
```

---

### Acceso al sistema

1. Abre tu navegador y accede a: `http://localhost:5005`
2. Credenciales: **Usuario:** `XONILAB` | **Contraseña:** `laboratorio`

## Funcionalidades

- **Inventario** - Gestión de materiales con códigos QR
- **Préstamos** - Registro y control de préstamos a alumnos
- **Alumnos** - Registro y seguimiento de alumnos
- **Deudas** - Control de deudas por daños o pérdidas
- **Reservas** - Calendario interactivo de reservas
- **Reportes** - Generación de reportes del sistema
- **Backups** - Copias de seguridad automáticas

## Estructura de Archivos

```
xonilab/
├── start.py                 # Lanzador universal
├── xonilab.py               # Programa principal
├── requisitos.txt           # Dependencias Python
├── README.md                # Este archivo
├── INICIAR_XONILAB.bat      # Script de inicio para Windows
├── data/                    # Archivos CSV con datos
├── templates/               # Vistas HTML
├── static/qrcodes/          # Códigos QR generados
└── backups/                 # Copias de seguridad
```

## Configuración

Por defecto, el sistema:
- Puerto: `5005`
- Host: `localhost`
- Usuario: `XONILAB`
- Contraseña: `laboratorio`

Para cambiar la configuración, modifica las variables en `xonilab.py`.

## Problemas comunes

**"No puedo acceder desde otro dispositivo"** - Cambia `HOST` a `'0.0.0.0'` en `xonilab.py`

**"No se generan los códigos QR"** - Verifica que pillow esté instalado y los permisos de `static/qrcodes/`

**"Error al leer archivos CSV"** - Verifica permisos de lectura en la carpeta `data/`

**"El archivo .bat no se ejecuta"** - Ejecuta como administrador o verifica que Python esté en el PATH

## Contacto y Créditos

- **Proyecto:** XONIDU
- **Creador:** Darian Alberto Camacho Salas
- **Versión:** 3.0
- **Año:** 2026
- **Somos XONIDU**