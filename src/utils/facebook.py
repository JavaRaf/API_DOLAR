from os import getenv
import requests
from datetime import datetime, timezone, timedelta
from src.config import IMAGE_OUTPUT






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