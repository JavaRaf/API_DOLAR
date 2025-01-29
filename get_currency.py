from config import *
from main import Currency, logger
import requests
from bs4 import BeautifulSoup

class GetCurrency(Currency):

    def __init__(self):
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/131.0.0.0 Safari/537.36"
        )

    def fetch_currency(self, url: str) -> Currency | None:
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Erro ao obter dados da URL {url}: {str(e)}")
            raise

    def get_currency_awesome(self) -> Currency | None:
        """
        Obtém a cotação do dólar através da AwesomeAPI.
        """
        response = self.fetch_currency(AWESOME_API_URL)
        data = response.json()
        value = data["USDBRL"]["bid"]
        logger.info(f"Cotação AwesomeAPI obtida: {value}")
        return Currency(
            price=float(value.replace(",", ".")),
            service_name="awesomeapi.com.br"
        )

    def get_currency_dolarhoje(self) -> Currency | None:
        """
        Obtém a cotação do dólar através do DolarHoje.
        """
        response = self.fetch_currency(DOLAR_HOJE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        value = soup.find("input", {"id": "nacional"})

        if value is None:
            logger.error("Elemento de valor não encontrado na página")
            raise ValueError("Elemento de valor não encontrado na página")
        
        logger.info(f"Cotação DolarHoje obtida: {value.get('value')}")
        return Currency(
            price=float(value.get("value", 0).replace(",", ".")),
            service_name="dolarhoje.com"
        )

    def get_currency_wise(self) -> Currency | None:
        """
        Obtém a cotação do dólar através do Wise.
        
        Returns:
            Currency: Objeto com informações da cotação
        
        Raises:
            requests.RequestException: Erro na requisição
            ValueError: Erro no processamento dos dados
            """
        response = self.fetch_currency(WISE_URL)
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





