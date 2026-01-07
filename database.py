"""
Módulo de Gerenciamento de Banco de Dados
Gerencia armazenamento e recuperação de dados no SQLite
"""

import sqlite3
from datetime import datetime, timedelta
import pandas as pd


class Database:
    """Classe para gerenciar operações no banco de dados SQLite"""

    def __init__(self, db_name='crypto_data.db'):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        """Cria e retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                market_cap REAL,
                volume_24h REAL,
                change_24h REAL,
                rank INTEGER
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON crypto_prices(timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_symbol 
            ON crypto_prices(symbol)
        ''')

        conn.commit()
        conn.close()

    def save_data(self, data_list):
        """
        Salva uma lista de dados no banco
        Args:
            data_list: Lista de dicionários com dados das criptomoedas
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        for data in data_list:
            cursor.execute('''
                INSERT INTO crypto_prices 
                (timestamp, name, symbol, price, market_cap, volume_24h, change_24h, rank)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['timestamp'],
                data['name'],
                data['symbol'],
                data['price'],
                data['market_cap'],
                data['volume_24h'],
                data['change_24h'],
                data['rank']
            ))

        conn.commit()
        conn.close()

    def get_latest_data(self):
        """
        Recupera os dados mais recentes
        Returns: DataFrame com os dados mais recentes
        """
        conn = self.get_connection()

        query = '''
            SELECT * FROM crypto_prices 
            WHERE timestamp = (SELECT MAX(timestamp) FROM crypto_prices)
            ORDER BY rank
        '''

        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_historical_data(self, symbol=None, hours=24):
        """
        Recupera dados históricos
        Args:
            symbol: Símbolo da criptomoeda (opcional)
            hours: Número de horas para buscar histórico
        Returns: DataFrame com dados históricos
        """
        conn = self.get_connection()

        cutoff_time = datetime.now() - timedelta(hours=hours)

        if symbol:
            query = '''
                SELECT * FROM crypto_prices 
                WHERE symbol = ? AND timestamp >= ?
                ORDER BY timestamp
            '''
            df = pd.read_sql_query(query, conn, params=(symbol, cutoff_time))
        else:
            query = '''
                SELECT * FROM crypto_prices 
                WHERE timestamp >= ?
                ORDER BY timestamp
            '''
            df = pd.read_sql_query(query, conn, params=(cutoff_time,))

        conn.close()
        return df

    def get_statistics(self):
        """
        Calcula estatísticas gerais dos dados
        Returns: Dicionário com estatísticas
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(DISTINCT symbol) FROM crypto_prices')
        total_coins = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM crypto_prices')
        total_records = cursor.fetchone()[0]

        cursor.execute(
            'SELECT MIN(timestamp), MAX(timestamp) FROM crypto_prices')
        date_range = cursor.fetchone()

        conn.close()

        return {
            'total_coins': total_coins,
            'total_records': total_records,
            'first_record': date_range[0],
            'last_record': date_range[1]
        }

    def delete_old_data(self, days=7):
        """
        Remove dados mais antigos que X dias
        Args:
            days: Número de dias para manter os dados
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cutoff_date = datetime.now() - timedelta(days=days)

        cursor.execute('''
            DELETE FROM crypto_prices 
            WHERE timestamp < ?
        ''', (cutoff_date,))

        deleted_rows = cursor.rowcount
        conn.commit()
        conn.close()

        return deleted_rows

    def get_coin_summary(self, symbol):
        """
        Retorna um resumo estatístico de uma criptomoeda específica
        Args:
            symbol: Símbolo da criptomoeda
        Returns: Dicionário com estatísticas
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                COUNT(*) as total_records,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(volume_24h) as avg_volume
            FROM crypto_prices 
            WHERE symbol = ?
        ''', (symbol,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'total_records': result[0],
                'avg_price': result[1],
                'min_price': result[2],
                'max_price': result[3],
                'avg_volume': result[4]
            }
        return None