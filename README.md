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

## Uso

### Método 1: Usando el lanzador (Recomendado)

```bash
python start.py
```

El lanzador detectará automáticamente tu sistema operativo, verificará e instalará las dependencias necesarias y abrirá el navegador.

### Método 2: Ejecución directa

```bash
python xonilab.py
```

---
### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonicli
cd xonicli
pip install -r requisitos.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonicli`).

---

### Acceso al sistema

1. Abre tu navegador y accede a: `http://localhost:5005`
2. Credenciales: **Usuario:** `XONILAB` | **Contraseña:** `laboratorio`

### Windows: Archivos de acceso rápido

Al ejecutar `start.py` en Windows, se generan automáticamente dos archivos:
- `XONILAB.bat` - Doble clic para ejecutar el sistema
- `XONILAB_ADMIN.bat` - Ejecutar como administrador (para instalar dependencias)

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

## Contacto y Créditos

- **Proyecto:** XONIDU
- **Creador:** Darian Alberto Camacho Salas
- **Versión:** 3.0
- **Año:** 2025
- **Somos XONIDU**
