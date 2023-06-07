import requests
from bs4 import BeautifulSoup

TEXT_URL: str = "https://www.online-literature.com/dickens/2941/"

html_page = requests.get(TEXT_URL)