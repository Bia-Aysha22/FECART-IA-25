from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import random
from datetime import datetime, timedelta
import ssl
import certifi
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# Configuração do Flask
app = Flask(__name__, static_folder='.')
CORS(app)

# Adiciona o caminho para os certificados SSL confiáveis.
os.environ['SSL_CERT_FILE'] = certifi.where()
try:
    _create_unverified_https_context = ssl._create_unverified_https_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# =========================================================================================
# === CONFIGURAÇÃO DE CHAVES DE API =======================================================
# =========================================================================================
# NOTA: A AwesomeAPI não exige uma chave de API para as consultas gratuitas.
NEWS_API_KEY = "579cf0d4f8be4534a96cfa001c58d315"

# Mapeamento de moedas para os tickers da AwesomeAPI e informações completas
MOEDAS_DISPONIVEIS = {
    "Brasil": {
        "moeda": "Real", "ticker": "BRL", "codigo": "BRL", "flag": "🇧🇷",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/057/095/416/non_2x/silhouette-map-of-brazil-on-transparent-backhround-free-png.png",
        "color": "#009C3B", "keywords": ["Brasil", "economia brasileira", "real brasileiro"],
        "description": "O Real Brasileiro é a moeda oficial do Brasil, a maior economia da América Latina.",
        "period_days": 120
    },
    "Rússia": {
        "moeda": "Rublo Russo", "ticker": "RUB", "codigo": "RUB", "flag": "🇷🇺",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg",
        "silhouette": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Babayasin_Russia_outline_map.svg/1280px-Babayasin_Russia_outline_map.png",
        "color": "#D52B1E", "keywords": ["Rússia", "economia russa", "rublo", "gás", "petróleo", "sanções"],
        "description": "O Rublo Russo é a moeda da Rússia, uma das maiores exportadoras de petróleo e gás do mundo.",
        "period_days": 30
    },
    "Índia": {
        "moeda": "Rúpia Indiana", "ticker": "INR", "codigo": "INR", "flag": "🇮🇳",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/947/non_2x/country-map-india-free-png.png",
        "color": "#FF9933", "keywords": ["Índia", "economia indiana", "rúpia"],
        "description": "A Rúpia Indiana é a moeda oficial da Índia, uma das economias que mais crescem no mundo.",
        "period_days": 90
    },
    "China": {
        "moeda": "Yuan Chinês", "ticker": "CNY", "codigo": "CNY", "flag": "🇨🇳",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg",
        "silhouette": "https://www.pngmart.com/files/21/China-Silhoutte-PNG-HD.png",
        "color": "#DE2910", "keywords": ["China", "economia chinesa", "yuan", "comércio"],
        "description": "O Yuan Chinês é a moeda da China, a segunda maior economia do mundo.",
        "period_days": 90
    },
    "África do Sul": {
        "moeda": "Rand Sul-Africano", "ticker": "ZAR", "codigo": "ZAR", "flag": "🇿🇦",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/a/af/Flag_of_South_Africa.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-simple-flat-vector-illustration-of-south-africa-in-solid-black-silhouette-with-country-area-map-vector-picture-image_10081507.png",
        "color": "#007A4D", "keywords": ["África do Sul", "economia sul-africana", "rand"],
        "description": "O Rand Sul-Africano é a moeda da África do Sul, a economia mais industrializada do continente africano.",
        "period_days": 90
    },
    "Argentina": {
        "moeda": "Peso Argentino", "ticker": "ARS", "codigo": "ARS", "flag": "🇦🇷",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-simple-flat-vector-illustration-of-argentinasolid-black-silhouette-map-depicting-the-countrys-area-vector-picture-image_10081545.png",
        "color": "#74ACDF", "keywords": ["Argentina", "economia argentina", "peso argentino", "crise", "inflação"],
        "description": "O Peso Argentino é a moeda da Argentina, conhecida por sua volatilidade econômica.",
        "period_days": 30
    },
    "Egito": {
        "moeda": "Libra Egípcia", "ticker": "EGP", "codigo": "EGP", "flag": "🇪🇬",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Egypt.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/947/non_2x/country-map-india-free-png.png",
        "color": "#CE1126", "keywords": ["Egito", "economia egípcia", "libra egípcia"],
        "description": "A Libra Egípcia é a moeda do Egito, a maior economia do mundo árabe.",
        "period_days": 90
    },
    "Arábia Saudita": {
        "moeda": "Riyal Saudita", "ticker": "SAR", "codigo": "SAR", "flag": "🇸🇦",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg",
        "silhouette": "https://images.vexels.com/media/users/3/314245/isolated/preview/6945b1c55e7dacfa13d16e65f599c231-uma-silhueta-do-mapa-da-arabia-saudita.png",
        "color": "#245C36", "keywords": ["Arábia Saudita", "economia saudita", "riyal", "petróleo", "OPEP"],
        "description": "O Riyal Saudita é a moeda da Arábia Saudita, o maior exportador de petróleo do mundo.",
        "period_days": 90
    },
    "Emirados Árabes Unidos": {
        "moeda": "Dirham", "ticker": "AED", "codigo": "AED", "flag": "🇦🇪",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg",
        "silhouette": "https://cdn.pixabay.com/photo/2016/04/29/00/41/united-arab-emerites-1360076_1280.png",
        "color": "#00843D", "keywords": ["Emirados Árabes Unidos", "economia dos Emirados", "dirham", "petróleo"],
        "description": "O Dirham é a moeda dos Emirados Árabes Unidos, um dos países mais ricos do mundo.",
        "period_days": 90
    },
    "Estados Unidos": {
        "moeda": "Dólar Americano", "ticker": "USD", "codigo": "USD", "flag": "🇺🇸",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "silhouette": "https://www.pngplay.com/wp-content/uploads/12/USA-Map-PNG-HD-Photos.png",
        "color": "#3C3B6E", "keywords": ["Estados Unidos", "economia americana", "dólar", "taxa de juros", "inflação"],
        "description": "O Dólar Americano é a moeda de reserva global e a mais negociada no mundo.",
        "period_days": 120
    },
    "União Europeia": {
        "moeda": "Euro", "ticker": "EUR", "codigo": "EUR", "flag": "🇪🇺",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-eu-flag-overlay-on-vector-map-of-european-union-vector-picture-image_10053056.png",
        "color": "#003399", "keywords": ["União Europeia", "euro", "economia europeia", "BCE", "inflação"],
        "description": "O Euro é a moeda oficial da União Europeia, usado por 19 dos 27 estados-membros.",
        "period_days": 120
    },
    "Japão": {
        "moeda": "Iene Japonês", "ticker": "JPY", "codigo": "JPY", "flag": "🇯🇵",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/980/non_2x/country-map-japan-free-png.png",
        "color": "#BC002D", "keywords": ["Japão", "economia japonesa", "iene", "juros negativos"],
        "description": "O Iene Japonês é a moeda do Japão, a terceira maior economia do mundo.",
        "period_days": 90
    },
    "Reino Unido": {
        "moeda": "Libra Esterlina", "ticker": "GBP", "codigo": "GBP", "flag": "🇬🇧",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg",
        "silhouette": "https://cdn.creazilla.com/silhouettes/2353/great-britain-silhouette-000000-xl.png",
        "color": "#012169", "keywords": ["Reino Unido", "economia britânica", "libra esterlina", "Brexit"],
        "description": "A Libra Esterlina é a moeda do Reino Unido, uma das principais moedas de reserva do mundo.",
        "period_days": 90
    }
}

