import subprocess
import sys

# Função para rodar outro script Python
def run_script(script_name):
    print(f"Rodando {script_name}...")
    result = subprocess.run([sys.executable, script_name])
    if result.returncode != 0:
        print(f"Erro ao rodar {script_name}")
        sys.exit(1)  # para caso dê erro

# Roda na ordem certa
run_script("installer.py")
run_script("app.py")
