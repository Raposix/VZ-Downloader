import subprocess
import sys
import re
import time
import os
from datetime import date
import tkinter as tk
from tkinter import filedialog

# ================= ESTÉTICA =================

parrot_frames = [
    "🦜  ♪┏(・o･)┛♪",
    "🦜  ♪┗(・o･)┓♪",
]

rgb_colors = [
    "\033[91m",
    "\033[93m",
    "\033[92m",
    "\033[96m",
    "\033[94m",
    "\033[95m",
]

RESET = "\033[0m"
BAR_LEN = 30

def desenhar_barra(percent, frame):
    filled = int(percent / 100 * BAR_LEN)
    bar = "█" * filled + " " * (BAR_LEN - filled)
    color = rgb_colors[frame % len(rgb_colors)]
    parrot = parrot_frames[frame % len(parrot_frames)]

    sys.stdout.write(
        f"\r{color}[{bar}]{RESET} {percent:5.1f}% {parrot}"
    )
    sys.stdout.flush()

# ============================================

def nome_disponivel(caminho):
    if not os.path.exists(caminho):
        return caminho

    base, ext = os.path.splitext(caminho)
    i = 1
    while True:
        novo = f"{base} ({i}){ext}"
        if not os.path.exists(novo):
            return novo
        i += 1

# ============================================

hoje = date.today()
print("Bem-Vindo ao VZDownloader! O seu downloader de vídeos do YouTube.")

if (hoje.day == 31 and hoje.month == 12) or (hoje.day == 1 and hoje.month == 1):
    print("🎉 HAPPY NEW YEAR!")

if hoje.day == 25 and hoje.month == 12:
    print("🎅 MERRY CHRISTMAS!")

print("se precisar de ajuda, digite (?)")

print("\nFormatos disponíveis:")
print("1. MP4")
print("2. MP3")
print("3. MOV")
print("4. AVI")
print("5. Outros")

opcao = input("Escolha uma opção (1-5): ")

# Verificar se é devinfo
if opcao.lower() == "devinfo":
    # ASCII art colorido
    cores = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
    ascii_art = r"""
____________  _______   __ ______ _____ _   _ 
| ___ \ ___ \/  ___\ \ / / |  _  \  ___| | | |
| |_/ / |_/ /\ `--. \ V /  | | | | |__ | | | |
|    /|  __/  `--. \/   \  | | | |  __|| | | |
| |\ \| |    /\__/ / /^\ \ | |/ /| |___\ \_/ /
\_| \_\_|    \____/\/   \/ |___/ \____/ \___/  
    """
    
    linhas = ascii_art.split('\n')
    for i, linha in enumerate(linhas):
        cor = cores[i % len(cores)]
        print(f"{cor}{linha}{RESET}")
    
    print("\n" + "="*70)
    print("VZDownloader Legacy - Release 1.1 (01/01/2026)")
    print("="*70)
    print("\nDesenvolvido por: @raposix on yt")
    print("GitHub: Raposix")
    print("Descrição: Downloader de vídeos do YouTube com interface em cmd")
    print("\nTecnologias: Python, yt-dlp, tkinter")
    print("="*70)
    input("\nPressione ENTER para continuar...")
    sys.exit()

    

url = input("Cole a URL do vídeo do YouTube: ")

# ===== SELETOR DE PASTA =====
root = tk.Tk()
root.withdraw()

pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
if not pasta:
    print("Nenhuma pasta selecionada. Encerrando.")
    input("\nPressione ENTER para sair...")
    sys.exit()

# ===== NOME DO ARQUIVO =====
nome_arquivo = filedialog.asksaveasfilename(
    title="Escolha o nome do arquivo",
    initialdir=pasta,
    defaultextension="",
    filetypes=[("Todos os arquivos", "*.*")]
)

if not nome_arquivo:
    print("Nenhum nome escolhido. Encerrando.")
    input("\nPressione ENTER para sair...")
    sys.exit()

# ============================================

if opcao == "1":
    ext = ".mp4"
    formato_cmd = ['-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]']

elif opcao == "2":
    ext = ".mp3"
    formato_cmd = ['-x', '--audio-format', 'mp3']

elif opcao == "3":
    ext = ".mov"
    formato_cmd = ['--recode-video', 'mov']

elif opcao == "4":
    ext = ".avi"
    formato_cmd = ['--recode-video', 'avi']

elif opcao == "5":
    ext = input("Digite a extensão desejada (ex: mkv, wav): ")
    if not ext.startswith("."):
        ext = "." + ext
    formato_cmd = ['--recode-video', ext.replace(".", "")]

elif opcao == "?":
    print("Como usar o programa?")
    print("Primeiro, digite o número correspondente ao formato de vídeo que queira baixar")
    print("Depois, insira a URL do vídeo que queira baixar no seu pc")
    print("Logo depois, selecione a pasta que queira baixar o vídeo e o nome do arquivo")
    print("Pronto! Vídeo baixado com sucesso!")

input("\nPressione ENTER para sair...")
sys.exit()

else:
    print("Opção inválida.")
    input("\nPressione ENTER para sair...")
    sys.exit()

# garante extensão
if not nome_arquivo.endswith(ext):
    nome_arquivo += ext

nome_final = nome_disponivel(nome_arquivo)

output = ['-o', nome_final]

# ============================================

cmd = [
    "yt-dlp",
    "--newline",
    "--progress-template",
    "%(progress._percent_str)s",
    *formato_cmd,
    *output,
    url
]

print("\nIniciando download...\n")

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)

frame = 0

for line in process.stdout:
    match = re.search(r"(\d+\.?\d*)%", line)
    if match:
        percent = float(match.group(1))
        desenhar_barra(percent, frame)
        frame += 1
        time.sleep(0.05)

process.wait()
print("\n\n✅ Download finalizado com sucesso!")
print(f"📁 Arquivo salvo em:\n{nome_final}")
print("Obrigado por usar o VZDownloader! Volte sempre! 😊")

# Pausa para manter o terminal aberto

input("\n🔵 Pressione ENTER para fechar...")
