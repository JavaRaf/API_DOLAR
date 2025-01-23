# Imports da biblioteca padrão
import os
from os import getenv
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
import subprocess
import logging
from logging.handlers import RotatingFileHandler

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

def get_currency_wise() -> Currency:
    """
    Obtém a cotação do dólar através do Wise.
    
    Returns:
        Currency: Objeto com informações da cotação
    
    Raises:
        requests.RequestException: Erro na requisição
        ValueError: Erro no processamento dos dados
    """
    logger.debug("Iniciando busca de cotação no Wise")
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/131.0.0.0 Safari/537.36"
    )
    headers = {"User-Agent": user_agent}
    
    try:
        response = requests.get(
            WISE_URL,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        value = soup.find("input", {"id": "target-input"})
        
        if value is None:
            logger.error("Elemento de valor não encontrado na página")
            raise ValueError("Elemento de valor não encontrado na página")
        
        logger.info(f"Cotação Wise obtida: {value.get('value')}")
        return Currency(
            price=float(value.get("value", 0).replace(",", ".")),
            service_name="wise.com"
        )
        
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Erro ao obter taxa de câmbio do Wise: {str(e)}")
        raise

def save_currency(currency: Currency) -> None:
    """
    Salva as informações da cotação em arquivo.
    
    Args:
        currency (Currency): Objeto com informações da cotação
    """
    logger.info("Salvando informações da cotação")
    os.makedirs(HISTORY_DIR, exist_ok=True)
    with open(PRICES_FILE, "a", encoding="utf-8") as f:
        f.write(f"Valor: {currency.price} - Data_criação (UTC): {datetime.fromtimestamp(float(currency.timestamp))}\n")
    logger.info("Informações da cotação salvas com sucesso")

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
        print("Buscando informações de moeda...")
        currency = get_currency_wise()
        print(f"Moeda obtida: {currency}")

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
            save_currency(currency)

    except Exception as e:
        print(f"Erro no fluxo principal: {e}")

if __name__ == "__main__":
    main()
