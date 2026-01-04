import os
import sys
import platform
import subprocess
import zipfile
import urllib.request
from pathlib import Path

def instalar_ytdlp():
    """Instala yt-dlp via pip"""
    print("Instalando yt-dlp...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("✓ yt-dlp instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar yt-dlp: {e}")
        return False

def verificar_ffmpeg():
    """Verifica se ffmpeg já está no PATH"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✓ ffmpeg já está instalado e no PATH!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def instalar_ffmpeg_windows():
    """Instala ffmpeg no Windows"""
    print("Instalando ffmpeg no Windows...")
    
    # Diretório de instalação
    install_dir = Path.home() / "ffmpeg"
    install_dir.mkdir(exist_ok=True)
    
    # URL do ffmpeg (versão essentials)
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = install_dir / "ffmpeg.zip"
    
    try:
        print("Baixando ffmpeg...")
        urllib.request.urlretrieve(ffmpeg_url, zip_path)
        
        print("Extraindo arquivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Encontrar a pasta bin
        bin_path = None
        for item in install_dir.rglob("bin"):
            if item.is_dir():
                bin_path = item
                break
        
        if not bin_path:
            print("✗ Não foi possível encontrar a pasta bin do ffmpeg")
            return False
        
        # Adicionar ao PATH do sistema
        print("Adicionando ao PATH do sistema...")
        
        # Usar setx para adicionar permanentemente ao PATH do usuário
        current_path = os.environ.get('PATH', '')
        if str(bin_path) not in current_path:
            subprocess.run(['setx', 'PATH', f"{current_path};{bin_path}"], check=True)
            # Atualizar PATH da sessão atual
            os.environ['PATH'] = f"{current_path};{bin_path}"
        
        # Limpar arquivo zip
        zip_path.unlink()
        
        print(f"✓ ffmpeg instalado em: {bin_path}")
        print("✓ ffmpeg adicionado ao PATH!")
        print("\n⚠ IMPORTANTE: Reinicie o terminal/IDE para que as mudanças no PATH tenham efeito.")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao instalar ffmpeg: {e}")
        return False

def instalar_ffmpeg_linux():
    """Instala ffmpeg no Linux"""
    print("Instalando ffmpeg no Linux...")
    
    try:
        # Tentar com apt (Debian/Ubuntu)
        if subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
            print("Usando apt para instalar...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
        
        # Tentar com yum (CentOS/RHEL)
        elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
            print("Usando yum para instalar...")
            subprocess.run(["sudo", "yum", "install", "-y", "ffmpeg"], check=True)
        
        # Tentar com dnf (Fedora)
        elif subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
            print("Usando dnf para instalar...")
            subprocess.run(["sudo", "dnf", "install", "-y", "ffmpeg"], check=True)
        
        else:
            print("✗ Gerenciador de pacotes não suportado.")
            print("Por favor, instale ffmpeg manualmente para sua distribuição.")
            return False
        
        print("✓ ffmpeg instalado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar ffmpeg: {e}")
        return False

def instalar_ffmpeg_mac():
    """Instala ffmpeg no macOS"""
    print("Instalando ffmpeg no macOS...")
    
    try:
        # Verificar se Homebrew está instalado
        if subprocess.run(["which", "brew"], capture_output=True).returncode != 0:
            print("Homebrew não encontrado. Instalando Homebrew...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(install_cmd, shell=True, check=True)
        
        print("Instalando ffmpeg via Homebrew...")
        subprocess.run(["brew", "install", "ffmpeg"], check=True)
        print("✓ ffmpeg instalado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar ffmpeg: {e}")
        return False

def instalar_dependencias():
    """Função principal para instalar todas as dependências"""
    print("=" * 50)
    print("Instalador de ffmpeg e yt-dlp")
    print("=" * 50)
    print()
    
    sistema = platform.system()
    print(f"Sistema operacional detectado: {sistema}")
    print()
    
    # Instalar yt-dlp
    ytdlp_ok = instalar_ytdlp()
    print()
    
    # Verificar e instalar ffmpeg
    if verificar_ffmpeg():
        ffmpeg_ok = True
    else:
        print("ffmpeg não encontrado. Iniciando instalação...")
        
        if sistema == "Windows":
            ffmpeg_ok = instalar_ffmpeg_windows()
        elif sistema == "Linux":
            ffmpeg_ok = instalar_ffmpeg_linux()
        elif sistema == "Darwin":  # macOS
            ffmpeg_ok = instalar_ffmpeg_mac()
        else:
            print(f"✗ Sistema operacional '{sistema}' não suportado.")
            ffmpeg_ok = False
    
    print()
    print("=" * 50)
    print("Resumo da instalação:")
    print(f"  yt-dlp: {'✓ OK' if ytdlp_ok else '✗ FALHOU'}")
    print(f"  ffmpeg: {'✓ OK' if ffmpeg_ok else '✗ FALHOU'}")
    print("=" * 50)
    
    return ytdlp_ok and ffmpeg_ok

if __name__ == "__main__":
    sucesso = instalar_dependencias()
    sys.exit(0 if sucesso else 1)