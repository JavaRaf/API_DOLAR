import os
import datetime
from datetime import timezone, timedelta

from src.set_logger import logger
from src.get_currency import Currency
from src.config import HISTORY_DIR, FB_LOG_FILE, PRICES_FILE



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



def save_currency_log(currency: Currency) -> None:
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