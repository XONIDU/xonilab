# XONILAB - Sistema de Gestión de Laboratorio

**Creador:** Darian Alberto Camacho Salas

> ⚠️ **Advertencia:** Sistema para fines educativos y gestión interna de laboratorios. No debe usarse con fines malintencionados. El autor no se hace responsable del uso indebido.

## 🎯 ¿Qué es XONILAB?

Sistema web en Python con Flask para gestión integral de laboratorios educativos. Administra inventario, préstamos, alumnos, deudas y reservas sin base de datos (archivos CSV). Incluye códigos QR, calendario y backups automáticos.

## 📥 Instalación

```bash
git clone https://github.com/XONIDU/xonilab.git
cd xonilab
python start.py
```

## ✅ Requisitos

- Python 3.8+
- Flask, qrcode[pil], pillow

## 🔐 Acceso

```
URL: http://localhost:5005
Usuario: XONILAB
Contraseña: laboratorio
```

## ✨ Funcionalidades

- 📦 **Inventario** con códigos QR
- 📋 **Préstamos** a alumnos
- 👥 **Registro** de alumnos
- 💰 **Deudas** por daños
- 📅 **Calendario** de reservas
- 📊 **Reportes** y estadísticas
- 💾 **Backups** automáticos

## 📁 Estructura

```
xonilab/
├── start.py          # Instalador y lanzador
├── xonilab.py        # Programa principal
├── requisitos.txt    # Dependencias
├── data/             # Archivos CSV
├── templates/        # Vistas HTML
├── static/qrcodes/   # Códigos QR
└── backups/          # Copias de seguridad
```

## 🖥️ Sistemas soportados

- **Windows:** `INICIAR_XONILAB.bat`
- **Linux:** `./INICIAR_XONILAB.sh`
- **macOS:** `INICIAR_XONILAB.command`

## ⚙️ Configuración

Puerto por defecto: **5005**

---

