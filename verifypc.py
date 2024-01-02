import tkinter as tk
from tkinter import ttk, scrolledtext
import platform
import os
import socket
import psutil
import datetime
import subprocess
import time
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tqdm import tqdm

def open_url(url):
    webbrowser.open(url, new=2)

def get_external_ip():
    try:
        # Use um serviço web para obter o IP externo
        external_ip = requests.get('https://api64.ipify.org?format=json').json()['ip']
        return external_ip
    except Exception as e:
        return f"Erro ao obter o IP externo: {str(e)}"

def get_system_info():
    system_info = {
        "Hostname": socket.gethostname(),
        "Sistema Operacional": f"{platform.system()} {platform.release()}",
        "Versão do SO": platform.version(),
        "Arquitetura do Processador": platform.architecture(),
        "Processador": platform.processor(),
        "Núcleos do Processador": psutil.cpu_count(logical=False),
        "Threads do Processador": psutil.cpu_count(logical=True),
        "Uso de CPU (%)": psutil.cpu_percent(interval=1),
        "Memória RAM Total (GB)": round(psutil.virtual_memory().total / (1024**3), 2),
        "Memória RAM Disponível (GB)": round(psutil.virtual_memory().available / (1024**3), 2),
        "Uso de Memória RAM (%)": psutil.virtual_memory().percent,
        "Capacidade Total do Disco (GB)": round(psutil.disk_usage('/').total / (1024**3), 2),
        "Espaço Disponível no Disco (GB)": round(psutil.disk_usage('/').free / (1024**3), 2),
        "Uso de Disco (%)": psutil.disk_usage('/').percent,
        "Placa de Vídeo": subprocess.check_output(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], text=True).strip(),
        "Endereço IP Local": socket.gethostbyname(socket.gethostname()),
        "Endereço IP Externo": get_external_ip(),
    }
    return system_info

def download_icon(url):
    response = requests.get(url)
    return ImageTk.PhotoImage(Image.open(BytesIO(response.content)))

def show_system_info():
    root = tk.Tk()
    root.title("Informações do Sistema")

    style = ttk.Style()
    style.theme_use("clam")

    # Adicionando a arte ASCII
    ascii_art = '''
    $$\      $$\           $$\           $$\           $$\       
    $$$\    $$$ |          \__|          \__|          $$ |      
    $$$$\  $$$$ | $$$$$$\  $$\  $$$$$$\  $$\ $$$$$$$\  $$ |  $$\ 
    $$\$$\$$ $$ | \____$$\ $$ |$$  __$$\ $$ |$$  __$$\ $$ | $$  |
    $$ \$$$  $$ | $$$$$$$ |$$ |$$ |  \__|$$ |$$ |  $$ |$$$$$$  / 
    $$|\$  /$$ |$$  __$$ |$$ |$$ |      $$ |$$ |  $$ |$$  _$$<  
    $$ | \_/ $$ |\$$$$$$$ |$$ |$$ |      $$ |$$ |  $$ |$$ | \$$\ 
    \__|     \__| \_______|\__|\__|      \__|\__|  \__|\__|  \__|
    '''
    label_ascii = ttk.Label(root, text=ascii_art, justify='left', font=('Courier', 8), foreground='black')
    label_ascii.pack(pady=10)

    frame_intro = ttk.Frame(root)
    frame_intro.pack(expand=True, fill="both")

    label_intro = ttk.Label(frame_intro, text="Carregando Informações...", font=('Helvetica', 14, 'bold'), foreground='black')
    label_intro.pack(pady=10)

    progress_bar = ttk.Progressbar(frame_intro, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    # Carregamento simulado
    for _ in tqdm(range(100), desc="Carregando", unit="%", dynamic_ncols=True):
        time.sleep(0.03)  # Simulando um carregamento demorado
        progress_bar["value"] += 1
        root.update_idletasks()

    frame_intro.destroy()  # Remover a tela de carregamento

    frame_info = ttk.Frame(root)
    frame_info.pack(expand=True, fill="both")

    text_area = scrolledtext.ScrolledText(frame_info, wrap=tk.WORD, width=80, height=30)
    text_area.insert(tk.INSERT, "\n".join([f"{key}: {value}" for key, value in get_system_info().items()]))
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill="both")

    # Adicionar botões com redirecionamento para redes sociais
    frame_buttons = ttk.Frame(frame_info)
    frame_buttons.pack(pady=10)

    github_url = "https://github.com/favicon.ico"
    github_icon = download_icon(github_url)

    instagram_url = "https://www.instagram.com/static/images/ico/favicon.ico/36b3ee2d91ed.ico"
    instagram_icon = download_icon(instagram_url)

    twitter_url = "https://twitter.com/favicon.ico"
    twitter_icon = download_icon(twitter_url)

    github_button = ttk.Button(frame_buttons, image=github_icon, command=lambda: open_url("https://github.com/mairinkx"))
    github_button.grid(row=0, column=0, padx=10)

    instagram_button = ttk.Button(frame_buttons, image=instagram_icon, command=lambda: open_url("https://instagram.com/mairinkx"))
    instagram_button.grid(row=0, column=1, padx=10)

    twitter_button = ttk.Button(frame_buttons, image=twitter_icon, command=lambda: open_url(""))
    twitter_button.grid(row=0, column=2, padx=10)

    root.mainloop()

if __name__ == "__main__":
    show_system_info()
