"""
Módulo de Web Scraping
Coleta dados de criptomoedas de fontes públicas
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


class CryptoScraper:
    """Classe para realizar web scraping de dados de criptomoedas"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Usando API pública do CoinGecko (não requer autenticação)
        self.api_url = "https://api.coingecko.com/api/v3/coins/markets"

    def fetch_crypto_data(self):
        """
        Coleta dados de criptomoedas
        Returns: Lista de dicionários com dados das criptomoedas
        """
        try:
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 20,
                'page': 1,
                'sparkline': False
            }

            response = requests.get(self.api_url, params=params,
                                    headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            timestamp = datetime.now()

            processed_data = []
            for coin in data:
                processed_data.append({
                    'timestamp': timestamp,
                    'name': coin['name'],
                    'symbol': coin['symbol'].upper(),
                    'price': coin['current_price'],
                    'market_cap': coin['market_cap'],
                    'volume_24h': coin['total_volume'],
                    'change_24h': coin['price_change_percentage_24h'],
                    'rank': coin['market_cap_rank']
                })

            return processed_data

        except requests.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return []

    def get_coin_details(self, coin_id):
        """
        Obtém detalhes específicos de uma criptomoeda
        Args:
            coin_id: ID da criptomoeda
        Returns: Dicionário com detalhes da moeda
        """
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar detalhes: {e}")
            return None