"""
Aplicativo Principal - Dashboard de Web Scraping
Executa o scraping e inicia o dashboard
"""

import schedule
import time
import threading
from scraper import CryptoScraper
from database import Database
from dashboard import create_dashboard


def run_scraping():
    """Executa o processo de scraping"""
    print("Iniciando scraping...")
    scraper = CryptoScraper()
    data = scraper.fetch_crypto_data()

    if data:
        db = Database()
        db.save_data(data)
        print(f"✓ {len(data)} registros salvos no banco de dados")
    else:
        print("✗ Nenhum dado coletado")


def schedule_scraping():
    """Agenda o scraping para rodar periodicamente"""
    # Executa imediatamente
    run_scraping()

    # Agenda para rodar a cada 30 minutos
    schedule.every(30).minutes.do(run_scraping)

    while True:
        schedule.run_pending()
        time.sleep(60)


def main():
    """Função principal"""
    print("=" * 60)
    print("Dashboard de Web Scraping - Criptomoedas")
    print("=" * 60)

    # Inicia scraping em thread separada
    scraping_thread = threading.Thread(target=schedule_scraping, daemon=True)
    scraping_thread.start()

    # Inicia o dashboard
    print("\nIniciando dashboard...")
    app = create_dashboard()

    print("\n" + "=" * 60)
    print("Dashboard disponível em: http://127.0.0.1:8050")
    print("Pressione Ctrl+C para encerrar")
    print("=" * 60 + "\n")

    # Para deploy em produção, usa PORT do ambiente
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()