# =========================================================================================
# === FUNÇÃO DE BUSCA DE DADOS E ANÁLISE DE SENTIMENTO ====================================
# =========================================================================================
def fetch_currency_data(from_ticker, to_ticker, days):
    """Busca dados históricos de uma moeda na API da AwesomeAPI."""
    try:
        url = f'https://economia.awesomeapi.com.br/json/daily/{from_ticker}-{to_ticker}/{days}'
        response = requests.get(url, verify=False)
        data = response.json()

        if isinstance(data, dict) and data.get("code") == "NotFound":
            print(f"Erro ao buscar dados da AwesomeAPI para {from_ticker}/{to_ticker}: Moeda não encontrada ou dados indisponíveis.")
            return None, None

        if not isinstance(data, list) or not data:
            print(f"Erro ao buscar dados da AwesomeAPI: Resposta inesperada ou vazia.")
            return None, None

        historical_data = []
        for item in data:
            date_obj = datetime.fromtimestamp(int(item.get('timestamp')))
            historical_data.append({
                "date": date_obj.strftime('%Y-%m-%d'),
                "value": round(float(item.get('bid')), 4)
            })

        historical_data.reverse()
        last_rate = historical_data[-1]['value']
        return last_rate, historical_data
    except Exception as e:
        print(f"Erro ao buscar dados da AwesomeAPI: {e}")
        return None, None

