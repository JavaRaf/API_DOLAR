# Imports locais
from src.config import *
from src.get_currency import GetCurrency, Currency
from src.set_logger import logger
from src.utils.image_creator import create_image
from src.utils.save_logs import save_log_fb, save_currency_log
from src.utils.facebook import post_to_fb




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
            save_currency_log(currency)

    except Exception as e:
        print(f"Erro no fluxo principal: {e}")

if __name__ == "__main__":
    main()
