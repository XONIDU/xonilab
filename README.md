# 📊 XONILAB - Sistema de Gestión de Laboratorio

**Advertencia:** Sistema para fines educativos y gestión interna de laboratorios. No debe usarse con fines malintencionados ni para acceder a sistemas no autorizados. El autor no se hace responsable del uso indebido.

## 🎯 ¿Qué es XONILAB?

XONILAB es un sistema web desarrollado en Python con Flask para la gestión integral de laboratorios educativos. Permite administrar inventario, préstamos, alumnos, deudas y reservas sin necesidad de base de datos, almacenando toda la información en archivos CSV.

El sistema incluye generación de códigos QR, calendario de reservas y sistema de copias de seguridad automáticas.

## 📥 Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xonilab.git
cd xonilab
```

## ✅ Requisitos

- Python 3.8+ instalado
- Dependencias Python listadas en `requisitos.txt`
- Navegador web moderno

### Dependencias del sistema por plataforma:

#### 🐧 Arch Linux

```bash
sudo pacman -S python python-pip
sudo pacman -S python-pillow
pip install -r requisitos.txt --break-system-packages
```

#### 🐧 Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip -y
sudo apt install python3-pil -y
pip3 install -r requisitos.txt --break-system-packages
```

#### 🪟 Windows

1. Instala Python 3 desde [python.org](https://python.org)
2. Abre Command Prompt o PowerShell como administrador
3. Ejecuta:

```bash
pip install -r requisitos.txt
```

#### 🍎 macOS

```bash
brew install python
pip3 install -r requisitos.txt
```

## 🚀 Uso

1. Navega hasta la carpeta del proyecto:

```bash
cd xonilab
```

2. Ejecuta el script principal:

```bash
python start.py
```

3. Abre tu navegador y accede a:

```
http://localhost:5005
```

4. Credenciales de acceso:
- **Usuario:** `XONILAB`
- **Contraseña:** `laboratorio`

## ✨ Funcionalidades

### 📦 Inventario
- Gestión completa de materiales de laboratorio
- Generación automática de códigos QR para cada item
- Búsqueda y filtrado de materiales
- Control de cantidades disponibles

### 📋 Préstamos
- Registro de préstamos a alumnos
- Control de fechas de devolución
- Historial de préstamos por alumno
- Estado actual de cada préstamo

### 👥 Alumnos
- Registro de alumnos
- Historial de préstamos por alumno
- Control de deudas pendientes

### 💰 Deudas
- Registro de deudas por daños o pérdidas
- Estado de pago de cada deuda
- Historial financiero por alumno

### 📅 Reservas
- Calendario interactivo de reservas
- Reserva de materiales por fecha y hora
- Evita reservas duplicadas

### 📊 Reportes
- Reportes de inventario
- Reportes de préstamos activos
- Reportes de deudas pendientes
- Reportes de reservas

### 💾 Backups
- Sistema automático de copias de seguridad
- Restauración desde backups
- Almacenamiento en carpeta `backups/`

## 🔧 Estructura de Archivos

```
xonilab/
├── start.py                 # Programa principal
├── requisitos.txt           # Dependencias Python
├── README.md                # Este archivo
├── xonilab_manual.pdf       # Manual de usuario
├── data/                    # Archivos CSV con datos
│   ├── alumnos.csv
│   ├── deudas.csv
│   ├── inventario.csv
│   ├── prestamos.csv
│   └── reservas.csv
├── templates/               # Vistas HTML
│   ├── index.html
│   ├── inventario.html
│   ├── prestamos.html
│   └── ...
├── static/                  # Archivos estáticos
│   └── qrcodes/             # Códigos QR generados
└── backups/                 # Copias de seguridad
```

## ⚙️ Configuración

Por defecto, el sistema:
- Puerto: `5005`
- Host: `localhost` (solo accesible localmente)
- Formato de datos: CSV
- Carpeta de QR: `static/qrcodes/`
- Carpeta de backups: `backups/`

Para cambiar la configuración, modifica las variables en `start.py`:
- `PUERTO`: Puerto del servidor
- `HOST`: Dirección de escucha
- `USUARIO`: Usuario de acceso
- `CONTRASEÑA`: Contraseña de acceso

## 🔒 Consideraciones de seguridad

- ⚠️ El sistema está diseñado para uso local en laboratorios educativos
- No expongas el servidor a internet sin implementar medidas de seguridad adicionales
- Las contraseñas se almacenan en texto plano en el código (modificar para producción)
- Realiza copias de seguridad periódicas de la carpeta `data/`

## 📦 Archivos incluidos

- `start.py` — Programa principal de XONILAB
- `requisitos.txt` — Dependencias Python
- `README.md` — Este archivo de documentación
- `xonilab_manual.pdf` — Manual detallado de usuario
- `templates/` — Vistas HTML del sistema
- `data/` — Archivos CSV con la información

## ✉️ Contacto y Créditos

- **Proyecto:** XONIDU
- **Creador:** Darian Alberto Camacho Salas
- **Versión:** 3.0
- **Año:** 2025
- **#Somos XONIDU**

---

**Sobre el proyecto:** Un sistema completo para la gestión eficiente de laboratorios educativos, desarrollado con tecnologías web modernas y almacenamiento en CSV para facilitar su implementación en entornos educativos.
**Creador:** Darian Alberto Camacho Salas
