# Imports da biblioteca padrão
import os
from os import getenv
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from get_currency import GetCurrency

# Imports de bibliotecas de terceiros
import requests
from bs4 import BeautifulSoup

# Imports locais
from config import *

# Configuração do logger com rotação de arquivos
handler = RotatingFileHandler(
    filename="app.log",
    maxBytes=1024 * 1024,  # 1MB por arquivo
    backupCount=5,  # Mantém até 5 arquivos de backup
    encoding="utf-8"
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@dataclass
class Currency:
    """
    Classe para armazenar informações de cotação de moeda.
    
    Attributes:
        price (str): Valor da cotação
        timestamp (str): Timestamp da cotação
        service_name (str): Nome do serviço que forneceu a cotação
    """
    price: str
    service_name: str

def create_image(value: str, service_name: str = "") -> None:
    """
    Cria uma imagem com informações da cotação usando ImageMagick.
    
    Args:
        value (str): Valor da cotação
        timestamp (str): Timestamp da cotação
        service_name (str): Nome do serviço
    """
    logger.debug(f"Iniciando criação da imagem com valor {value}")
    command = 'magick' if os.name == 'nt' else 'convert'
    data_e_hora_atuais = datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        subprocess.run(
            [command, IMAGE_BASE,
            "-gravity", "center",
            "-pointsize", "50",
            "-font", "fonts/sans-bold.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -210, -100", value,
            IMAGE_OUTPUT]
        , check=True)

        subprocess.run(
            [command, IMAGE_OUTPUT,
            "-gravity", "center",
            "-pointsize", "20",
            "-font", "fonts/sans-normal.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -35, -40", f"{data_e_hora_atuais} - BR - fonte: {service_name}",
            IMAGE_OUTPUT]
        , check=True)

        subprocess.run(
            [command, IMAGE_OUTPUT,
            "-gravity", "center",
            "-pointsize", "28",
            "-font", "fonts/sans-normal.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -190, +140", value,
            IMAGE_OUTPUT]
        , check=True)
        
        logger.info("Imagem criada com sucesso")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o comando ImageMagick: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado na criação da imagem: {e}")
        raise

def save_log_fb(post_id: str) -> None:
    """
    Salva o ID do post do Facebook em arquivo.
    
    Args:
        post_id (str): ID do post criado no Facebook
    """
    logger.info(f"Salvando log do Facebook para post {post_id}")
    os.makedirs(HISTORY_DIR, exist_ok=True)
    with open(FB_LOG_FILE, "a") as f:
        f.write(f"https://facebook.com/{post_id}\n")
    logger.info("Log do Facebook salvo com sucesso")

def save_currency_to_file(currency: Currency) -> None:
    """
    Salva as informações da cotação em arquivo.
    
    Args:
        currency (Currency): Objeto com informações da cotação
    """
    logger.info("Salvando informações da cotação")
    os.makedirs(HISTORY_DIR, exist_ok=True)
    with open(PRICES_FILE, "a", encoding="utf-8") as f:
        f.write(f"Valor: {currency.price} - Data_criação (BR): {datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M:%S')}\n")
    logger.info("Informações da cotação salvas com sucesso")

def post_to_fb() -> str | None:
    token = getenv("FB_TOKEN")
    if token is None:
        print("Erro: Variável de ambiente 'FB_TOKEN' não definida.")
        return None
    
    fuso_horario = timezone(timedelta(hours=-3))
    data_e_hora_atuais = datetime.now(fuso_horario).strftime("%d/%m/%Y %H:%M:%S")

    message = f"Data da postagem: {data_e_hora_atuais}"

    try:
        with open(IMAGE_OUTPUT, "rb") as f:
            image = f.read()

            response = requests.post(
                "https://graph.facebook.com/v21.0/me/photos",
                params={
                    "message": message,
                    "access_token": token
                },
                files={"source": image}
            )
            
        response.raise_for_status()
        return response.json()["id"]
    except requests.RequestException as e:
        print(f"Erro ao postar no Facebook: {e}")

def main():
    try:
        currency_value = None  # Inicializa como None para melhor clareza

        for currency in [
            GetCurrency().get_currency_dolarhoje(),
            GetCurrency().get_currency_wise(),
            GetCurrency().get_currency_awesome()
        ]:
            if currency is not None and currency.price > 0:
                currency_value = currency
                break

        if currency_value is None:
            logger.error("Nenhuma cotação válida encontrada")
            print("Nenhuma cotação válida encontrada")
            return

        print(f"Moeda obtida: {currency_value.price}, {currency_value.service_name}")

    except Exception as e:
        logger.error(f"Erro ao buscar os dados da API: {e}")
        print(f"Erro ao buscar os dados da API: {e}")

    try:    
        print("Criando imagem...")
        create_image(f"{float(currency.price):.2f}", currency.service_name)

        print("Postando no Facebook...")
        post_id = post_to_fb()

        if post_id is not None:
            print(f"Post criado com sucesso. ID: {post_id}")
            save_log_fb(post_id)
            save_currency_to_file(currency)

    except Exception as e:
        print(f"Erro no fluxo principal: {e}")

if __name__ == "__main__":
    main()
