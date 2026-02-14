import paramiko
import time
import sys

HOST = "187.77.37.72"
USER = "root"
PASS = "1763kovQ@123"

def setup_server():
    print(f"-> Conectando em {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, username=USER, password=PASS)
        print("[OK] Conectado com sucesso!")
        
        # Função para executar e mostrar output
        def run(cmd, name):
            print(f"\n[EXEC] {name}...")
            print(f"   Comando: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            
            # Streaming de output
            while True:
                line = stdout.readline()
                if not line:
                    break
                try:
                    print(f"   [REMOTO] {line.strip()}")
                except:
                    pass # Ignora erro de encode no print
            
            status = stdout.channel.recv_exit_status()
            if status == 0:
                print(f"[OK] {name}: Sucesso")
            else:
                print(f"[ERRO] {name}: Falhou (Exit {status})")
                try:
                    print(stderr.read().decode())
                except:
                    pass
                return False
            return True

        # 1. Update Básico (Ignorar erro se passar)
        print("\n[EXEC] apt-get update...")
        client.exec_command("apt-get update") 

        # 2. Instalar Curl (Garantia)
        if not run("apt-get install -y curl wget sudo", "Instalando Dependencias"): return

        # 3. Instalar Coolify
        print("\n[EXEC] Iniciando Instalacao do Coolify (Isso pode demorar 5-10 min)...")
        stdin, stdout, stderr = client.exec_command("curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash")
        
        # Ler output até acabar
        for line in iter(stdout.readline, ""):
            try:
                print(line, end="")
            except:
                pass
        
        print("\n[FIM] Instalacao Finalizada.")
        
    except Exception as e:
        print(f"-> Erro Crítico: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    setup_server()
