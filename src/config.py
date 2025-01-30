from pathlib import Path

# URLs das APIs
AWESOME_API_URL = "https://economia.awesomeapi.com.br/last/USD-BRL"
WISE_URL = "https://wise.com/br/currency-converter/usd-to-brl-rate?amount=1"
DOLAR_HOJE_URL = "https://www.dolarhoje.com/"

# Caminhos de arquivo
BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_DIR = BASE_DIR / "history"
PRICES_FILE = HISTORY_DIR / "prices.txt"
FB_LOG_FILE = HISTORY_DIR / "fb_log.txt"

# Caminhos de imagens
IMAGE_BASE = BASE_DIR / "images" / "base.png"
IMAGE_OUTPUT = BASE_DIR / "images" / "output.png" 

# Caminhos de fontes
FONT_PATH_SANS_BOLD = BASE_DIR / "fonts" / "sans-bold.ttf"
FONT_PATH_SANS_NORMAL = BASE_DIR / "fonts" / "sans-normal.ttf"