from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import csv
from datetime import datetime, timedelta
from functools import wraps
import calendar
import locale

# Configurar locale para español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

app = Flask(__name__)
app.secret_key = "xonilab_Darian_Alberto_Camacho_Salas"

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, 'data')
os.makedirs(CSV_FOLDER, exist_ok=True)

USUARIOS_CSV = os.path.join(CSV_FOLDER, 'usuarios.csv')
INVENTARIO_CSV = os.path.join(CSV_FOLDER, 'inventario.csv')
PRESTAMOS_CSV = os.path.join(CSV_FOLDER, 'prestamos.csv')
ALUMNOS_CSV = os.path.join(CSV_FOLDER, 'alumnos.csv')
DEUDAS_CSV = os.path.join(CSV_FOLDER, 'deudas.csv')
RESERVAS_CSV = os.path.join(CSV_FOLDER, 'reservas.csv')

# =============================================
# FUNCIONES AUXILIARES MEJORADAS
# =============================================

def inicializar_csv():
    """Inicializa los archivos CSV con datos de ejemplo"""
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'nombre', 'rol'])
            writer.writerow(['XONILAB', 'laboratorio', 'Administrador Laboratorio', 'admin'])
            writer.writerow(['PROFESOR1', 'prof123', 'Profesor Ejemplo', 'profesor'])
    
    if not os.path.exists(INVENTARIO_CSV):
        with open(INVENTARIO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                           'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro'])
    
    if not os.path.exists(PRESTAMOS_CSV):
        with open(PRESTAMOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_prestamo', 'id_item', 'nombre_item', 'id_alumno', 
                           'nombre_alumno', 'num_cuenta', 'fecha_prestamo', 
                           'fecha_devolucion', 'cantidad', 'estado', 'observaciones'])
    
    if not os.path.exists(ALUMNOS_CSV):
        with open(ALUMNOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_alumno', 'nombre', 'num_cuenta', 'grupo', 'semestre', 'telefono', 'email', 'activo'])
    
    if not os.path.exists(DEUDAS_CSV):
        with open(DEUDAS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_deuda', 'id_prestamo', 'nombre_alumno', 'num_cuenta', 
                           'nombre_item', 'descripcion_dano', 'monto', 'estado', 
                           'fecha_deuda', 'fecha_pago', 'observaciones'])
    
    if not os.path.exists(RESERVAS_CSV):
        with open(RESERVAS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_reserva', 'fecha', 'hora_inicio', 'hora_fin', 'duracion',
                           'grupo', 'materia', 'profesor', 'num_alumnos', 'observaciones', 
                           'estado', 'fecha_registro', 'responsable'])

def leer_csv(archivo):
    """Lee un archivo CSV"""
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")
        return []

def escribir_csv(archivo, datos, campos):
    """Escribe datos a un archivo CSV"""
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            if datos:
                writer.writerows(datos)
        return True
    except Exception as e:
        print(f"Error escribiendo {archivo}: {e}")
        return False

def generar_id():
    """Genera un ID único"""
    import secrets
    import string
    import time
    timestamp = int(time.time() * 1000)
    random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
    return f"{timestamp}{random_part}"

