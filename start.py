#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONILAB 2026 - Lanzador Universal
Este script detecta el sistema, instala dependencias y ejecuta xonilab.py
Genera un archivo .bat en Windows para ejecutar con permisos de administrador
Desarrollado por: Darian Alberto Camacho Salas
"""

import subprocess
import sys
import os
import webbrowser
import time
import platform
import threading
import ctypes

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

# Desactivar colores si no hay soporte
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# Dependencias necesarias para XONILAB
REQUISITOS = [
    'Flask==2.3.3',
    'qrcode==7.4.2',
    'pillow==10.0.1',
    'Werkzeug==2.3.7',
    'Jinja2==3.1.2',
    'itsdangerous==2.1.2',
    'click==8.1.7',
    'MarkupSafe==2.1.3'
]

def is_admin():
    """Verifica si el script se ejecuta como administrador en Windows"""
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_python_command():
    """Obtiene el comando Python correcto según el sistema"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    """Obtiene el comando pip correcto según el sistema"""
    if get_system() == 'windows':
        return [sys.executable, '-m', 'pip']
    else:
        return [sys.executable, '-m', 'pip']

def get_install_flags():
    """Obtiene los flags de instalación según el sistema"""
    flags = []
    if get_system() == 'darwin':
        flags.append('--user')
    return flags

def print_banner():
    """Muestra el banner de XONILAB"""
    sistema = get_system()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                     XONILAB 2026 v3.0                      ║
║              Sistema de Gestion de Laboratorio              ║
║                                                            ║
║               Sistema detectado: {sistema_texto}            ║
║                                                            ║
║               Desarrollado por: Darian Alberto               ║
║                      Camacho Salas                           ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica que Python esta instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    """Verifica que pip esta instalado y funciona"""
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_windows():
    """Instala pip en Windows si no esta disponible"""
    print(f"{Colors.YELLOW}Pip no encontrado. Instalando pip...{Colors.END}")
    try:
        import urllib.request
        print("  Descargando get-pip.py...")
        urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')
        
        print("  Instalando pip...")
        subprocess.run([sys.executable, 'get-pip.py'], check=True)
        
        os.remove('get-pip.py')
        
        print(f"{Colors.GREEN}  Pip instalado correctamente{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}  Error instalando pip: {e}{Colors.END}")
        return False

def check_dependencies():
    """Verifica que dependencias necesita XONILAB"""
    print(f"\n{Colors.BOLD}Verificando dependencias para XONILAB...{Colors.END}")
    
    missing = []
    for req in REQUISITOS:
        package = req.split('==')[0].lower()
        try:
            if package == 'flask':
                __import__('flask')
            elif package == 'werkzeug':
                __import__('werkzeug')
            elif package == 'jinja2':
                __import__('jinja2')
            elif package == 'click':
                __import__('click')
            elif package == 'markupsafe':
                __import__('markupsafe')
            elif package == 'itsdangerous':
                __import__('itsdangerous')
            elif package == 'qrcode':
                __import__('qrcode')
            elif package == 'pillow':
                __import__('PIL')
            else:
                __import__(package)
            print(f"{Colors.GREEN}  - {req.split('==')[0]} OK{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  - {req.split('==')[0]} (faltante){Colors.END}")
            missing.append(req)
    
    return missing

def install_dependencies(missing):
    """Instala las dependencias faltantes"""
    if not missing:
        print(f"\n{Colors.GREEN}Todas las dependencias estan instaladas{Colors.END}")
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    pip_cmd = get_pip_command()
    flags = get_install_flags()
    
    if flags:
        print(f"{Colors.YELLOW}Flags: {' '.join(flags)}{Colors.END}")
    
    success = True
    for req in missing:
        print(f"  Instalando {req}...")
        try:
            cmd = pip_cmd + ['install', req] + flags
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"{Colors.GREEN}  - {req} instalado{Colors.END}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}  Error instalando {req}{Colors.END}")
            # Intentar sin flags
            try:
                print(f"  Intentando sin flags...")
                cmd = pip_cmd + ['install', req]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"{Colors.GREEN}  - {req} instalado (sin flags){Colors.END}")
            except:
                print(f"     {e}")
                success = False
    
    if success:
        print(f"\n{Colors.GREEN}Todas las dependencias instaladas correctamente{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}Algunas dependencias no se instalaron{Colors.END}")
    
    return success

def open_browser():
    """Abre el navegador despues de unos segundos"""
    time.sleep(3)
    url = 'http://localhost:5005'
    try:
        webbrowser.open(url)
        print(f"{Colors.GREEN}Navegador abierto en {url}{Colors.END}")
    except:
        print(f"{Colors.YELLOW}No se pudo abrir el navegador automaticamente{Colors.END}")
        print(f"   Abre manualmente: {url}")

def create_windows_bat():
    """Crea archivos .bat para Windows"""
    sistema = get_system()
    if sistema != 'windows':
        return
    
    # Archivo con permisos de administrador
    admin_bat_content = '''@echo off
title XONILAB 2026 - Sistema de Gestion de Laboratorio
color 0A
cls

echo ========================================
echo      XONILAB 2026 - Gestion de Laboratorio
echo      Desarrollado por Darian Alberto
echo ========================================
echo.

:: Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Se requieren permisos de administrador para instalar dependencias
    echo.
    echo Solicitando permisos...
    echo.
    
    :: Crear script temporal para ejecutar con admin
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\\getadmin.vbs"
    "%temp%\\getadmin.vbs"
    del "%temp%\\getadmin.vbs"
    exit /B
)

echo [OK] Permisos de administrador obtenidos
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo IMPORTANTE: Marca "Add Python to PATH" durante la instalacion
    echo.
    pause
    start https://www.python.org/downloads/
    exit
)

echo [OK] Python instalado
python --version
echo.

:: Verificar pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Pip no encontrado. Instalando pip...
    python -m ensurepip --upgrade
)

echo [OK] Pip disponible
echo.

:: Instalar dependencias
echo Instalando dependencias necesarias...
echo.

python -m pip install Flask==2.3.3
python -m pip install qrcode==7.4.2
python -m pip install pillow==10.0.1
python -m pip install Werkzeug==2.3.7
python -m pip install Jinja2==3.1.2
python -m pip install itsdangerous==2.1.2
python -m pip install click==8.1.7
python -m pip install MarkupSafe==2.1.3

echo.
echo [OK] Dependencias instaladas
echo.

:: Crear carpetas necesarias
if not exist "data" mkdir data
if not exist "static\\qrcodes" mkdir static\\qrcodes
if not exist "backups" mkdir backups

:: Iniciar XONILAB
echo ========================================
echo Iniciando XONILAB...
echo ========================================
echo.
echo Accede desde: http://localhost:5005
echo Usuario: XONILAB
echo Contrasena: laboratorio
echo.
echo Para detener el servidor presiona Ctrl+C
echo ========================================
echo.

start http://localhost:5005
python xonilab.py

pause
'''
    
    admin_bat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'XONILAB_ADMIN.bat')
    with open(admin_bat_path, 'w', encoding='utf-8') as f:
        f.write(admin_bat_content)
    print(f"{Colors.GREEN}Archivo XONILAB_ADMIN.bat creado - Ejecuta como administrador si hay problemas{Colors.END}")
    
    # Archivo simple sin admin
    simple_bat = '''@echo off
title XONILAB 2026
color 0A
echo ========================================
echo      XONILAB 2026 - Gestion de Laboratorio
echo ========================================
echo.
echo Iniciando XONILAB...
echo.
echo Accede desde: http://localhost:5005
echo Usuario: XONILAB
echo Contrasena: laboratorio
echo.
echo Para detener presiona Ctrl+C
echo ========================================
echo.
start http://localhost:5005
python xonilab.py
pause
'''
    simple_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'XONILAB.bat')
    with open(simple_path, 'w', encoding='utf-8') as f:
        f.write(simple_bat)
    print(f"{Colors.GREEN}Archivo XONILAB.bat creado - Doble clic para ejecutar{Colors.END}")

def ensure_directories():
    """Asegura que existen las carpetas necesarias"""
    directories = ['data', 'static/qrcodes', 'backups']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print(f"{Colors.GREEN}Carpetas necesarias creadas/verificadas{Colors.END}")

def mostrar_instrucciones_python():
    """Muestra instrucciones para instalar Python segun el sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        print(f"   Descarga Python desde: https://www.python.org/downloads/")
        print(f"   IMPORTANTE: Al instalar, marca 'Add Python to PATH'")
    elif sistema == 'linux':
        print(f"   Instala con: sudo apt install python3 python3-pip")
    elif sistema == 'darwin':
        print(f"   Instala con: brew install python3")