def analyze_sentiment_from_news(keywords):
    """
    Busca notícias e realiza uma análise de sentimento simples.
    Retorna uma pontuação entre -1 e 1 e um rótulo.
    """
    if not NEWS_API_KEY or NEWS_API_KEY == "SUA_CHAVE_AQUI":
        print("Aviso: Chave de API de notícias não configurada. A análise de sentimento será ignorada.")
        return 0, "Neutro"

    query = ' OR '.join(keywords)
    url = f'https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=relevancy&apiKey={NEWS_API_KEY}'

    positive_words = ["alta", "crescimento", "valorização", "forte", "ganhos", "recuperação", "superou", "aumento", "expansão", "recorde", "estabilidade", "avanço"]
    negative_words = ["queda", "perda", "desvalorização", "fraca", "baixa", "recuo", "diminuição", "instabilidade", "crise", "recessão", "tensão", "déficit"]

    try:
        response = requests.get(url, verify=False)
        data = response.json()
        articles = data.get('articles', [])

        if not articles:
            return 0, "Neutro"

        positive_count = 0
        negative_count = 0

        for article in articles:
            content = (article.get('title', '') + ' ' + article.get('description', '')).lower()
            if any(word in content for word in positive_words):
                positive_count += 1
            if any(word in content for word in negative_words):
                negative_count += 1

        total_count = positive_count + negative_count

        if total_count == 0:
            return 0, "Neutro"

        sentiment_score = (positive_count - negative_count) / total_count

        if sentiment_score > 0.1:
            sentiment_label = "Positivo"
        elif sentiment_score < -0.1:
            sentiment_label = "Negativo"
        else:
            sentiment_label = "Neutro"

        return sentiment_score, sentiment_label
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return 0, "Neutro"

# =========================================================================================
# === MODELOS DE PREVISÃO ENSEMBLE ========================================================
# =========================================================================================

def model_1_trend_prediction(prices):
    """Modelo baseado na tendência de média móvel."""
    if len(prices) < 7:
        return prices[-1]

    sma = sum(prices[-7:]) / 7
    trend = prices[-1] - sma
    return prices[-1] + (trend * random.uniform(0.9, 1.1))

def model_2_simple_average(prices):
    """Modelo baseado na média dos últimos 7 dias."""
    if len(prices) < 7:
        return prices[-1]
    return sum(prices[-7:]) / 7

def model_3_linear_regression(historical_data, sentiment_score, days_to_predict):
    """
    Modelo de regressão linear para previsão.
    Usa dados históricos para treinar o modelo e prevê o valor para `days_to_predict`.
    """
    if len(historical_data) < 30:
        return historical_data[-1]['value']

    prices = [item['value'] for item in historical_data]
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array([[len(prices) + days_to_predict]])
    prediction = model.predict(future_X)[0]

    final_prediction = prediction * (1 + sentiment_score * 0.005)
    return final_prediction

