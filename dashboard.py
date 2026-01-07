"""
Módulo do Dashboard
Interface visual para análise dos dados coletados
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
from database import Database
import pandas as pd

# Cores baseadas na imagem (tons vibrantes e modernos)
COLORS = {
    'background': '#f8f9fa',
    'card': '#ffffff',
    'primary': '#ff6b6b',  # Vermelho coral
    'secondary': '#4ecdc4',  # Turquesa
    'accent': '#ffe66d',  # Amarelo
    'text': '#2d3436',
    'text_light': '#636e72',
    'border': '#e1e8ed'
}


def create_dashboard():
    """Cria e configura o dashboard Dash"""

    app = dash.Dash(__name__)

    app.layout = html.Div(style={
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    }, children=[

        # Cabeçalho
        html.Div(style={
            'background': f'linear-gradient(135deg, {COLORS["secondary"]} 0%, {COLORS["primary"]} 100%)',
            'padding': '2rem',
            'marginBottom': '2rem',
            'borderRadius': '0 0 16px 16px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
        }, children=[
            html.H1('Criptocoins Dashboard', style={
                'color': 'white',
                'margin': '0',
                'fontSize': '2.5rem',
                'fontWeight': '600'
            }),
            html.P('Data collected via web scraping and stored in SQL',
                   style={
                       'color': 'rgba(255,255,255,0.9)',
                       'margin': '0.5rem 0 0 0',
                       'fontSize': '1.1rem'
                   })
        ]),

        # Intervalo para atualização automática
        dcc.Interval(
            id='interval-component',
            interval=60 * 1000,  # Atualiza a cada 60 segundos
            n_intervals=0
        ),

        # Container principal
        html.Div(style={
            'maxWidth': '1400px',
            'margin': '0 auto',
            'padding': '0 2rem 2rem 2rem'
        }, children=[

            # Cards de estatísticas
            html.Div(id='stats-cards', style={
                'marginBottom': '2rem'
            }),

            # Seletor de criptomoeda
            html.Div(style={
                'backgroundColor': COLORS['card'],
                'padding': '1.5rem',
                'borderRadius': '12px',
                'marginBottom': '2rem',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                'border': f'1px solid {COLORS["border"]}'
            }, children=[
                html.Label('Select a Cryptocurrency:', style={
                    'fontWeight': '500',
                    'marginBottom': '0.5rem',
                    'display': 'block',
                    'color': COLORS['text']
                }),
                dcc.Dropdown(
                    id='crypto-selector',
                    style={'width': '100%'}
                )
            ]),

            # Gráficos
            html.Div(style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
                'gap': '2rem'
            }, children=[

                # Gráfico de preço histórico
                html.Div(style={
                    'backgroundColor': COLORS['card'],
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': f'1px solid {COLORS["border"]}'
                }, children=[
                    html.H3('Historical Price', style={
                        'marginTop': '0',
                        'color': COLORS['text'],
                        'fontSize': '1.3rem',
                        'fontWeight': '600'
                    }),
                    dcc.Graph(id='price-chart')
                ]),

                # Gráfico de volume
                html.Div(style={
                    'backgroundColor': COLORS['card'],
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': f'1px solid {COLORS["border"]}'
                }, children=[
                    html.H3('Volume 24h', style={
                        'marginTop': '0',
                        'color': COLORS['text'],
                        'fontSize': '1.3rem',
                        'fontWeight': '600'
                    }),
                    dcc.Graph(id='volume-chart')
                ]),

                # Gráfico de ranking
                html.Div(style={
                    'backgroundColor': COLORS['card'],
                    'padding': '1.5rem',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'border': f'1px solid {COLORS["border"]}',
                    'gridColumn': '1 / -1'
                }, children=[
                    html.H3('Top Cryptocurrencies by Market Cap', style={
                        'marginTop': '0',
                        'color': COLORS['text'],
                        'fontSize': '1.3rem',
                        'fontWeight': '600'
                    }),
                    dcc.Graph(id='ranking-chart')
                ])
            ])
        ])
    ])

    @app.callback(
        [Output('stats-cards', 'children'),
         Output('crypto-selector', 'options'),
         Output('crypto-selector', 'value')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_stats_and_selector(n):
        db = Database()
        stats = db.get_statistics()
        latest_data = db.get_latest_data()

        if latest_data.empty:
            return [html.Div("Loading data...")], [], None

        # Cards de estatísticas
        total_market_cap = latest_data['market_cap'].sum()
        avg_change = latest_data['change_24h'].mean()

        cards = html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '1.5rem',
            'marginBottom': '2rem'
        }, children=[
            create_stat_card('Total Coins', f"{stats['total_coins']}",
                             COLORS['primary']),
            create_stat_card('Records in the DB', f"{stats['total_records']:,}",
                             COLORS['secondary']),
            create_stat_card('Market Cap Total',
                             f"${total_market_cap / 1e12:.2f}T",
                             COLORS['accent']),
            create_stat_card('Average 24h Variation', f"{avg_change:.2f}%",
                             COLORS[
                                 'primary'] if avg_change >= 0 else '#e74c3c')
        ])

        # Opções do dropdown
        options = [{'label': f"{row['name']} ({row['symbol']})",
                    'value': row['symbol']}
                   for _, row in latest_data.iterrows()]

        default_value = latest_data.iloc[0][
            'symbol'] if not latest_data.empty else None

        return cards, options, default_value

    @app.callback(
        [Output('price-chart', 'figure'),
         Output('volume-chart', 'figure'),
         Output('ranking-chart', 'figure')],
        [Input('crypto-selector', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_charts(selected_crypto, n):
        db = Database()

        if not selected_crypto:
            empty_fig = go.Figure()
            empty_fig.update_layout(template='plotly_white')
            return empty_fig, empty_fig, empty_fig

        # Dados históricos da moeda selecionada
        historical = db.get_historical_data(selected_crypto, hours=24)

        # Gráfico de preço
        price_fig = go.Figure()
        if not historical.empty:
            price_fig.add_trace(go.Scatter(
                x=historical['timestamp'],
                y=historical['price'],
                mode='lines',
                name='Preço',
                line=dict(color=COLORS['primary'], width=3),
                fill='tozeroy',
                fillcolor=f'rgba(255, 107, 107, 0.1)'
            ))

        price_fig.update_layout(
            template='plotly_white',
            xaxis_title='Time',
            yaxis_title='Price (USD)',
            hovermode='x unified',
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        # Gráfico de volume
        volume_fig = go.Figure()
        if not historical.empty:
            volume_fig.add_trace(go.Bar(
                x=historical['timestamp'],
                y=historical['volume_24h'],
                name='Volume',
                marker_color=COLORS['secondary']
            ))

        volume_fig.update_layout(
            template='plotly_white',
            xaxis_title='Time',
            yaxis_title='Volume (USD)',
            hovermode='x unified',
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        # Gráfico de ranking
        latest = db.get_latest_data().head(10)

        ranking_fig = go.Figure()
        if not latest.empty:
            ranking_fig.add_trace(go.Bar(
                x=latest['market_cap'],
                y=latest['name'],
                orientation='h',
                marker=dict(
                    color=latest['change_24h'],
                    colorscale=[[0, '#e74c3c'], [0.5, '#f39c12'],
                                [1, '#2ecc71']],
                    colorbar=dict(title="24-hour change (%)")
                ),
                text=[f"${x / 1e9:.2f}B" for x in latest['market_cap']],
                textposition='auto'
            ))

        ranking_fig.update_layout(
            template='plotly_white',
            xaxis_title='Market Cap (USD)',
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=10, r=10, t=10, b=10),
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        return price_fig, volume_fig, ranking_fig

    return app


def create_stat_card(title, value, color):
    """Cria um card de estatística"""
    return html.Div(style={
        'backgroundColor': COLORS['card'],
        'padding': '1.5rem',
        'borderRadius': '12px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
        'border': f'1px solid {COLORS["border"]}',
        'borderLeft': f'4px solid {color}'
    }, children=[
        html.Div(title, style={
            'color': COLORS['text_light'],
            'fontSize': '0.9rem',
            'marginBottom': '0.5rem',
            'fontWeight': '500'
        }),
        html.Div(value, style={
            'color': COLORS['text'],
            'fontSize': '2rem',
            'fontWeight': '700'
        })
    ])