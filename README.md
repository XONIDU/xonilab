# 📄 XONILAB - Sistema de Gestión de Laboratorio

**Advertencia:** Este sistema está diseñado **únicamente para fines educativos y de gestión interna** de laboratorios. No debe ser utilizado para actividades malintencionadas o sin la debida autorización. El autor no se hace responsable del uso indebido de esta herramienta.

---

## 🎯 ¿Qué es XONILAB?

XONILAB es un sistema web completo para la gestión integral de laboratorios educativos, desarrollado con Flask. Permite administrar:

- **Inventario** de materiales y equipos
- **Préstamos** de materiales a alumnos
- **Alumnos** y sus datos académicos
- **Deudas** por daños o extravíos
- **Calendario** de reservas de sesiones de práctica
- **Reportes** y estadísticas
- **Usuarios** con diferentes niveles de acceso (admin, profesor)
- **Copias de seguridad** de toda la información

El sistema almacena toda la información en archivos CSV, sin necesidad de base de datos externa, lo que lo hace portable y fácil de implementar.

---

## ✅ Requisitos

- Python 3.8+ instalado.
- Dependencias Python listadas en `requirements.txt`.
- Sistema operativo: Windows, Linux (Arch, Ubuntu, Debian) o macOS.

Instalar dependencias (recomendado dentro de un virtualenv):
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