def calculate_ensemble_prediction(historical_data, sentiment_score, days_to_predict):
    """
    Combina previsões de múltiplos modelos e ajusta com base no sentimento de notícias.
    """
    if len(historical_data) < 7:
        last_rate = historical_data[-1]['value']
        return last_rate, 0, "Alto"

    prices = [item['value'] for item in historical_data]

    # Obter previsões de cada modelo
    prediction_1 = model_1_trend_prediction(prices)
    prediction_2 = model_2_simple_average(prices)
    prediction_3 = model_3_linear_regression(historical_data, sentiment_score, days_to_predict)

    # Combinar as previsões usando uma média ponderada
    ensemble_prediction = (prediction_1 * 0.40 + prediction_2 * 0.50 + prediction_3 * 0.10)

    final_prediction = ensemble_prediction

    # Calcular a variância entre as previsões dos modelos
    predictions = [prediction_1, prediction_2, prediction_3]
    variance = sum([(p - ensemble_prediction)**2 for p in predictions]) / len(predictions)

    # A confiabilidade é inversamente proporcional à variância
    max_possible_variance = (max(prices) - min(prices))**2
    reliability = max(0, 100 - (variance / (max_possible_variance + 0.0001)) * 2000)
    reliability = min(95, max(15, reliability))

    # Classificar o risco baseado na variância
    risk_level = "Baixo"
    if variance > 0.001:
        risk_level = "Alto"
    elif variance > 0.0005:
        risk_level = "Médio"

    return round(final_prediction, 4), int(reliability), risk_level

# ------------------------------------------------------------------
# === ROTAS DA API ==================================================
# ------------------------------------------------------------------

@app.route('/api/countries', methods=['GET'])
def list_countries():
    countries = []
    for country, info in MOEDAS_DISPONIVEIS.items():
        countries.append({
            "name": country,
            "flag": info["flag"],
            "moeda": info["moeda"],
            "color": info["color"],
            "description": info["description"]
        })
    return jsonify(countries)

@app.route('/api/analyze', methods=['POST'])
def analyze_currency():
    data = request.json
    country = data.get('country')

    if not country or country not in MOEDAS_DISPONIVEIS:
        return jsonify({'error': 'País não encontrado'}), 400

    moeda_info = MOEDAS_DISPONIVEIS[country]

    # Busca dados da moeda usando a AwesomeAPI, sempre com 180 dias de histórico
    last_rate, historical_data = fetch_currency_data(moeda_info['ticker'], "BRL", 180)

    if not historical_data:
        return jsonify({'error': 'Não foi possível obter dados da moeda'}), 500

    # Executa a análise de notícias
    sentiment_score, sentiment_label = analyze_sentiment_from_news(moeda_info['keywords'])

    # Calcula a previsão para 1, 3 e 6 meses
    predicted_rate_1m, reliability, risk_level = calculate_ensemble_prediction(historical_data[-90:], sentiment_score, 30)
    predicted_rate_3m, _, _ = calculate_ensemble_prediction(historical_data[-90:], sentiment_score, 90)
    predicted_rate_6m, _, _ = calculate_ensemble_prediction(historical_data, sentiment_score, 180)

    change = ((predicted_rate_1m - last_rate) / last_rate) * 100 if last_rate else 0

    # Preparar resposta (inclui "name" em country_info para todos os países)
    response = {
        'country': country,
        'country_info': {**moeda_info, "name": country},
        'last_rate': last_rate,
        'predicted_rate_1m': predicted_rate_1m,
        'predicted_rate_3m': predicted_rate_3m,
        'predicted_rate_6m': predicted_rate_6m,
        'change': change,
        'reliability': reliability,
        'risk_level': risk_level,
        'sentiment_label': sentiment_label,
        'historical_data': historical_data[-30:],
        'today': datetime.now().isoformat()
    }
    return jsonify(response)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index_F.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)