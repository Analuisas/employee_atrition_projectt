import os
import subprocess

def setup_environment():
    print("🔧 Criando ambiente virtual...")
    subprocess.run(["python3", "-m", "venv", "venv"])

    print("📦 Instalando bibliotecas do requirements.txt...")
    subprocess.run(["venv/bin/pip", "install", "-r", "requirements.txt"])

    print("\n✅ Ambiente configurado com sucesso!")
    print("Para ativar o ambiente, use:")
    print("   source venv/bin/activate  (Linux/macOS)")
    print("Ou no Windows:")
    print("   venv\\Scripts\\activate")

if __name__ == "__main__":
    setup_environment()
