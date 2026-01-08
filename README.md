# 📊 Crypto Dashboard - Web Scraping & Analytics Platform

A real-time cryptocurrency monitoring dashboard built with Python, featuring automated web scraping, SQL database management, and interactive data visualization. Deployed on Render.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/dash-2.14.2-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Automated Web Scraping**: Collects real-time cryptocurrency data from public APIs
- **SQL Database Integration**: Stores historical data using SQLite with optimized indexing
- **Interactive Dashboard**: Modern, responsive UI built with Dash and Plotly
- **Real-time Updates**: Auto-refresh functionality with configurable intervals
- **Data Analytics**: Historical price tracking, volume analysis, and market cap rankings
- **Professional Architecture**: Modular design following software engineering best practices

## Screenshots
<img width="1502" height="760" alt="2" src="https://github.com/user-attachments/assets/d07e4706-22ae-4bbd-8724-1f83aa0aa06f" />

<img width="1502" height="760" alt="Untitled design(1)" src="https://github.com/user-attachments/assets/67850969-fd45-4c08-9de8-5efa12b53800" />

### Dashboard Overview
The main interface displays key metrics, price trends, and market rankings with a clean, modern design using vibrant gradients and intuitive visualizations.

## Tech Stack

- **Python 3.8+**
- **Dash & Plotly**: Interactive web-based dashboards
- **Pandas**: Data manipulation and analysis
- **SQLite**: Lightweight database for data persistence
- **Requests & BeautifulSoup**: Web scraping capabilities
- **Schedule**: Automated task scheduling

##  Project Structure

```
crypto-dashboard/
│
├── main.py              # Application entry point
├── scraper.py          # Web scraping logic
├── database.py         # Database management layer
├── dashboard.py        # Dashboard UI and callbacks
├── requirements.txt    # Project dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crypto-dashboard.git
   cd crypto-dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

The application will:
1. Initialize the SQLite database
2. Perform an initial data scraping
3. Schedule automatic updates every 30 minutes
4. Launch the dashboard server

### Accessing the Dashboard

Open your browser and navigate to:
```
http://127.0.0.1:8050
```

### Stopping the Application

Press `Ctrl+C` in the terminal to gracefully shut down the server.

## Features Breakdown

### Web Scraping Module (`scraper.py`)
- Fetches data from CoinGecko public API
- Retrieves top 20 cryptocurrencies by market cap
- Collects price, volume, market cap, and 24h change data
- Implements error handling and retry logic

### Database Module (`database.py`)
- Creates and manages SQLite database
- Implements indexed queries for optimal performance
- Provides methods for data insertion and retrieval
- Calculates statistical summaries
- Supports historical data queries with time-based filtering

### Dashboard Module (`dashboard.py`)
- Modern, responsive UI with gradient backgrounds
- Real-time data visualization using Plotly
- Interactive cryptocurrency selector
- Four key metric cards (total coins, records, market cap, average change)
- Three main charts:
  - **Price History**: Line chart with area fill showing 24h price trends
  - **Volume Analysis**: Bar chart displaying trading volume
  - **Market Rankings**: Horizontal bar chart of top cryptocurrencies by market cap

## Design Philosophy

The dashboard features a modern, clean design with:
- Vibrant color palette (coral red, turquoise, and yellow accents)
- Card-based layout with subtle shadows
- Responsive grid system
- Professional typography
- Intuitive user experience

## Data Flow

```
CoinGecko API → Scraper → SQLite Database → Dashboard → User Interface
                    ↑                             ↓
                    └─────── Schedule (30min) ────┘
```

## Security Considerations

- No API keys required (uses public endpoints)
- Local database storage
- No sensitive data transmission
- Rate limiting implemented to respect API guidelines

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Add user authentication
- [ ] Implement data export functionality (CSV, JSON)
- [ ] Add price alerts and notifications
- [ ] Integrate additional data sources
- [ ] Create mobile-responsive views
- [ ] Add portfolio tracking features
- [ ] Implement advanced technical indicators

##  Known Issues

- Historical charts require at least 2 data points to render
- Initial load may take a few seconds on first run

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## Acknowledgments

- CoinGecko API for providing free cryptocurrency data
- Dash & Plotly community for excellent documentation
- Python community for incredible libraries and tools

## Support

If you have any questions or run into issues, please open an issue on GitHub or contact me directly.

---

⭐ If you found this project helpful, please consider giving it a star!

**Made with ❤️ and Python**
