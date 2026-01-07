
import schedule
import time
import threading
from scraper import CryptoScraper
from database import Database
from dashboard import create_dashboard


def run_scraping():
    """Executa o processo de scraping"""
    print("Starting scraping...")
    scraper = CryptoScraper()
    data = scraper.fetch_crypto_data()

    if data:
        db = Database()
        db.save_data(data)
        print(f"✓ {len(data)} Records saved in the database")
    else:
        print("✗ No data collected.")


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
    print("Web Scraping Dashboard - Criptocoins")
    print("=" * 60)

    # Inicia scraping em thread separada
    scraping_thread = threading.Thread(target=schedule_scraping, daemon=True)
    scraping_thread.start()

    # Inicia o dashboard
    print("\nStarting panel...")
    app = create_dashboard()

    print("\n" + "=" * 60)
    print("Dashboard available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to quit.")
    print("=" * 60 + "\n")

    app.run_server(debug=False, host='127.0.0.1', port=8050)


if __name__ == "__main__":
    main()