def main():
    """Funcion principal - Ejecuta XONILAB"""
    # Limpiar pantalla segun sistema
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    sistema = get_system()
    
    print(f"{Colors.BOLD}Sistema operativo:{Colors.END} {sistema}")
    print(f"{Colors.BOLD}Python:{Colors.END} {sys.version.split()[0]}")
    print(f"{Colors.BOLD}Ruta:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Crear archivos .bat solo para Windows
    if sistema == 'windows':
        create_windows_bat()
        print()
    
    # Verificar que Python esta instalado
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado o no esta en el PATH{Colors.END}")
        mostrar_instrucciones_python()
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar pip en Windows e instalarlo si es necesario
    if sistema == 'windows' and not check_pip():
        print(f"\n{Colors.YELLOW}Pip no encontrado. Intentando instalar...{Colors.END}")
        if not install_pip_windows():
            print(f"\n{Colors.RED}No se pudo instalar pip automaticamente{Colors.END}")
            print(f"   Ejecuta XONILAB_ADMIN.bat como administrador")
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
            return
    
    # Verificar dependencias
    missing = check_dependencies()
    
    # Instalar dependencias si faltan
    if missing:
        print(f"\n{Colors.YELLOW}Faltan {len(missing)} dependencias{Colors.END}")
        
        # En Windows, sugerir usar el .bat con admin
        if sistema == 'windows':
            print(f"\n{Colors.YELLOW}Se recomienda ejecutar XONILAB_ADMIN.bat como administrador{Colors.END}")
            print(f"   para instalar las dependencias automaticamente")
            respuesta = input(f"Intentar instalar ahora? (s/n): ")
        else:
            respuesta = input(f"Instalar ahora? (s/n): ")
        
        if respuesta.lower() == 's':
            if not install_dependencies(missing):
                print(f"\n{Colors.YELLOW}Continuando a pesar de errores...{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}No se instalaran dependencias. Puede haber errores.{Colors.END}")
            if sistema == 'windows':
                print(f"   Ejecuta XONILAB_ADMIN.bat como administrador para instalarlas")
    
    # Crear carpetas necesarias
    ensure_directories()
    
    # Verificar que existe xonilab.py
    if not os.path.exists('xonilab.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonilab.py{Colors.END}")
        print(f"   Asegurate de que xonilab.py esta en la misma carpeta")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}Iniciando XONILAB (Sistema de Gestion de Laboratorio)...{Colors.END}")
    print(f"{Colors.BOLD}Credenciales:{Colors.END} Usuario: XONILAB | Contrasena: laboratorio")
    
    # Hilo para abrir el navegador
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Ejecutar xonilab.py
    try:
        python_cmd = get_python_command()
        print(f"{Colors.BOLD}Ejecutando:{Colors.END} {' '.join(python_cmd + ['xonilab.py'])}")
        print(f"{Colors.BOLD}Servidor:{Colors.END} http://localhost:5005")
        print(f"{Colors.BOLD}Para detener:{Colors.END} Ctrl+C")
        print("-" * 60)
        
        subprocess.run(python_cmd + ['xonilab.py'])
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Servidor detenido por el usuario{Colors.END}")
    except FileNotFoundError as e:
        print(f"\n{Colors.RED}Error: No se encuentra Python o xonilab.py{Colors.END}")
        print(f"   {e}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonilab.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONILAB 2026{Colors.END}")
    if sistema != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
