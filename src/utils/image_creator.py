import os
from datetime import datetime, timezone, timedelta
import subprocess
from src.set_logger import logger
from src.config import IMAGE_BASE, IMAGE_OUTPUT

def create_image(value: str, service_name: str = "") -> None:
    """
    Cria uma imagem com informações da cotação usando ImageMagick.
    
    Args:
        value (str): Valor da cotação
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
            "-annotate", "00, 00, 0, 100", data_e_hora_atuais,
            IMAGE_OUTPUT]
        , check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao criar imagem: {e}")