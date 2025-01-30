import os
from datetime import datetime, timezone, timedelta
import subprocess
from src.set_logger import logger
from src.config import IMAGE_BASE, IMAGE_OUTPUT, FONT_PATH_SANS_BOLD, FONT_PATH_SANS_NORMAL

def create_image(value: str, service_name: str = "") -> None:
    """
    Cria uma imagem com informações da cotação usando ImageMagick.
    
    Args:
        value (str): Valor da cotação
        service_name (str): Nome do serviço
    """
    logger.debug(f"Iniciando criação da imagem com valor {value}")
    command = 'magick' if os.name == 'nt' else 'convert'
    data_e_hora_atuais = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M:%S")



    
    try:
        
        subprocess.run(
            [command, IMAGE_BASE,
            "-gravity", "center",
            "-pointsize", "50",
            "-font", FONT_PATH_SANS_BOLD.as_posix(),
            "-fill", "white",
            "-annotate", "00, 00, -210, -100", value,
            IMAGE_OUTPUT]
        , check=True)

        subprocess.run(
            [command, IMAGE_OUTPUT,
            "-gravity", "center",
            "-pointsize", "20",
            "-font", FONT_PATH_SANS_NORMAL.as_posix(),
            "-fill", "white",
            "-annotate", "00, 00, -35, -40", f"{data_e_hora_atuais} - BR - fonte: {service_name}",
            IMAGE_OUTPUT]
        , check=True)

        subprocess.run(
            [command, IMAGE_OUTPUT,
            "-gravity", "center",
            "-pointsize", "28",
            "-font", FONT_PATH_SANS_NORMAL.as_posix(),
            "-fill", "white",
            "-annotate", "00, 00, -190, +140", value,
            IMAGE_OUTPUT]
        , check=True)
    
        logger.debug("Imagem criada com sucesso")
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar o comando ImageMagick: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado na criação da imagem: {e}")
        raise


