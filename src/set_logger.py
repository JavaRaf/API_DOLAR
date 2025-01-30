import logging
from logging.handlers import RotatingFileHandler


# Configuração do logger com rotação de arquivos
handler = RotatingFileHandler(
    filename="history/app.log",
    maxBytes=1024 * 1024,  # 1MB por arquivo
    backupCount=5,  # Mantém até 5 arquivos de backup
    encoding="utf-8"
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)