```markdown
# XONILAB - Sistema de Gestión de Laboratorio

**Creador:** Darian Alberto Camacho Salas

> ⚠️ **Advertencia:** Sistema para fines educativos y gestión interna de laboratorios.

## 🎯 Descripción

Sistema web para gestionar laboratorios educativos. Permite administrar inventario, préstamos, alumnos, deudas y reservas. Almacena datos en CSV (sin base de datos).

## ✅ Requisitos

- Python 3.8+
- Flask
- qrcode
- pillow

## 🚀 Instalación

```bash
# Instalar dependencias
pip install flask qrcode pillow

# Ejecutar
python start.py
```

## 🔐 Acceso

```
URL: http://localhost:5005
Usuario: XONILAB
Contraseña: laboratorio
```

## 📁 Archivos

- `start.py` - Programa principal
- `data/` - Archivos CSV con datos
- `templates/` - Vistas HTML
- `static/qrcodes/` - Códigos QR
- `backups/` - Copias de seguridad

## ✨ Funciones

- 📦 Inventario con códigos QR
- 📋 Préstamos a alumnos
- 👥 Registro de alumnos
- 💰 Deudas por daños

## ⚙️ Configuración

Puerto por defecto: **5005**

---

*Desarrollado por XONIDU - Versión 3.0 - 2026*
```