def generar_codigo_item(categoria, items):
    """Genera código único para ítem"""
    categoria_codigo = categoria[:3].upper()
    numero = len([i for i in items if i['categoria'].upper().startswith(categoria_codigo)]) + 1
    return f"{categoria_codigo}{numero:03d}"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor inicie sesión para continuar', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor inicie sesión para continuar', 'warning')
            return redirect(url_for('login'))
        if session.get('rol') != 'admin':
            flash('Acceso restringido. Se requieren permisos de administrador', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor para inyectar variables a todos los templates
@app.context_processor
def inject_now():
    return {
        'now': datetime.now(),
        'current_year': datetime.now().year,
        'current_month': datetime.now().month,
        'current_day': datetime.now().day
    }

# =============================================
# FUNCIONES PARA CALENDARIO MEJORADO
# =============================================

def obtener_mes_actual():
    """Obtiene el mes y año actual"""
    now = datetime.now()
    return now.year, now.month

def generar_calendario_mes(year, month):
    """Genera estructura completa del calendario para un mes"""
    # Obtener información del mes
    cal = calendar.monthcalendar(year, month)
    month_name = datetime(year, month, 1).strftime('%B').capitalize()
    year_name = year
    
    # Generar días del mes con información detallada
    days = []
    today = datetime.now().date()
    
    for week in cal:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append(None)  # Día fuera del mes
            else:
                day_date = datetime(year, month, day).date()
                is_today = (day_date == today)
                is_weekend = day_date.weekday() >= 5  # 5=sábado, 6=domingo
                is_past = (day_date < today)
                
                week_days.append({
                    'day': day,
                    'date': day_date.strftime('%Y-%m-%d'),
                    'is_today': is_today,
                    'is_weekend': is_weekend,
                    'is_past': is_past,
                    'weekday': day_date.strftime('%A').capitalize()[:3]
                })
        days.append(week_days)
    
    # Calcular estadísticas del mes
    total_dias = sum(1 for week in cal for day in week if day != 0)
    dias_laborables = sum(1 for week in cal for day in week 
                         if day != 0 and datetime(year, month, day).weekday() < 5)
    
    # Obtener reservas del mes
    reservas = leer_csv(RESERVAS_CSV)
    reservas_mes = []
    for reserva in reservas:
        try:
            fecha_reserva = datetime.strptime(reserva['fecha'], '%Y-%m-%d')
            if fecha_reserva.year == year and fecha_reserva.month == month:
                reservas_mes.append(reserva)
        except:
            continue
    
    # Contar reservas por día
    reservas_por_dia = {}
    for reserva in reservas_mes:
        fecha = reserva['fecha']
        if fecha not in reservas_por_dia:
            reservas_por_dia[fecha] = 0
        reservas_por_dia[fecha] += 1
    
    # Agregar conteo de reservas a cada día
    for week in days:
        for day_info in week:
            if day_info and 'date' in day_info:
                day_info['reservas_count'] = reservas_por_dia.get(day_info['date'], 0)
    
    # Calcular horas totales reservadas
    horas_totales = 0
    grupos_unicos = set()
    profesores_unicos = set()
    for reserva in reservas_mes:
        try:
            horas_totales += int(reserva.get('duracion', 0))
            grupos_unicos.add(reserva.get('grupo', ''))
            profesores_unicos.add(reserva.get('profesor', ''))
        except:
            continue
    
    return {
        'year': year,
        'month': month,
        'month_name': month_name,
        'year_name': year_name,
        'calendar': days,
        'reservas_mes': reservas_mes,
        'total_reservas': len(reservas_mes),
        'total_dias': total_dias,
        'dias_laborables': dias_laborables,
        'horas_totales': horas_totales,
        'grupos_unicos': len(grupos_unicos),
        'profesores_unicos': len(profesores_unicos),
        'prev_month': get_previous_month(year, month),
        'next_month': get_next_month(year, month),
        'today': today.strftime('%Y-%m-%d')
    }

def get_previous_month(year, month):
    """Obtiene el mes anterior"""
    if month == 1:
        return year - 1, 12
    return year, month - 1

def get_next_month(year, month):
    """Obtiene el mes siguiente"""
    if month == 12:
        return year + 1, 1
    return year, month + 1

def obtener_horarios_disponibles(fecha, hora_inicio=None):
    """Obtiene horarios disponibles para una fecha específica"""
    # Generar todos los horarios de 7am a 7pm
    horarios = []
    for hora in range(7, 19):
        horarios.append(f"{hora:02d}:00")
    
    # Si no hay hora_inicio especificada, devolver todos los horarios
    if not hora_inicio:
        return horarios
    
    # Obtener reservas para la fecha
    reservas = leer_csv(RESERVAS_CSV)
    reservas_dia = [r for r in reservas if r['fecha'] == fecha and r.get('estado') == 'confirmada']
    
    # Verificar horarios ocupados
    horarios_ocupados = []
    for reserva in reservas_dia:
        try:
            inicio = int(reserva['hora_inicio'].split(':')[0])
            fin = int(reserva['hora_fin'].split(':')[0])
            # Marcar todas las horas que están ocupadas
            for hora in range(inicio, fin):
                horarios_ocupados.append(f"{hora:02d}:00")
        except:
            continue
    
    # Filtrar horarios disponibles
    horarios_disponibles = [h for h in horarios if h not in horarios_ocupados]
    
    return horarios_disponibles, horarios_ocupados

def verificar_disponibilidad(fecha, hora_inicio, duracion):
    """Verifica si un horario está disponible"""
    try:
        hora_inicio_int = int(hora_inicio.split(':')[0])
        hora_fin_int = hora_inicio_int + int(duracion)
        
        # Verificar que esté dentro del rango permitido
        if hora_inicio_int < 7 or hora_fin_int > 19:
            return False, "Horario fuera del rango permitido (7:00 - 19:00)"
        
        # Obtener reservas del día
        reservas = leer_csv(RESERVAS_CSV)
        reservas_dia = [r for r in reservas if r['fecha'] == fecha and r.get('estado') == 'confirmada']
        
        # Verificar solapamiento
        for reserva in reservas_dia:
            try:
                inicio_existente = int(reserva['hora_inicio'].split(':')[0])
                fin_existente = int(reserva['hora_fin'].split(':')[0])
                
                # Verificar solapamiento
                if hora_inicio_int < fin_existente and hora_fin_int > inicio_existente:
                    return False, f"El horario se solapa con una reserva existente: {reserva['hora_inicio']}-{reserva['hora_fin']}"
            except:
                continue
        
        return True, "Horario disponible"
    except Exception as e:
        return False, f"Error verificando disponibilidad: {str(e)}"

def obtener_horarios_detalle(fecha):
    """Obtiene detalle de horarios para un día específico"""
    horarios = []
    reservas = leer_csv(RESERVAS_CSV)
    reservas_dia = [r for r in reservas if r['fecha'] == fecha and r.get('estado') == 'confirmada']
    
    for hora in range(7, 19):
        hora_str = f"{hora:02d}:00"
        ocupado = False
        reserva_en_hora = None
        es_inicio = False
        
        for reserva in reservas_dia:
            try:
                hora_inicio = int(reserva['hora_inicio'].split(':')[0])
                hora_fin = int(reserva['hora_fin'].split(':')[0])
                
                if hora_inicio <= hora < hora_fin:
                    ocupado = True
                    reserva_en_hora = reserva
                    es_inicio = (hora == hora_inicio)
                    break
            except:
                continue
        
        horarios.append({
            'hora': hora_str,
            'ocupado': ocupado,
            'reserva': reserva_en_hora,
            'es_inicio': es_inicio
        })
    
    return horarios

# =============================================
# RUTAS PRINCIPALES
# =============================================

@app.route('/')
def index():
    """Página principal"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        usuarios = leer_csv(USUARIOS_CSV)
        usuario = next((u for u in usuarios if u['username'] == username and u['password'] == password), None)
        
        if usuario:
            session['username'] = username
            session['nombre'] = usuario['nombre']
            session['rol'] = usuario.get('rol', 'usuario')
            flash(f'¡Bienvenido/a, {usuario["nombre"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    try:
        inventario = leer_csv(INVENTARIO_CSV)
        prestamos = leer_csv(PRESTAMOS_CSV)
        alumnos = leer_csv(ALUMNOS_CSV)
        deudas = leer_csv(DEUDAS_CSV)
        reservas = leer_csv(RESERVAS_CSV)
        
        # Estadísticas
        total_items = len(inventario)
        
        # Préstamos activos
        prestamos_activos = [p for p in prestamos if p.get('estado') == 'prestado']
        total_prestamos = len(prestamos_activos)
        
        # Alumnos activos
        alumnos_activos = [a for a in alumnos if a.get('activo') == '1']
        total_alumnos = len(alumnos_activos)
        
        # Deudas pendientes
        deudas_pendientes = [d for d in deudas if d.get('estado') == 'pendiente']
        total_deudas = len(deudas_pendientes)
        total_monto_deudas = sum(float(d.get('monto', 0)) for d in deudas_pendientes)
        
        # Ítems con bajo stock
        items_bajo_stock = []
        for item in inventario:
            try:
                cantidad = int(item.get('cantidad', 0))
                if cantidad <= 5:
                    items_bajo_stock.append(item)
            except:
                continue
        
        # Reservas de hoy
        hoy = datetime.now().strftime('%Y-%m-%d')
        reservas_hoy = [r for r in reservas if r['fecha'] == hoy and r.get('estado') == 'confirmada']
        reservas_hoy_count = len(reservas_hoy)
        
        # Préstamos próximos a vencer (en 3 días)
        hoy_date = datetime.now()
        prestamos_proximos_vencer = []
        for prestamo in prestamos_activos:
            try:
                fecha_devolucion = datetime.strptime(prestamo.get('fecha_devolucion', ''), '%Y-%m-%d')
                dias_restantes = (fecha_devolucion - hoy_date).days
                if 0 <= dias_restantes <= 3:
                    prestamos_proximos_vencer.append(prestamo)
            except:
                continue
        
        # Últimos movimientos
        prestamos_recientes = prestamos[-5:] if len(prestamos) > 5 else prestamos
        for prestamo in prestamos_recientes:
            try:
                fecha_devolucion = datetime.strptime(prestamo.get('fecha_devolucion', ''), '%Y-%m-%d')
                dias_restantes = (fecha_devolucion - hoy_date).days
                prestamo['dias_restantes'] = dias_restantes
            except:
                prestamo['dias_restantes'] = None
        reservas_proximas = []
        
        # Reservas de los próximos 7 días
        for i in range(7):
            fecha = (hoy_date + timedelta(days=i)).strftime('%Y-%m-%d')
            reservas_dia = [r for r in reservas if r['fecha'] == fecha and r.get('estado') == 'confirmada']
            if reservas_dia:
                reservas_proximas.extend(reservas_dia[:2])
        
        return render_template('dashboard.html',
                             total_items=total_items,
                             total_prestamos=total_prestamos,
                             total_alumnos=total_alumnos,
                             total_deudas=total_deudas,
                             total_monto_deudas=total_monto_deudas,
                             items_bajo_stock=items_bajo_stock[:5],
                             prestamos_recientes=prestamos_recientes,
                             prestamos_proximos_vencer=prestamos_proximos_vencer[:5],
                             reservas_hoy=reservas_hoy,
                             reservas_hoy_count=reservas_hoy_count,
                             reservas_proximas=reservas_proximas[:5],
                             today=hoy)
    
    except Exception as e:
        flash(f'Error cargando el dashboard: {str(e)}', 'danger')
        return render_template('dashboard.html',
                             total_items=0,
                             total_prestamos=0,
                             total_alumnos=0,
                             total_deudas=0,
                             total_monto_deudas=0,
                             items_bajo_stock=[],
                             prestamos_recientes=[],
                             prestamos_proximos_vencer=[],
                             reservas_hoy=[],
                             reservas_hoy_count=0,
                             reservas_proximas=[],
                             today=datetime.now().strftime('%Y-%m-%d'))

# =============================================
# RUTAS DE INVENTARIO
# =============================================

@app.route('/inventario')
@login_required
def inventario():
    """Página de inventario"""
    items = leer_csv(INVENTARIO_CSV)
    
    # Categorías disponibles
    categorias = sorted(set(item['categoria'] for item in items if item.get('categoria')))
    
    # Filtrar por búsqueda
    buscar = request.args.get('buscar', '')
    categoria = request.args.get('categoria', '')
    estado = request.args.get('estado', '')
    
    if buscar:
        buscar = buscar.lower()
        items = [i for i in items if buscar in i.get('nombre', '').lower() or 
                               buscar in i.get('codigo', '').lower() or
                               buscar in i.get('descripcion', '').lower()]
    
    if categoria:
        items = [i for i in items if i.get('categoria') == categoria]
    
    if estado:
        if estado == 'disponible':
            items = [i for i in items if int(i.get('cantidad', 0)) > 0]
        elif estado == 'agotado':
            items = [i for i in items if int(i.get('cantidad', 0)) == 0]
        elif estado == 'bajo_stock':
            items = [i for i in items if 0 < int(i.get('cantidad', 0)) <= 5]
    
    # Estadísticas
    total_items = len(items)
    items_disponibles = len([i for i in items if int(i.get('cantidad', 0)) > 0])
    items_agotados = len([i for i in items if int(i.get('cantidad', 0)) == 0])
    items_bajo_stock = len([i for i in items if 0 < int(i.get('cantidad', 0)) <= 5])
    
    return render_template('inventario.html', 
                         items=items, 
                         categorias=categorias,
                         buscar=buscar,
                         categoria=categoria,
                         estado=estado,
                         total_items=total_items,
                         items_disponibles=items_disponibles,
                         items_agotados=items_agotados,
                         items_bajo_stock=items_bajo_stock)

@app.route('/inventario/agregar', methods=['POST'])
@login_required
def agregar_item():
    """Agregar nuevo ítem"""
    try:
        nombre = request.form.get('nombre', '').strip()
        categoria = request.form.get('categoria', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        cantidad = request.form.get('cantidad', '0').strip()
        unidad = request.form.get('unidad', 'pzas').strip()
        ubicacion = request.form.get('ubicacion', '').strip()
        
        if not nombre or not categoria:
            flash('Nombre y categoría son obligatorios', 'warning')
            return redirect(url_for('inventario'))
        
        # Validar cantidad
        try:
            cantidad_int = int(cantidad)
            if cantidad_int < 0:
                flash('La cantidad no puede ser negativa', 'danger')
                return redirect(url_for('inventario'))
        except:
            flash('Cantidad inválida', 'danger')
            return redirect(url_for('inventario'))
        
        # Generar código único
        items = leer_csv(INVENTARIO_CSV)
        codigo = generar_codigo_item(categoria, items)
        
        nuevo_item = {
            'id_item': generar_id(),
            'codigo': codigo,
            'nombre': nombre,
            'categoria': categoria,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'unidad': unidad,
            'ubicacion': ubicacion,
            'estado': 'disponible' if int(cantidad) > 0 else 'agotado',
            'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        items.append(nuevo_item)
        
        if escribir_csv(INVENTARIO_CSV, items, 
                       ['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                        'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro']):
            flash(f'✅ Ítem "{nombre}" agregado correctamente (Código: {codigo})', 'success')
        else:
            flash('Error al guardar el ítem', 'danger')
        
        return redirect(url_for('inventario'))
    
    except Exception as e:
        flash(f'Error al agregar ítem: {str(e)}', 'danger')
        return redirect(url_for('inventario'))

@app.route('/inventario/editar/<id_item>', methods=['POST'])
@login_required
def editar_item(id_item):
    """Editar ítem existente"""
    try:
        items = leer_csv(INVENTARIO_CSV)
        item_encontrado = False
        
        for item in items:
            if item['id_item'] == id_item:
                item['nombre'] = request.form.get('nombre', '').strip()
                item['categoria'] = request.form.get('categoria', '').strip()
                item['descripcion'] = request.form.get('descripcion', '').strip()
                item['cantidad'] = request.form.get('cantidad', '0').strip()
                item['unidad'] = request.form.get('unidad', '').strip()
                item['ubicacion'] = request.form.get('ubicacion', '').strip()
                
                # Actualizar estado según cantidad
                try:
                    if int(item['cantidad']) > 0:
                        item['estado'] = 'disponible'
                    else:
                        item['estado'] = 'agotado'
                except:
                    item['estado'] = 'disponible'
                
                item_encontrado = True
                break
        
        if item_encontrado:
            if escribir_csv(INVENTARIO_CSV, items, 
                           ['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                            'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro']):
                flash('✅ Ítem actualizado correctamente', 'success')
            else:
                flash('Error al actualizar el ítem', 'danger')
        else:
            flash('Ítem no encontrado', 'danger')
        
        return redirect(url_for('inventario'))
    
    except Exception as e:
        flash(f'Error al editar ítem: {str(e)}', 'danger')
        return redirect(url_for('inventario'))

@app.route('/inventario/eliminar/<id_item>')
@login_required
@admin_required
def eliminar_item(id_item):
    """Eliminar ítem"""
    try:
        items = leer_csv(INVENTARIO_CSV)
        items_filtrados = [item for item in items if item['id_item'] != id_item]
        
        if len(items_filtrados) < len(items):
            if escribir_csv(INVENTARIO_CSV, items_filtrados, 
                           ['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                            'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro']):
                flash('✅ Ítem eliminado correctamente', 'success')
            else:
                flash('Error al eliminar el ítem', 'danger')
        else:
            flash('Ítem no encontrado', 'danger')
        
        return redirect(url_for('inventario'))
    
    except Exception as e:
        flash(f'Error al eliminar ítem: {str(e)}', 'danger')
        return redirect(url_for('inventario'))

# =============================================
# RUTAS DE PRÉSTAMOS
# =============================================

@app.route('/prestamos')
@login_required
def prestamos():
    """Página de préstamos"""
    prestamos_lista = leer_csv(PRESTAMOS_CSV)
    items = leer_csv(INVENTARIO_CSV)
    alumnos = leer_csv(ALUMNOS_CSV)
    
    # Filtrar por estado
    estado = request.args.get('estado', '')
    buscar = request.args.get('buscar', '')
    
    if estado:
        prestamos_lista = [p for p in prestamos_lista if p.get('estado') == estado]
    
    if buscar:
        buscar = buscar.lower()
        prestamos_lista = [p for p in prestamos_lista 
                          if buscar in p.get('nombre_alumno', '').lower() or 
                             buscar in p.get('nombre_item', '').lower() or
                             buscar in p.get('num_cuenta', '').lower()]
    
    # Ordenar por fecha (más recientes primero)
    prestamos_lista.sort(key=lambda x: x.get('fecha_prestamo', ''), reverse=True)
    
    # Estadísticas
    total_prestamos = len(prestamos_lista)
    prestamos_activos = len([p for p in prestamos_lista if p.get('estado') == 'prestado'])
    prestamos_devueltos = len([p for p in prestamos_lista if p.get('estado') == 'devuelto'])
    
    # Items disponibles (con stock > 0)
    items_disponibles = [i for i in items if int(i.get('cantidad', 0)) > 0]
    
    # Alumnos activos
    alumnos_activos = [a for a in alumnos if a.get('activo') == '1']
    
    return render_template('prestamos.html',
                         prestamos=prestamos_lista,
                         items=items_disponibles,
                         alumnos=alumnos_activos,
                         estado=estado,
                         buscar=buscar,
                         total_prestamos=total_prestamos,
                         prestamos_activos=prestamos_activos,
                         prestamos_devueltos=prestamos_devueltos)

@app.route('/prestamos/nuevo', methods=['POST'])
@login_required
def nuevo_prestamo():
    """Crear nuevo préstamo"""
    try:
        id_item = request.form.get('item', '').strip()
        id_alumno = request.form.get('alumno', '').strip()
        cantidad = request.form.get('cantidad', '1').strip()
        fecha_devolucion = request.form.get('fecha_devolucion', '').strip()
        observaciones = request.form.get('observaciones', '').strip()
        
        # Validar datos
        if not id_item or not id_alumno:
            flash('Debe seleccionar un ítem y un alumno', 'warning')
            return redirect(url_for('prestamos'))
        
        # Obtener información del ítem
        items = leer_csv(INVENTARIO_CSV)
        item = next((i for i in items if i['id_item'] == id_item), None)
        
        if not item:
            flash('Ítem no encontrado', 'danger')
            return redirect(url_for('prestamos'))
        
        # Verificar disponibilidad
        try:
            cant_disponible = int(item.get('cantidad', 0))
            cant_prestar = int(cantidad)
            
            if cant_prestar <= 0:
                flash('La cantidad debe ser mayor a 0', 'danger')
                return redirect(url_for('prestamos'))
            
            if cant_prestar > cant_disponible:
                flash(f'Cantidad insuficiente. Disponible: {cant_disponible}', 'danger')
                return redirect(url_for('prestamos'))
            
            # Actualizar inventario
            item['cantidad'] = str(cant_disponible - cant_prestar)
            if int(item['cantidad']) == 0:
                item['estado'] = 'agotado'
            
            if not escribir_csv(INVENTARIO_CSV, items, 
                               ['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                                'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro']):
                flash('Error al actualizar el inventario', 'danger')
                return redirect(url_for('prestamos'))
        
        except ValueError:
            flash('Error en la cantidad especificada', 'danger')
            return redirect(url_for('prestamos'))
        
        # Obtener información del alumno
        alumnos = leer_csv(ALUMNOS_CSV)
        alumno = next((a for a in alumnos if a['id_alumno'] == id_alumno), None)
        
        if not alumno:
            flash('Alumno no encontrado', 'danger')
            return redirect(url_for('prestamos'))
        
        # Verificar si el alumno tiene deudas pendientes
        deudas = leer_csv(DEUDAS_CSV)
        deudas_alumno = [d for d in deudas if d['num_cuenta'] == alumno['num_cuenta'] and d['estado'] == 'pendiente']
        
        if deudas_alumno:
            flash(f'El alumno tiene {len(deudas_alumno)} deuda(s) pendiente(s). No se puede realizar el préstamo.', 'warning')
            return redirect(url_for('prestamos'))
        
        # Crear préstamo
        prestamos = leer_csv(PRESTAMOS_CSV)
        
        nuevo_prestamo = {
            'id_prestamo': generar_id(),
            'id_item': id_item,
            'nombre_item': item['nombre'],
            'id_alumno': id_alumno,
            'nombre_alumno': alumno['nombre'],
            'num_cuenta': alumno['num_cuenta'],
            'fecha_prestamo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_devolucion': fecha_devolucion,
            'cantidad': cantidad,
            'estado': 'prestado',
            'observaciones': observaciones
        }
        
        prestamos.append(nuevo_prestamo)
        
        if escribir_csv(PRESTAMOS_CSV, prestamos,
                       ['id_prestamo', 'id_item', 'nombre_item', 'id_alumno', 
                        'nombre_alumno', 'num_cuenta', 'fecha_prestamo', 
                        'fecha_devolucion', 'cantidad', 'estado', 'observaciones']):
            flash('✅ Préstamo registrado correctamente', 'success')
        else:
            flash('Error al registrar el préstamo', 'danger')
        
        return redirect(url_for('prestamos'))
    
    except Exception as e:
        flash(f'Error al crear préstamo: {str(e)}', 'danger')
        return redirect(url_for('prestamos'))

@app.route('/prestamos/devolver/<id_prestamo>')
@login_required
def devolver_prestamo(id_prestamo):
    """Registrar devolución"""
    try:
        prestamos = leer_csv(PRESTAMOS_CSV)
        items = leer_csv(INVENTARIO_CSV)
        devuelto = False
        
        for prestamo in prestamos:
            if prestamo['id_prestamo'] == id_prestamo and prestamo['estado'] == 'prestado':
                # Marcar como devuelto
                prestamo['estado'] = 'devuelto'
                prestamo['fecha_devolucion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Devolver cantidad al inventario
                for item in items:
                    if item['id_item'] == prestamo['id_item']:
                        try:
                            cant_actual = int(item.get('cantidad', 0))
                            cant_devuelta = int(prestamo.get('cantidad', 0))
                            item['cantidad'] = str(cant_actual + cant_devuelta)
                            
                            if int(item['cantidad']) > 0:
                                item['estado'] = 'disponible'
                        except:
                            pass
                        break
                
                devuelto = True
                break
        
        if devuelto:
            # Guardar cambios
            if (escribir_csv(PRESTAMOS_CSV, prestamos,
                           ['id_prestamo', 'id_item', 'nombre_item', 'id_alumno', 
                            'nombre_alumno', 'num_cuenta', 'fecha_prestamo', 
                            'fecha_devolucion', 'cantidad', 'estado', 'observaciones']) and
                escribir_csv(INVENTARIO_CSV, items, 
                           ['id_item', 'codigo', 'nombre', 'categoria', 'descripcion', 
                            'cantidad', 'unidad', 'ubicacion', 'estado', 'fecha_registro'])):
                flash('✅ Préstamo devuelto correctamente', 'success')
            else:
                flash('Error al guardar los cambios', 'danger')
        else:
            flash('Préstamo no encontrado o ya devuelto', 'warning')
        
        return redirect(url_for('prestamos'))
    
    except Exception as e:
        flash(f'Error al devolver préstamo: {str(e)}', 'danger')
        return redirect(url_for('prestamos'))

# =============================================
# RUTAS DE ALUMNOS
# =============================================

@app.route('/alumnos')
@login_required
def alumnos():
    """Página de alumnos"""
    alumnos_lista = leer_csv(ALUMNOS_CSV)
    
    # Filtrar por búsqueda
    buscar = request.args.get('buscar', '')
    grupo = request.args.get('grupo', '')
    estado = request.args.get('estado', '')
    
    if buscar:
        buscar = buscar.lower()
        alumnos_lista = [a for a in alumnos_lista 
                        if buscar in a.get('nombre', '').lower() or 
                           buscar in a.get('num_cuenta', '').lower() or
                           buscar in a.get('email', '').lower()]
    
    if grupo:
        alumnos_lista = [a for a in alumnos_lista if a.get('grupo') == grupo]
    
    if estado:
        if estado == 'activo':
            alumnos_lista = [a for a in alumnos_lista if a.get('activo') == '1']
        elif estado == 'inactivo':
            alumnos_lista = [a for a in alumnos_lista if a.get('activo') == '0']
    
    # Obtener grupos únicos para filtro
    grupos = sorted(set(a['grupo'] for a in alumnos_lista if a.get('grupo')))
    
    # Estadísticas
    total_alumnos = len(alumnos_lista)
    alumnos_activos = len([a for a in alumnos_lista if a.get('activo') == '1'])
    alumnos_inactivos = total_alumnos - alumnos_activos
    
    # Obtener préstamos y deudas para estadísticas
    prestamos = leer_csv(PRESTAMOS_CSV)
    deudas = leer_csv(DEUDAS_CSV)
    
    # Agregar estadísticas a cada alumno
    for alumno in alumnos_lista:
        num_cuenta = alumno.get('num_cuenta', '')
        # Contar préstamos activos
        prestamos_alumno = [p for p in prestamos if p.get('num_cuenta') == num_cuenta and p.get('estado') == 'prestado']
        alumno['prestamos_activos'] = len(prestamos_alumno)
        # Contar deudas pendientes
        deudas_alumno = [d for d in deudas if d.get('num_cuenta') == num_cuenta and d.get('estado') == 'pendiente']
        alumno['deudas_pendientes'] = len(deudas_alumno)
    
    return render_template('alumnos.html', 
                         alumnos=alumnos_lista, 
                         buscar=buscar,
                         grupo=grupo,
                         estado=estado,
                         grupos=grupos,
                         total_alumnos=total_alumnos,
                         alumnos_activos=alumnos_activos,
                         alumnos_inactivos=alumnos_inactivos)

@app.route('/alumnos/agregar', methods=['POST'])
@login_required
def agregar_alumno():
    """Agregar nuevo alumno"""
    try:
        nombre = request.form.get('nombre', '').strip()
        num_cuenta = request.form.get('num_cuenta', '').strip()
        grupo = request.form.get('grupo', '').strip()
        semestre = request.form.get('semestre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        email = request.form.get('email', '').strip()
        
        if not nombre or not num_cuenta:
            flash('Nombre y número de cuenta son obligatorios', 'warning')
            return redirect(url_for('alumnos'))
        
        # Verificar si ya existe
        alumnos = leer_csv(ALUMNOS_CSV)
        if any(a.get('num_cuenta') == num_cuenta for a in alumnos):
            flash('Ya existe un alumno con ese número de cuenta', 'danger')
            return redirect(url_for('alumnos'))
        
        nuevo_alumno = {
            'id_alumno': generar_id(),
            'nombre': nombre,
            'num_cuenta': num_cuenta,
            'grupo': grupo,
            'semestre': semestre,
            'telefono': telefono,
            'email': email,
            'activo': '1'
        }
        
        alumnos.append(nuevo_alumno)
        
        if escribir_csv(ALUMNOS_CSV, alumnos,
                       ['id_alumno', 'nombre', 'num_cuenta', 'grupo', 'semestre', 'telefono', 'email', 'activo']):
            flash(f'✅ Alumno "{nombre}" agregado correctamente', 'success')
        else:
            flash('Error al guardar el alumno', 'danger')
        
        return redirect(url_for('alumnos'))
    
    except Exception as e:
        flash(f'Error al agregar alumno: {str(e)}', 'danger')
        return redirect(url_for('alumnos'))

@app.route('/alumnos/editar/<id_alumno>', methods=['POST'])
@login_required
def editar_alumno(id_alumno):
    """Editar alumno"""
    try:
        alumnos = leer_csv(ALUMNOS_CSV)
        encontrado = False
        
        for alumno in alumnos:
            if alumno['id_alumno'] == id_alumno:
                alumno['nombre'] = request.form.get('nombre', '').strip()
                alumno['num_cuenta'] = request.form.get('num_cuenta', '').strip()
                alumno['grupo'] = request.form.get('grupo', '').strip()
                alumno['semestre'] = request.form.get('semestre', '').strip()
                alumno['telefono'] = request.form.get('telefono', '').strip()
                alumno['email'] = request.form.get('email', '').strip()
                alumno['activo'] = request.form.get('activo', '1')
                encontrado = True
                break
        
        if encontrado:
            if escribir_csv(ALUMNOS_CSV, alumnos,
                           ['id_alumno', 'nombre', 'num_cuenta', 'grupo', 'semestre', 'telefono', 'email', 'activo']):
                flash('✅ Alumno actualizado correctamente', 'success')
            else:
                flash('Error al actualizar el alumno', 'danger')
        else:
            flash('Alumno no encontrado', 'danger')
        
        return redirect(url_for('alumnos'))
    
    except Exception as e:
        flash(f'Error al editar alumno: {str(e)}', 'danger')
        return redirect(url_for('alumnos'))

@app.route('/alumnos/eliminar/<id_alumno>')
@login_required
@admin_required
def eliminar_alumno(id_alumno):
    """Eliminar alumno"""
    try:
        alumnos = leer_csv(ALUMNOS_CSV)
        alumnos_filtrados = [a for a in alumnos if a['id_alumno'] != id_alumno]
        
        if len(alumnos_filtrados) < len(alumnos):
            # Verificar si el alumno tiene préstamos activos
            prestamos = leer_csv(PRESTAMOS_CSV)
            alumno_eliminar = next((a for a in alumnos if a['id_alumno'] == id_alumno), None)
            
            if alumno_eliminar:
                num_cuenta = alumno_eliminar.get('num_cuenta', '')
                prestamos_activos = [p for p in prestamos if p.get('num_cuenta') == num_cuenta and p.get('estado') == 'prestado']
                
                if prestamos_activos:
                    flash('No se puede eliminar el alumno porque tiene préstamos activos', 'warning')
                    return redirect(url_for('alumnos'))
            
            if escribir_csv(ALUMNOS_CSV, alumnos_filtrados,
                           ['id_alumno', 'nombre', 'num_cuenta', 'grupo', 'semestre', 'telefono', 'email', 'activo']):
                flash('✅ Alumno eliminado correctamente', 'success')
            else:
                flash('Error al eliminar el alumno', 'danger')
        else:
            flash('Alumno no encontrado', 'danger')
        
        return redirect(url_for('alumnos'))
    
    except Exception as e:
        flash(f'Error al eliminar alumno: {str(e)}', 'danger')
        return redirect(url_for('alumnos'))

# =============================================
# RUTAS DE DEUDAS
# =============================================

@app.route('/deudas')
@login_required
def deudas():
    """Página de deudas por daños en préstamos"""
    deudas_lista = leer_csv(DEUDAS_CSV)
    prestamos = leer_csv(PRESTAMOS_CSV)
    
    # Filtrar por estado
    estado = request.args.get('estado', '')
    buscar = request.args.get('buscar', '')
    
    if estado:
        deudas_lista = [d for d in deudas_lista if d.get('estado') == estado]
    
    if buscar:
        buscar = buscar.lower()
        deudas_lista = [d for d in deudas_lista 
                       if buscar in d.get('nombre_alumno', '').lower() or 
                          buscar in d.get('num_cuenta', '').lower() or
                          buscar in d.get('nombre_item', '').lower()]
    
    # Ordenar por fecha
    deudas_lista.sort(key=lambda x: x.get('fecha_deuda', ''), reverse=True)
    
    # Estadísticas
    total_deudas = len(deudas_lista)
    deudas_pendientes = len([d for d in deudas_lista if d.get('estado') == 'pendiente'])
    deudas_pagadas = len([d for d in deudas_lista if d.get('estado') == 'pagado'])
    
    # Calcular montos
    total_monto = sum(float(d.get('monto', 0)) for d in deudas_lista)
    monto_pendiente = sum(float(d.get('monto', 0)) for d in deudas_lista if d.get('estado') == 'pendiente')
    monto_pagado = sum(float(d.get('monto', 0)) for d in deudas_lista if d.get('estado') == 'pagado')
    
    return render_template('deudas.html',
                         deudas=deudas_lista,
                         prestamos=prestamos,
                         estado=estado,
                         buscar=buscar,
                         total_deudas=total_deudas,
                         deudas_pendientes=deudas_pendientes,
                         deudas_pagadas=deudas_pagadas,
                         total_monto=total_monto,
                         monto_pendiente=monto_pendiente,
                         monto_pagado=monto_pagado)

@app.route('/deudas/nueva', methods=['POST'])
@login_required
def nueva_deuda():
    """Registrar nueva deuda por daño"""
    try:
        id_prestamo = request.form.get('prestamo', '').strip()
        descripcion_dano = request.form.get('descripcion_dano', '').strip()
        monto = request.form.get('monto', '0').strip()
        observaciones = request.form.get('observaciones', '').strip()
        
        if not id_prestamo or not descripcion_dano:
            flash('Debe seleccionar un préstamo y describir el daño', 'warning')
            return redirect(url_for('deudas'))
        
        # Validar monto
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                flash('El monto debe ser mayor a 0', 'danger')
                return redirect(url_for('deudas'))
        except:
            flash('Monto inválido', 'danger')
            return redirect(url_for('deudas'))
        
        # Obtener información del préstamo
        prestamos = leer_csv(PRESTAMOS_CSV)
        prestamo = next((p for p in prestamos if p['id_prestamo'] == id_prestamo), None)
        
        if not prestamo:
            flash('Préstamo no encontrado', 'danger')
            return redirect(url_for('deudas'))
        
        # Crear deuda
        deudas = leer_csv(DEUDAS_CSV)
        
        nueva_deuda = {
            'id_deuda': generar_id(),
            'id_prestamo': id_prestamo,
            'nombre_alumno': prestamo['nombre_alumno'],
            'num_cuenta': prestamo['num_cuenta'],
            'nombre_item': prestamo['nombre_item'],
            'descripcion_dano': descripcion_dano,
            'monto': monto,
            'estado': 'pendiente',
            'fecha_deuda': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_pago': '',
            'observaciones': observaciones
        }
        
        deudas.append(nueva_deuda)
        
        if escribir_csv(DEUDAS_CSV, deudas,
                       ['id_deuda', 'id_prestamo', 'nombre_alumno', 'num_cuenta', 
                        'nombre_item', 'descripcion_dano', 'monto', 'estado', 
                        'fecha_deuda', 'fecha_pago', 'observaciones']):
            flash('✅ Deuda registrada correctamente', 'success')
        else:
            flash('Error al registrar la deuda', 'danger')
        
        return redirect(url_for('deudas'))
    
    except Exception as e:
        flash(f'Error al registrar deuda: {str(e)}', 'danger')
        return redirect(url_for('deudas'))

@app.route('/deudas/pagar/<id_deuda>')
@login_required
def pagar_deuda(id_deuda):
    """Marcar deuda como pagada"""
    try:
        deudas = leer_csv(DEUDAS_CSV)
        encontrada = False
        
        for deuda in deudas:
            if deuda['id_deuda'] == id_deuda:
                deuda['estado'] = 'pagado'
                deuda['fecha_pago'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                encontrada = True
                break
        
        if encontrada:
            if escribir_csv(DEUDAS_CSV, deudas,
                           ['id_deuda', 'id_prestamo', 'nombre_alumno', 'num_cuenta', 
                            'nombre_item', 'descripcion_dano', 'monto', 'estado', 
                            'fecha_deuda', 'fecha_pago', 'observaciones']):
                flash('✅ Deuda marcada como pagada', 'success')
            else:
                flash('Error al actualizar la deuda', 'danger')
        else:
            flash('Deuda no encontrada', 'danger')
        
        return redirect(url_for('deudas'))
    
    except Exception as e:
        flash(f'Error al pagar deuda: {str(e)}', 'danger')
        return redirect(url_for('deudas'))

@app.route('/deudas/eliminar/<id_deuda>')
@login_required
@admin_required
def eliminar_deuda(id_deuda):
    """Eliminar deuda"""
    try:
        deudas = leer_csv(DEUDAS_CSV)
        deudas_filtradas = [d for d in deudas if d['id_deuda'] != id_deuda]
        
        if len(deudas_filtradas) < len(deudas):
            if escribir_csv(DEUDAS_CSV, deudas_filtradas,
                           ['id_deuda', 'id_prestamo', 'nombre_alumno', 'num_cuenta', 
                            'nombre_item', 'descripcion_dano', 'monto', 'estado', 
                            'fecha_deuda', 'fecha_pago', 'observaciones']):
                flash('✅ Deuda eliminada correctamente', 'success')
            else:
                flash('Error al eliminar la deuda', 'danger')
        else:
            flash('Deuda no encontrada', 'danger')
        
        return redirect(url_for('deudas'))
    
    except Exception as e:
        flash(f'Error al eliminar deuda: {str(e)}', 'danger')
        return redirect(url_for('deudas'))

# =============================================
# RUTAS DE CALENDARIO MEJORADO
# =============================================

@app.route('/calendario')
@login_required
def calendario():
    """Calendario de sesiones de prácticas"""
    try:
        # Obtener año y mes de los parámetros o usar el actual
        now = datetime.now()
        year = request.args.get('year', now.year, type=int)
        month = request.args.get('month', now.month, type=int)
        
        # Validar año y mes
        if year < 2000 or year > 2100:
            year = now.year
        if month < 1 or month > 12:
            month = now.month
        
        # Generar estructura del calendario
        calendario_data = generar_calendario_mes(year, month)
        
        # Obtener estadísticas adicionales
        reservas_mes = calendario_data['reservas_mes']
        
        # Calcular horas totales reservadas
        horas_totales = 0
        grupos_unicos = set()
        profesores_unicos = set()
        
        for reserva in reservas_mes:
            try:
                horas_totales += int(reserva.get('duracion', 0))
                grupos_unicos.add(reserva.get('grupo', ''))
                profesores_unicos.add(reserva.get('profesor', ''))
            except:
                continue
        
        # Días con reservas
        dias_con_reservas = len(set(r['fecha'] for r in reservas_mes))
        
        # Agregar estadísticas a calendario_data
        calendario_data.update({
            'horas_totales': horas_totales,
            'grupos_unicos': len(grupos_unicos),
            'profesores_unicos': len(profesores_unicos),
            'dias_con_reservas': dias_con_reservas,
            'reservas_por_dia': round(len(reservas_mes) / max(1, calendario_data['dias_laborables']), 1) if calendario_data['dias_laborables'] > 0 else 0
        })
        
        return render_template('calendario.html', **calendario_data)
    
    except Exception as e:
        flash(f'Error cargando el calendario: {str(e)}', 'danger')
        # Cargar calendario actual en caso de error
        now = datetime.now()
        calendario_data = generar_calendario_mes(now.year, now.month)
        return render_template('calendario.html', **calendario_data)

@app.route('/calendario/dia/<fecha>')
@login_required
def calendario_dia(fecha):
    """Ver reservas de un día específico"""
    try:
        # Validar fecha
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        
        # Obtener reservas del día
        reservas = leer_csv(RESERVAS_CSV)
        reservas_dia = [r for r in reservas if r['fecha'] == fecha and r.get('estado') == 'confirmada']
        
        # Ordenar reservas por hora de inicio
        reservas_dia.sort(key=lambda x: x.get('hora_inicio', ''))
        
        # Generar información detallada de horarios
        horarios_detalle = obtener_horarios_detalle(fecha)
        
        # Obtener horarios disponibles para nueva reserva
        horarios_disponibles = obtener_horarios_disponibles(fecha)
        
        # Calcular estadísticas del día
        total_reservas = len(reservas_dia)
        horas_reservadas = sum(int(r.get('duracion', 0)) for r in reservas_dia)
        grupos_dia = set(r.get('grupo', '') for r in reservas_dia)
        materias_dia = set(r.get('materia', '') for r in reservas_dia)
        
        return render_template('calendario_dia.html',
                             fecha=fecha,
                             fecha_obj=fecha_obj,
                             reservas=reservas_dia,
                             horarios_detalle=horarios_detalle,
                             horarios_disponibles=horarios_disponibles,
                             total_reservas=total_reservas,
                             horas_reservadas=horas_reservadas,
                             grupos_dia=len(grupos_dia),
                             materias_dia=len(materias_dia))
    
    except ValueError:
        flash('Fecha inválida', 'danger')
        return redirect(url_for('calendario'))
    except Exception as e:
        flash(f'Error cargando el día: {str(e)}', 'danger')
        return redirect(url_for('calendario'))

@app.route('/calendario/reservar', methods=['POST'])
@login_required
def reservar_sesion():
    """Crear nueva reserva de sesión"""
    try:
        fecha = request.form.get('fecha', '').strip()
        hora_inicio = request.form.get('hora_inicio', '').strip()
        duracion = request.form.get('duracion', '1').strip()
        grupo = request.form.get('grupo', '').strip()
        materia = request.form.get('materia', '').strip()
        profesor = request.form.get('profesor', '').strip()
        num_alumnos = request.form.get('num_alumnos', '').strip()
        observaciones = request.form.get('observaciones', '').strip()
        
        # Validar campos obligatorios
        if not fecha or not hora_inicio or not duracion or not grupo or not materia or not profesor:
            flash('Fecha, hora, duración, grupo, materia y profesor son obligatorios', 'warning')
            return redirect(url_for('calendario_dia', fecha=fecha) if fecha else url_for('calendario'))
        
        # Validar duración
        try:
            duracion_int = int(duracion)
            if duracion_int not in [1, 2]:
                flash('La duración debe ser de 1 o 2 horas', 'danger')
                return redirect(url_for('calendario_dia', fecha=fecha))
        except:
            flash('Duración inválida', 'danger')
            return redirect(url_for('calendario_dia', fecha=fecha))
        
        # Validar número de alumnos
        try:
            num_alumnos_int = int(num_alumnos) if num_alumnos else 0
            if num_alumnos_int < 0:
                flash('El número de alumnos no puede ser negativo', 'danger')
                return redirect(url_for('calendario_dia', fecha=fecha))
        except:
            num_alumnos_int = 0
        
        # Verificar disponibilidad
        disponible, mensaje = verificar_disponibilidad(fecha, hora_inicio, duracion)
        
        if not disponible:
            flash(mensaje, 'danger')
            return redirect(url_for('calendario_dia', fecha=fecha))
        
        # Calcular hora de fin
        try:
            hora_inicio_int = int(hora_inicio.split(':')[0])
            hora_fin_int = hora_inicio_int + duracion_int
            hora_fin = f"{hora_fin_int:02d}:00"
        except:
            flash('Hora de inicio inválida', 'danger')
            return redirect(url_for('calendario_dia', fecha=fecha))
        
        # Crear reserva
        reservas = leer_csv(RESERVAS_CSV)
        
        nueva_reserva = {
            'id_reserva': generar_id(),
            'fecha': fecha,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'duracion': duracion,
            'grupo': grupo,
            'materia': materia,
            'profesor': profesor,
            'num_alumnos': str(num_alumnos_int),
            'observaciones': observaciones,
            'estado': 'confirmada',
            'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'responsable': session.get('nombre', '')
        }
        
        reservas.append(nueva_reserva)
        
        if escribir_csv(RESERVAS_CSV, reservas,
                       ['id_reserva', 'fecha', 'hora_inicio', 'hora_fin', 'duracion',
                        'grupo', 'materia', 'profesor', 'num_alumnos', 'observaciones', 
                        'estado', 'fecha_registro', 'responsable']):
            flash('✅ Sesión reservada correctamente', 'success')
        else:
            flash('Error al reservar la sesión', 'danger')
        
        return redirect(url_for('calendario_dia', fecha=fecha))
    
    except Exception as e:
        flash(f'Error al reservar sesión: {str(e)}', 'danger')
        return redirect(url_for('calendario'))

@app.route('/calendario/cancelar/<id_reserva>')
@login_required
def cancelar_reserva(id_reserva):
    """Cancelar reserva de sesión"""
    try:
        reservas = leer_csv(RESERVAS_CSV)
        encontrada = False
        
        for reserva in reservas:
            if reserva['id_reserva'] == id_reserva:
                reserva['estado'] = 'cancelada'
                encontrada = True
                break
        
        if encontrada:
            if escribir_csv(RESERVAS_CSV, reservas,
                           ['id_reserva', 'fecha', 'hora_inicio', 'hora_fin', 'duracion',
                            'grupo', 'materia', 'profesor', 'num_alumnos', 'observaciones', 
                            'estado', 'fecha_registro', 'responsable']):
                flash('✅ Reserva cancelada correctamente', 'success')
            else:
                flash('Error al cancelar la reserva', 'danger')
        else:
            flash('Reserva no encontrada', 'danger')
        
        # Redirigir a la página anterior
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        else:
            return redirect(url_for('calendario'))
    
    except Exception as e:
        flash(f'Error al cancelar reserva: {str(e)}', 'danger')
        return redirect(url_for('calendario'))

@app.route('/calendario/eliminar/<id_reserva>')
@login_required
@admin_required
def eliminar_reserva(id_reserva):
    """Eliminar reserva permanentemente"""
    try:
        reservas = leer_csv(RESERVAS_CSV)
        reservas_filtradas = [r for r in reservas if r['id_reserva'] != id_reserva]
        
        if len(reservas_filtradas) < len(reservas):
            if escribir_csv(RESERVAS_CSV, reservas_filtradas,
                           ['id_reserva', 'fecha', 'hora_inicio', 'hora_fin', 'duracion',
                            'grupo', 'materia', 'profesor', 'num_alumnos', 'observaciones', 
                            'estado', 'fecha_registro', 'responsable']):
                flash('✅ Reserva eliminada correctamente', 'success')
            else:
                flash('Error al eliminar la reserva', 'danger')
        else:
            flash('Reserva no encontrada', 'danger')
        
        # Redirigir a la página anterior
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        else:
            return redirect(url_for('calendario'))
    
    except Exception as e:
        flash(f'Error al eliminar reserva: {str(e)}', 'danger')
        return redirect(url_for('calendario'))

# =============================================
# RUTAS ADICIONALES
# =============================================

@app.route('/reportes')
@login_required
def reportes():
    """Página de reportes"""
    try:
        # Obtener datos para reportes
        inventario = leer_csv(INVENTARIO_CSV)
        prestamos = leer_csv(PRESTAMOS_CSV)
        alumnos = leer_csv(ALUMNOS_CSV)
        deudas = leer_csv(DEUDAS_CSV)
        reservas = leer_csv(RESERVAS_CSV)
        
        # Estadísticas generales
        total_items = len(inventario)
        total_prestamos = len(prestamos)
        total_alumnos = len(alumnos)
        total_deudas = len(deudas)
        total_reservas = len([r for r in reservas if r.get('estado') == 'confirmada'])
        
        # Inventario por categoría
        categorias = {}
        for item in inventario:
            cat = item.get('categoria', 'Sin categoría')
            if cat not in categorias:
                categorias[cat] = 0
            categorias[cat] += 1
        
        # Préstamos por mes (últimos 6 meses)
        prestamos_por_mes = {}
        hoy = datetime.now()
        for i in range(6):
            fecha = hoy - timedelta(days=30*i)
            mes_key = fecha.strftime('%Y-%m')
            prestamos_por_mes[mes_key] = 0
        
        for prestamo in prestamos:
            try:
                fecha = datetime.strptime(prestamo['fecha_prestamo'][:7], '%Y-%m')
                mes_key = fecha.strftime('%Y-%m')
                if mes_key in prestamos_por_mes:
                    prestamos_por_mes[mes_key] += 1
            except:
                pass
        
        # Alumnos por grupo
        alumnos_por_grupo = {}
        for alumno in alumnos:
            grupo = alumno.get('grupo', 'Sin grupo')
            if grupo not in alumnos_por_grupo:
                alumnos_por_grupo[grupo] = 0
            alumnos_por_grupo[grupo] += 1
        
        # Reservas por mes (últimos 6 meses)
        reservas_por_mes = {}
        for i in range(6):
            fecha = hoy - timedelta(days=30*i)
            mes_key = fecha.strftime('%Y-%m')
            reservas_por_mes[mes_key] = 0
        
        for reserva in reservas:
            try:
                if reserva.get('estado') == 'confirmada':
                    mes_key = reserva['fecha'][:7]
                    if mes_key in reservas_por_mes:
                        reservas_por_mes[mes_key] += 1
            except:
                pass
        
        # Convertir a listas para el template
        categorias_list = [{'categoria': k, 'cantidad': v} for k, v in categorias.items()]
        prestamos_mes_list = [{'mes': k, 'cantidad': v} for k, v in sorted(prestamos_por_mes.items())]
        grupos_list = [{'grupo': k, 'cantidad': v} for k, v in alumnos_por_grupo.items()]
        reservas_mes_list = [{'mes': k, 'cantidad': v} for k, v in sorted(reservas_por_mes.items())]
        
        return render_template('reportes.html',
                             total_items=total_items,
                             total_prestamos=total_prestamos,
                             total_alumnos=total_alumnos,
                             total_deudas=total_deudas,
                             total_reservas=total_reservas,
                             categorias=categorias_list,
                             prestamos_mes=prestamos_mes_list,
                             grupos=grupos_list,
                             reservas_mes=reservas_mes_list,
                             today=hoy.strftime('%Y-%m-%d'))
    
    except Exception as e:
        flash(f'Error generando reportes: {str(e)}', 'danger')
        return render_template('reportes.html',
                             total_items=0,
                             total_prestamos=0,
                             total_alumnos=0,
                             total_deudas=0,
                             total_reservas=0,
                             categorias=[],
                             prestamos_mes=[],
                             grupos=[],
                             reservas_mes=[],
                             today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/configuracion')
@login_required
@admin_required
def configuracion():
    """Página de configuración del sistema"""
    return render_template('configuracion.html')

@app.route('/backup')
@login_required
@admin_required
def backup():
    """Crear copia de seguridad"""
    try:
        # Crear directorio de backups si no existe
        backup_dir = os.path.join(BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nombre del archivo de backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.zip')
        
        # Importar módulo de zip
        import zipfile
        
        # Crear archivo zip
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Agregar archivos CSV
            csv_files = [USUARIOS_CSV, INVENTARIO_CSV, PRESTAMOS_CSV, 
                        ALUMNOS_CSV, DEUDAS_CSV, RESERVAS_CSV]
            
            for csv_file in csv_files:
                if os.path.exists(csv_file):
                    zipf.write(csv_file, os.path.basename(csv_file))
        
        # Obtener lista de backups
        backups = []
        for file in os.listdir(backup_dir):
            if file.startswith('backup_') and file.endswith('.zip'):
                filepath = os.path.join(backup_dir, file)
                stat = os.stat(filepath)
                backups.append({
                    'nombre': file,
                    'tamaño': f"{stat.st_size / 1024:.1f} KB",
                    'fecha': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x['fecha'], reverse=True)
        
        flash(f'✅ Copia de seguridad creada correctamente: {os.path.basename(backup_file)}', 'success')
        return render_template('backup.html', backups=backups[:10])  # Mostrar solo los 10 más recientes
    
    except Exception as e:
        flash(f'Error creando backup: {str(e)}', 'danger')
        return render_template('backup.html', backups=[])

# =============================================
# ERROR HANDLERS
# =============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================

if __name__ == '__main__':
    # Inicializar archivos CSV
    inicializar_csv()
    
    # Configuración de la aplicación
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5005))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Mostrar información de inicio
    print("=" * 70)
    print("🔬 XONILAB - Sistema de Gestión de Laboratorio")
    print("=" * 70)
    print("  Sistema completo para la gestión de laboratorios educativos")
    print()
    print("👤 INFORMACIÓN DEL DESARROLLADOR:")
    print("  Nombre: Darian Alberto Camacho Salas")
    print("  Contacto: xonidu@gmail.com")
    print("  Laboratorio de Ciencias")
    print()
    print("🚀 INICIANDO SISTEMA...")
    print(f"  URL: http://{host}:{port}")
    print(f"  Modo debug: {debug}")
    print()
    print("🔐 CREDENCIALES DE ACCESO:")
    print("  Usuario: XONILAB")
    print("  Contraseña: laboratorio")
    print("=" * 70)
    
    # Iniciar servidor
    app.run(host=host, port=port, debug=debug)
