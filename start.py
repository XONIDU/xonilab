#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONILAB - Sistema de Gestión de Laboratorio
Este script ejecuta xonilab.py y verifica dependencias
Desarrollado por: Darian Alberto Camacho Salas
#Somos XONINDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util
import webbrowser
import time

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

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribucion de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def print_banner():
    """Muestra el banner de XONILAB"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONILAB v3.0                    
              Sistema de Gestión de Laboratorio            
              Inventario • Préstamos • Alumnos                
              Deudas • Calendario • Reportes
              Códigos QR • Backups
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONINDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_command(comando):
    """Verifica si un comando existe"""
    return shutil.which(comando) is not None

def check_python_module(module_name):
    """Verifica si un modulo de Python esta instalado"""
    return importlib.util.find_spec(module_name) is not None

def check_dependencies():
    """Verifica las dependencias de Python necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    dependencias = [
        ('flask', 'flask', 'Framework web', 'flask'),
        ('qrcode', 'qrcode[pil]', 'Códigos QR', 'qrcode'),
        ('pillow', 'pillow', 'Imágenes', 'PIL'),
    ]
    
    faltantes = []
    
    for modulo, paquete, desc, import_name in dependencias:
        if check_python_module(import_name):
            print(f"{Colors.GREEN}  - {modulo}: OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  - {modulo}: FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    if sistema == 'windows':
        # Windows - instalación normal
        cmd = [sys.executable, '-m', 'pip', 'install'] + faltantes
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            return False
    
    elif sistema == 'darwin':
        # macOS - usar --user
        cmd = [sys.executable, '-m', 'pip', 'install', '--user'] + faltantes
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
            return True
        except:
            print(f"{Colors.RED}Error instalando dependencias{Colors.END}")
            return False
    
    else:
        # Linux - intentar con --break-system-packages si es Arch
        if distro in ['arch', 'manjaro', 'fedora']:
            cmd = [sys.executable, '-m', 'pip', 'install', '--break-system-packages'] + faltantes
            try:
                print(f"Ejecutando: {' '.join(cmd)}")
                subprocess.run(cmd, check=True)
                print(f"{Colors.GREEN}Dependencias instaladas correctamente (--break-system-packages){Colors.END}")
                return True
            except:
                pass
        
        # Segundo intento: --user
        try:
            cmd = [sys.executable, '-m', 'pip', 'install', '--user'] + faltantes
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente (--user){Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\nInstala manualmente:")
            print(f"  pip install {' '.join(faltantes)}")
            if distro in ['arch', 'manjaro']:
                print(f"  pip install --break-system-packages {' '.join(faltantes)}")
            return False

def verificar_importaciones():
    """Verifica que todas las importaciones necesarias funcionen"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    modulos = [
        ('flask', 'Flask'),
        ('qrcode', 'qrcode'),
        ('PIL', 'Pillow'),
    ]
    
    todos_ok = True
    for modulo, nombre in modulos:
        try:
            __import__(modulo)
            print(f"{Colors.GREEN}  - {nombre}: OK{Colors.END}")
        except ImportError as e:
            print(f"{Colors.RED}  - {nombre}: FALLO - {e}{Colors.END}")
            todos_ok = False
    
    return todos_ok

def crear_directorios():
    """Crea los directorios necesarios"""
    directorios = ['data', 'static/qrcodes', 'backups', 'templates']
    
    for dir_path in directorios:
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_path)
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
                print(f"{Colors.GREEN}Creado directorio: {dir_path}{Colors.END}")
            except:
                print(f"{Colors.YELLOW}No se pudo crear: {dir_path}{Colors.END}")

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONILAB.bat', 'w') as f:
            f.write("""@echo off
title XONILAB - Sistema de Gestion de Laboratorio
color 1F
echo ========================================
echo      XONILAB v3.0
echo      Sistema de Gestion de Laboratorio
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONILAB.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONILAB.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONILAB v3.0"
echo "      Sistema de Gestion de Laboratorio"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONILAB.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONILAB.sh - Ejecuta con: ./INICIAR_XONILAB.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONILAB.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONILAB v3.0"
echo "      Sistema de Gestion de Laboratorio"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONILAB.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONILAB.command - Haz doble clic para ejecutar{Colors.END}")

def mostrar_credenciales():
    """Muestra las credenciales de acceso"""
    credenciales = f"""
{Colors.BOLD}╔════════════════════════════════════════╗
║      CREDENCIALES DE ACCESO          ║
╠════════════════════════════════════════╣
║  Usuario: {Colors.GREEN}XONILAB{Colors.END}                     ║
║  Contraseña: {Colors.GREEN}laboratorio{Colors.END}                ║
║                                        ║
║  URL: {Colors.BLUE}http://localhost:5005{Colors.END}           ║
╚════════════════════════════════════════╝{Colors.END}
    """
    print(credenciales)

def abrir_navegador():
    """Abre el navegador después de 3 segundos"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:5005')
        print(f"{Colors.GREEN}Navegador abierto en http://localhost:5005{Colors.END}")
    except:
        print(f"{Colors.YELLOW}No se pudo abrir el navegador automáticamente{Colors.END}")

def main():
    """Funcion principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Crear directorios necesarios
    crear_directorios()
    
    # Verificar que existe xonilab.py
    if not os.path.exists('xonilab.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonilab.py{Colors.END}")
        print("Asegurate de que xonilab.py esta en el mismo directorio")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}Faltan dependencias: {', '.join(faltantes)}{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            if not install_dependencies(faltantes):
                print(f"\n{Colors.RED}No se pudieron instalar las dependencias{Colors.END}")
                print("Puedes instalarlas manualmente con:")
                print(f"  pip install {' '.join(faltantes)}")
                input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.END}")
    else:
        print(f"{Colors.GREEN}Todas las dependencias estan instaladas{Colors.END}")
    
    # Verificar que las importaciones funcionan
    if not verificar_importaciones():
        print(f"\n{Colors.RED}Error: No se pueden importar los módulos necesarios{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Mostrar credenciales
    mostrar_credenciales()
    
    print(f"\n{Colors.BOLD}Iniciando XONILAB...{Colors.END}")
    print(f"{Colors.BOLD}Servidor web en: {Colors.BLUE}http://localhost:5005{Colors.END}")
    print(f"{Colors.BOLD}Para detener el servidor:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # EJECUTAR xonilab.py
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonilab.py']
        
        # Abrir navegador automáticamente después de 3 segundos
        import threading
        threading.Thread(target=abrir_navegador, daemon=True).start()
        
        # Ejecutar xonilab.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonilab.py termino con codigo {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonilab.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Servidor detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonilab.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONILAB{Colors.END}")
    print(f"{Colors.BLUE}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.BLUE}#Somos XONINDU{Colors.END}")
    
    # Pausa al final
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
