from dataclasses import dataclass
import requests
import subprocess
from os import getenv
import os
from datetime import datetime, timezone, timedelta

awsome_api_url = "https://economia.awesomeapi.com.br/last/USD-BRL"
api_layer_url = "https://api.apilayer.com/currency_data/convert"

@dataclass
class Currency:
    price: str
    timestamp: str
    service_name: str

def create_image(value: str, timestamp: str = "", service_name: str = ""):

    command = 'magick' if os.name == 'nt' else 'convert'

    try:
        subprocess.run(
            [command, "images/base.png",
            "-gravity", "center",
            "-pointsize", "50",
            "-font", "fonts/sans-bold.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -210, -100", value,
            "images/output.png"]
        , check=True)

        subprocess.run(
            [command, "images/output.png",
            "-gravity", "center",
            "-pointsize", "20",
            "-font", "fonts/sans-normal.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -35, -40", f"{datetime.fromtimestamp(float(timestamp))} - BRT - fonte: {service_name}",
            "images/output.png"]
        , check=True)

        subprocess.run(
            [command, "images/output.png",
            "-gravity", "center",
            "-pointsize", "28",
            "-font", "fonts/sans-normal.ttf",
            "-fill", "white",
            "-annotate", "00, 00, -190, +140", value,
            "images/output.png"]
        , check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando ImageMagick: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def get_currency_ApiLayer() -> Currency:
    try:
        params = {
        "to": "BRL",
        "from": "USD",
        "amount": 1,
        "apikey": getenv("API_LAYER_TOKEN")
        }

        response = requests.get(api_layer_url, params=params, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            print(f"Erro ao buscar os dados da API: {response.status_code}")
            return None
        
        data = response.json()
        currency = Currency(
            price=data["result"],
            timestamp=data["info"]["timestamp"],
            service_name="APiLayer"  
        )
        return currency
            
    except requests.RequestException as e:
        print(f"Erro ao buscar os dados da API: {e}")
        raise

def get_currency_awesome() -> Currency:
    try:
        response = requests.get(awsome_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        currency = Currency(
            price=data["USDBRL"]["bid"],
            timestamp=data["USDBRL"]["timestamp"],
            service_name="AwesomeAPI"
        )
        return currency
    except requests.RequestException as e:
        print(f"Erro ao buscar os dados da API: {e}")
        raise

def get_currency() -> Currency:
    currency = get_currency_ApiLayer()
    if currency is None:
        currency = get_currency_awesome()
    return currency

def save_currency(currency: Currency):
    os.makedirs("history", exist_ok=True)
    with open("history/prices.txt", "a", encoding="utf-8") as f:  # Certifique-se da codificação correta
        f.write(f"Maior valor: {currency.high} - Data_criação (UTC): {datetime.fromtimestamp(float(currency.timestamp))}\n")

def save_log_fb(post_id: str):
    os.makedirs("history", exist_ok=True)
    with open("history/fb_log.txt", "a") as f:
        f.write(f"https://facebook.com/{post_id}\n")

def post_to_fb():
    
    token = getenv("FB_TOKEN")
    if token is None:
        print("Erro: Variável de ambiente 'FB_TOKEN' não definida.")
        return
    
    fuso_horario = timezone(timedelta(hours=-3))
    data_e_hora_atuais = datetime.now(fuso_horario).strftime("%d/%m/%Y %H:%M:%S")

    message = f"Data da postagem: {data_e_hora_atuais}"

    try:
        with open("images/output.png", "rb") as f:
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
        currency = get_currency()
        print(f"Moeda obtida: {currency}")

        print("Criando imagem...")
        create_image(f"{float(currency.price):.2f}", currency.timestamp, currency.service_name)

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
