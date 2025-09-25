from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import random
from datetime import datetime
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
# A NewsAPI, por sua vez, exige uma chave. Você pode adicionar mais chaves aqui.
NEWS_API_KEYS = [
    "579cf0d4f8be4534a96cfa001c58d315",
    "42656565682945dc9cb3d46235d88281",
    "2bc4889d67f24aa09de7002a11a57bc8"
]

# Mapeamento de moedas para os tickers da AwesomeAPI e informações completas
MOEDAS_DISPONIVEIS = {
    "Rússia": {
        "moeda": "Rublo Russo", "ticker": "RUB", "codigo": "RUB", "flag": "🇷🇺",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg",
        "silhouette": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Babayasin_Russia_outline_map.svg/1280px-Babayasin_Russia_outline_map.png",
        "color": "#D52B1E",
        "keywords": ["Rússia", "economia russa", "rublo", "gás", "petróleo", "sanções"],
        "description": "O Rublo Russo é a moeda da Rússia, uma economia globalmente integrada e altamente dependente das exportações de commodities como petróleo e gás natural. Sua cotação é sensível a eventos geopolíticos, a flutuações nos preços das commodities e a sanções econômicas internacionais, refletindo a complexidade do cenário político e comercial global.",
        "period_days": 30
    },
    "Índia": {
        "moeda": "Rúpia Indiana", "ticker": "INR", "codigo": "INR", "flag": "🇮🇳",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/947/non_2x/country-map-india-free-png.png",
        "color": "#FF9933",
        "keywords": ["Índia", "economia indiana", "rúpia"],
        "description": "A Rúpia Indiana é a moeda oficial da Índia, a quinta maior economia do mundo e uma das que apresenta o crescimento mais acelerado. Sua performance é impulsionada por um forte setor de tecnologia da informação, um mercado consumidor em expansão e investimentos em infraestrutura. A política monetária do Reserve Bank of India e a dinâmica do mercado de trabalho são cruciais para sua estabilidade.",
        "period_days": 90
    },
    "China": {
        "moeda": "Yuan Chinês", "ticker": "CNY", "codigo": "CNY", "flag": "🇨🇳",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg",
        "silhouette": "https://www.pngmart.com/files/21/China-Silhoutte-PNG-HD.png",
        "color": "#DE2910",
        "keywords": ["China", "economia chinesa", "yuan", "comércio"],
        "description": "O Yuan Chinês, ou Renminbi, é a moeda da China, a segunda maior economia do mundo e um centro vital de manufatura e comércio global. A estabilidade de sua cotação é de grande importância para o comércio internacional, e sua política cambial é gerenciada pelo Banco Popular da China. A moeda reflete tanto a força industrial do país quanto as relações comerciais com seus parceiros globais.",
        "period_days": 90
    },
    "África do Sul": {
        "moeda": "Rand Sul-Africano", "ticker": "ZAR", "codigo": "ZAR", "flag": "🇿🇦",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/a/af/Flag_of_South_Africa.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-simple-flat-vector-illustration-of-south-africa-in-solid-black-silhouette-with-country-area-map-vector-picture-image_10081507.png",
        "color": "#007A4D",
        "keywords": ["África do Sul", "economia sul-africana", "rand"],
        "description": "O Rand Sul-Africano é a moeda da África do Sul, a nação mais industrializada do continente. Sua cotação está intimamente ligada ao desempenho do setor de mineração, especialmente ouro e platina, e à estabilidade política interna. A moeda é um reflexo direto dos desafios e oportunidades econômicas do país, incluindo questões de emprego e infraestrutura.",
        "period_days": 90
    },
    "Argentina": {
        "moeda": "Peso Argentino", "ticker": "ARS", "codigo": "ARS", "flag": "🇦🇷",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-simple-flat-vector-illustration-of-argentinasolid-black-silhouette-map-depicting-the-countrys-area-vector-picture-image_10081545.png",
        "color": "#74ACDF",
        "keywords": ["Argentina", "economia argentina", "peso argentino", "crise", "inflação"],
        "description": "O Peso Argentino é a moeda oficial da Argentina, uma economia marcada por períodos de alta inflação e volatilidade. Sua cotação é um termômetro da estabilidade fiscal e das políticas do governo. O mercado cambial argentino é influenciado por fatores como a confiança dos investidores, negociações da dívida e a produção agrícola do país.",
        "period_days": 30
    },
    "Egito": {
        "moeda": "Libra Egípcia", "ticker": "EGP", "codigo": "EGP", "flag": "🇪🇬",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Egypt.svg",
        "silhouette": "https://cdn.creazilla.com/silhouettes/2560/egypt-map-silhouette-000000-md.png",
        "color": "#C8102E",
        "keywords": ["Egito", "economia egípcia", "libra egípcia"],
        "description": "A Libra Egípcia é a moeda do Egito, uma economia que lida com desafios fiscais e a dependência do turismo, das remessas de egípcios no exterior e da receita do Canal de Suez. A sua cotação é afetada por medidas de política econômica, como a flutuação controlada do câmbio, e por tensões geopolíticas regionais.",
        "period_days": 90
    },
    "Arábia Saudita": {
        "moeda": "Riyal Saudita", "ticker": "SAR", "codigo": "SAR", "flag": "🇸🇦",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg",
        "silhouette": "https://images.vexels.com/media/users/3/314245/isolated/preview/6945b1c55e7dacfa13d16e65f599c231-uma-silhueta-do-mapa-da-arabia-saudita.png",
        "color": "#245C36",
        "keywords": ["Arábia Saudita", "economia saudita", "riyal", "petróleo", "OPEP"],
        "description": "O Riyal Saudita, moeda oficial da Arábia Saudita, é um dos principais indicadores da economia do Oriente Médio. Sua cotação é indexada ao Dólar Americano, garantindo estabilidade. A economia saudita é a maior do mundo árabe e é fortemente dependente da exportação de petróleo. Mudanças na política da OPEP e nos preços globais do petróleo impactam diretamente a economia do país.",
        "period_days": 90
    },
    "Estados Unidos": {
        "moeda": "Dólar Americano", "ticker": "USD", "codigo": "USD", "flag": "🇺🇸",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "silhouette": "https://www.pngplay.com/wp-content/uploads/12/USA-Map-PNG-HD-Photos.png",
        "color": "#3C3B6E",
        "keywords": ["Estados Unidos", "economia americana", "dólar", "taxa de juros", "inflação"],
        "description": "O Dólar Americano é a principal moeda de reserva global e a mais negociada no mundo. A sua cotação reflete não apenas a saúde da economia dos EUA, mas também a confiança global. Decisões do Federal Reserve (o banco central americano), dados sobre inflação e emprego, e o cenário político internacional têm um impacto direto em seu valor, afetando mercados financeiros em todo o planeta.",
        "period_days": 120
    },
    "União Europeia": {
        "moeda": "Euro", "ticker": "EUR", "codigo": "EUR", "flag": "🇪🇺",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230807/original/pngtree-eu-flag-overlay-on-vector-map-of-european-union-vector-picture-image_10053056.png",
        "color": "#003399",
        "keywords": ["União Europeia", "euro", "economia europeia", "BCE", "inflação"],
        "description": "O Euro é a moeda comum de 19 países da União Europeia, sendo a segunda maior moeda de reserva global. A sua cotação reflete a saúde econômica de um bloco diversificado de nações. Decisões do Banco Central Europeu (BCE), a estabilidade financeira dos países-membros e o desempenho de setores chave como indústria e serviços influenciam diretamente o valor do Euro.",
        "period_days": 120
    },
    "Japão": {
        "moeda": "Iene Japonês", "ticker": "JPY", "codigo": "JPY", "flag": "🇯🇵",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/980/non_2x/country-map-japan-free-png.png",
        "color": "#BC002D",
        "keywords": ["Japão", "economia japonesa", "iene", "juros negativos"],
        "description": "O Iene Japonês é a moeda do Japão, uma das economias mais desenvolvidas e tecnologicamente avançadas do mundo. A sua cotação é influenciada pela política monetária do Banco do Japão, que tem mantido taxas de juros ultra-baixas, e pelas exportações de bens de alta tecnologia. O Iene é considerado um 'porto seguro' em tempos de incerteza global, atraindo investidores.",
        "period_days": 90
    },
    "Reino Unido": {
        "moeda": "Libra Esterlina", "ticker": "GBP", "codigo": "GBP", "flag": "🇬🇧",
        "flag_img": "https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg",
        "silhouette": "https://cdn.creazilla.com/silhouettes/2353/great-britain-silhouette-000000-xl.png",
        "color": "#012169",
        "keywords": ["Reino Unido", "economia britânica", "libra esterlina", "Brexit"],
        "description": "A Libra Esterlina é a moeda do Reino Unido e uma das mais importantes do mundo. A sua cotação reflete a saúde da economia britânica, que é dominada pelo setor de serviços, especialmente finanças. A política do Banco da Inglaterra e as negociações comerciais pós-Brexit continuam a ter um grande impacto sobre o seu valor no mercado internacional.",
        "period_days": 90
    },
    "Emirados Árabes Unidos": {
        "moeda": "Dirham", "ticker": "AED", "codigo": "AED", "flag": "🇦🇪",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg",
        "silhouette": "https://cdn.pixabay.com/photo/2016/04/29/00/41/united-arab-emerites-1360076_1280.png",
        "color": "#00843D",
        "keywords": ["Emirados Árabes Unidos", "economia dos Emirados", "dirham", "petróleo"],
        "description": "O Dirham dos Emirados Árabes Unidos é uma moeda estável, que também é atrelada ao Dólar Americano. Sua estabilidade é um pilar para o crescimento da economia do país, que se diversificou para além do petróleo e inclui setores como turismo, finanças e tecnologia. O Dirham reflete a força econômica dos Emirados, um polo de negócios e inovação na região.",
        "period_days": 90
    },
    "Canadá": {
        "moeda": "Dólar Canadense", "ticker": "CAD", "codigo": "CAD", "flag": "🇨🇦",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Canada_%28Pantone%29.svg",
        "silhouette": "https://cdn.creazilla.com/silhouettes/2787/canada-map-silhouette-000000-lg.png",
        "color": "#D41E38",
        "keywords": ["Dólar Canadense", "economia Canadá", "juros Canadá", "inflação Canadá"],
        "description": "O Dólar Canadense é a moeda do Canadá, uma economia desenvolvida e rica em recursos naturais como petróleo, gás natural e minerais. Sua cotação é conhecida por sua forte correlação com os preços globais das commodities e com o desempenho econômico de seu principal parceiro comercial, os Estados Unidos. A política do Banco do Canadá, focada em manter a estabilidade de preços, é um fator chave para o seu valor.",
        "period_days": 90
    },
    "Austrália": {
        "moeda": "Dólar Australiano", "ticker": "AUD", "codigo": "AUD", "flag": "🇦🇺",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Flag_of_Australia.svg",
        "silhouette": "https://www.mappng.com/png-country-maps/2021-06-30157australia-map-black.png",
        "color": "#00008B",
        "keywords": ["Dólar Australiano", "economia Austrália", "juros Austrália", "inflação Austrália"],
        "description": "O Dólar Australiano é a moeda da Austrália, uma economia robusta e diversificada, com destaque para a mineração e o setor de serviços. Conhecida como uma 'moeda de commodity', o AUD é sensível às flutuações nos preços globais de minério de ferro e carvão. Sua cotação também reflete a saúde da economia chinesa, seu maior parceiro comercial, e as decisões de política monetária do Reserve Bank of Australia.",
        "period_days": 90
    },
    "Suíça": {
        "moeda": "Franco Suíço", "ticker": "CHF", "codigo": "CHF", "flag": "🇨🇭",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Flag_of_Switzerland_%28Pantone%29.svg/1200px-Flag_of_Switzerland_%28Pantone%29.svg.png",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/067/937/579/non_2x/switzerland-map-silhouette-icon-isolated-on-transparent-background-free-png.png",
        "color": "#FF0000",
        "keywords": ["Franco Suíço", "economia Suíça", "juros Suíça", "inflação Suíça"],
        "description": "O Franco Suíço é a moeda da Suíça, reconhecida globalmente por sua estabilidade e por seu status de 'porto seguro' em tempos de incerteza geopolítica ou econômica. A Suíça possui um sistema financeiro robusto, uma política de neutralidade e um histórico de baixa inflação, o que faz do Franco uma escolha popular para investidores em busca de segurança. A política do Banco Nacional Suíço é crucial para gerir seu valor.",
        "period_days": 90
    },
    "México": {
        "moeda": "Peso Mexicano", "ticker": "MXN", "codigo": "MXN", "flag": "🇲🇽",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Flag_of_Mexico.svg",
        "silhouette": "https://cdn.creazilla.com/silhouettes/1819/mexico-map-silhouette-000000-lg.png",
        "color": "#006847",
        "keywords": ["Peso Mexicano", "economia México", "juros México", "inflação México"],
        "description": "O Peso Mexicano é a moeda oficial do México, uma economia emergente com fortes laços comerciais com os Estados Unidos. Sua cotação é sensível a eventos econômicos e políticos na América do Norte, especialmente a negociação de acordos comerciais e a política de imigração. A política monetária do Banco de México e os preços do petróleo também são fatores importantes para sua estabilidade.",
        "period_days": 90
    },
    "Turquia": {
        "moeda": "Lira Turca", "ticker": "TRY", "codigo": "TRY", "flag": "🇹🇷",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Turkey.svg",
        "silhouette": "https://exposetobacco.org/wp-content/uploads/Turkey-2.png",
        "color": "#E30A17",
        "keywords": ["Lira Turca", "economia Turquia", "juros Turquia", "inflação Turquia"],
        "description": "A Lira Turca é a moeda da Turquia, uma economia em transição com desafios significativos de inflação e volatilidade. Sua cotação reflete as incertezas políticas internas, as decisões de política monetária e as tensões geopolíticas na região. A gestão da Lira pelo Banco Central da República da Turquia é um ponto focal para investidores e analistas, dada a sua influência na economia do país.",
        "period_days": 90
    },
    "Coreia do Sul": {
        "moeda": "Won Sul-Coreano", "ticker": "KRW", "codigo": "KRW", "flag": "🇰🇷",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20230810/original/pngtree-map-of-south-korea-icon-black-color-south-east-silhouette-vector-picture-image_10241716.png",
        "color": "#0047A0",
        "keywords": ["Won Sul-Coreano", "economia Coreia do Sul", "juros Coreia do Sul", "inflação Coreia do Sul"],
        "description": "O Won Sul-Coreano é a moeda da Coreia do Sul, uma das maiores economias asiáticas, líder em tecnologia, eletrônicos e semicondutores. A sua cotação é um termômetro para o comércio global e a confiança dos investidores em economias de exportação. Eventos geopolíticos na Península Coreana e a dinâmica da economia chinesa têm um impacto direto no valor do Won.",
        "period_days": 90
    },
    "Suécia": {
        "moeda": "Coroa Sueca", "ticker": "SEK", "codigo": "SEK", "flag": "🇸🇪",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Flag_of_Sweden.svg",
        "silhouette": "https://storage.needpix.com/rsynced_images/sweden-35134_1280.png",
        "color": "#FECC01",
        "keywords": ["Coroa Sueca", "economia Suécia", "juros Suécia", "inflação Suécia"],
        "description": "A Coroa Sueca é a moeda da Suécia, uma economia desenvolvida com foco em inovação, tecnologia e exportação de bens e serviços. A cotação da Coroa é influenciada pela política monetária do Riksbank, o banco central mais antigo do mundo, e pelo desempenho dos setores de exportação. A economia sueca é conhecida por sua estabilidade e forte setor de serviços, mas também pode ser sensível a mudanças no cenário global.",
        "period_days": 90
    },
    "Noruega": {
        "moeda": "Coroa Norueguesa", "ticker": "NOK", "codigo": "NOK", "flag": "🇳🇴",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg",
        "silhouette": "https://static.vecteezy.com/system/resources/previews/037/797/989/non_2x/country-map-norway-free-png.png",
        "color": "#BA0C2F",
        "keywords": ["Coroa Norueguesa", "economia Noruega", "petróleo Noruega", "gás"],
        "description": "A Coroa Norueguesa é a moeda da Noruega, uma economia pequena, mas extremamente rica, impulsionada por vastas reservas de petróleo e gás. Sua cotação é sensível a flutuações nos preços globais do petróleo e à política do Norges Bank. A estabilidade política e o fundo soberano do país a tornam uma moeda confiável.",
        "period_days": 90
    },
    "Singapura": {
        "moeda": "Dólar de Singapura", "ticker": "SGD", "codigo": "SGD", "flag": "🇸🇬",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Flag_of_Singapore.svg",
        "silhouette": "https://www.pngmart.com/files/15/Singapore-Map-PNG-Image.png",
        "color": "#EF4026",
        "keywords": ["Dólar de Singapura", "economia Singapura", "política monetária de Singapura", "comércio asiático"],
        "description": "O Dólar de Singapura é a moeda de Singapura, um dos maiores centros financeiros e de comércio do mundo. Sua cotação é gerenciada pelo banco central do país por meio de uma 'banda de câmbio' em relação a outras moedas. A estabilidade do SGD reflete o sucesso de Singapura como uma economia de alta tecnologia e o seu papel estratégico no comércio global.",
        "period_days": 90
    },
    "Bitcoin": {
        "moeda": "Bitcoin", "ticker": "BTC", "codigo": "BTC", "flag": "₿",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg",
        "silhouette": "https://png.pngtree.com/png-vector/20240816/ourmid/pngtree-bitcoin-symbol-btc-gold-plate-on-transparent-background-png-image_13503828.png",
        "color": "#F7931A",
        "keywords": ["Bitcoin", "crypto", "preço Bitcoin", "BTC"],
        "description": "O Bitcoin é a primeira e mais conhecida criptomoeda descentralizada, baseada em tecnologia blockchain. Lançado em 2009, ele serve como uma forma de 'ouro digital' para muitos investidores, sendo visto como uma reserva de valor e uma proteção contra a inflação das moedas tradicionais. Sua extrema volatilidade e a natureza descentralizada o tornam um ativo de alto risco e de grande interesse no mercado financeiro global.",
        "period_days": 180
    },
    "Ethereum": {
        "moeda": "Ethereum", "ticker": "ETH", "codigo": "ETH", "flag": "Ξ",
        "flag_img": "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg",
        "silhouette": "https://png.pngtree.com/png-clipart/20250105/original/pngtree-ethereum-cryptocurrency-coin-represents-modern-finance-and-digital-currency-growth-png-image_19122532.png",
        "color": "#627EEA",
        "keywords": ["Ethereum", "crypto", "preço Ethereum", "ETH"],
        "description": "Ethereum é a segunda maior criptomoeda e uma plataforma de blockchain descentralizada de código aberto. Sua principal inovação é a funcionalidade de contrato inteligente, que permite a criação de aplicações descentralizadas (dApps), finanças descentralizadas (DeFi) e tokens não fungíveis (NFTs). A cotação do Ether (ETH), a moeda nativa da plataforma, é influenciada pela adoção e desenvolvimento de seu ecossistema.",
        "period_days": 180
    },
    "Litecoin": {
        "moeda": "Litecoin", "ticker": "LTC", "codigo": "LTC", "flag": "Ł",
        "flag_img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1dn-Q-AmFkN9D2CWb30Y-UOZEH01vb0gqnw&s",
        "silhouette": "https://png.pngtree.com/png-clipart/20240428/original/pngtree-gold-futuristic-litecoin-cryptocurrency-coin-png-image_14960708.png",
        "color": "#BFBFBF",
        "keywords": ["Litecoin", "crypto", "preço Litecoin", "LTC"],
        "description": "O Litecoin é uma criptomoeda peer-to-peer e projeto de software de código aberto, criado em 2011 como um 'fork' do Bitcoin. Conhecido como a 'prata para o ouro do Bitcoin', o Litecoin foi projetado para ter um tempo de processamento de bloco mais rápido (2,5 minutos versus 10 minutos do Bitcoin) e uma quantidade total maior de moedas. Sua cotação é impulsionada pela adoção e interesse no mercado de criptoativos, mas geralmente segue as tendências do Bitcoin.",
        "period_days": 180
    }
}
# Países que realmente fazem parte do BRICS (membros oficiais)
BRICS_MEMBERS = ["Brasil", "Rússia", "Índia", "China", "África do Sul"]

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
    """Busca notícias e realiza uma análise de sentimento simples."""
    print(f"Buscando notícias para palavras-chave: {keywords}")

    for api_key in NEWS_API_KEYS:
        query = ' OR '.join(keywords)
        url = f'https://newsapi.org/v2/everything?q={query}&language=pt&sortBy=relevancy&apiKey={api_key}'

        print(f"Tentando chave: {api_key[:10]}...")

        try:
            # Usar verificação SSL com certificados confiáveis
            response = requests.get(
                url,
                verify=certifi.where(),  # Usar certificados confiáveis
                timeout=10
            )

            data = response.json()
            print(f"Status da resposta: {data.get('status')}")

            if data.get("status") == "ok":
                articles = data.get('articles', [])[:5]
                print(f"✅ Artigos encontrados: {len(articles)}")

                if articles:
                    return process_sentiment(articles)
                else:
                    print("⚠️ Nenhum artigo encontrado")
                    continue

            else:
                error_message = data.get('message', 'Erro desconhecido')
                print(f"❌ Erro com a chave {api_key[:10]}...: {error_message}")
                continue

        except requests.exceptions.SSLError as ssl_error:
            print(f"❌ Erro SSL com a chave {api_key[:10]}...: {ssl_error}")
            # Tentar sem verificação SSL como fallback
            try:
                response = requests.get(url, verify=False, timeout=10)
                data = response.json()

                if data.get("status") == "ok":
                    articles = data.get('articles', [])[:5]
                    print(f"✅ Artigos encontrados (SSL ignorado): {len(articles)}")
                    return process_sentiment(articles)

            except Exception as fallback_error:
                print(f"❌ Fallback também falhou: {fallback_error}")
                continue

        except Exception as e:
            print(f"❌ Erro geral com a chave {api_key[:10]}...: {str(e)}")
            continue

    print("❌ Todas as chaves falharam, retornando neutro")
    return 0, "Neutro", []

def process_sentiment(articles):
    """Processa os artigos para análise de sentimento."""
    positive_words = ["alta", "crescimento", "valorização", "forte", "ganhos", "recuperação", "superou", "aumento", "expansão", "recorde", "estabilidade", "avanço"]
    negative_words = ["queda", "perda", "desvalorização", "fraca", "baixa", "recuo", "diminuição", "instabilidade", "crise", "recessão", "tensão", "déficit"]

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
        return 0, "Neutro", articles

    sentiment_score = (positive_count - negative_count) / total_count
    if sentiment_score > 0.1:
        sentiment_label = "Positivo"
    elif sentiment_score < -0.1:
        sentiment_label = "Negativo"
    else:
        sentiment_label = "Neutro"

    return sentiment_score, sentiment_label, articles
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

def model_4_arima_prediction(historical_data, days_to_predict):
    """
    Modelo de previsão usando ARIMA para capturar tendências e sazonalidade.
    """
    if len(historical_data) < 60:
        return historical_data[-1]['value']

    prices = [item['value'] for item in historical_data]
    try:
        # A ordem (p,d,q) pode ser ajustada ou otimizada com um grid search.
        # Aqui, usamos uma ordem simples para demonstração.
        model = ARIMA(prices, order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=days_to_predict)[-1]
        return forecast
    except Exception as e:
        print(f"Erro no modelo ARIMA: {e}")
        return prices[-1]

def calculate_ensemble_prediction(historical_data, sentiment_score, days_to_predict):
    """
    Combina previsões de múltiplos modelos com ponderação dinâmica e ajusta
    com base no sentimento de notícias.
    """
    if len(historical_data) < 60:
        last_rate = historical_data[-1]['value']
        return last_rate, 0, "Alto"

    prices = [item['value'] for item in historical_data]

    # Divide os dados para treinar e validar os modelos
    training_data = historical_data[:-30]
    validation_data = historical_data[-30:]
    validation_prices = [item['value'] for item in validation_data]

    # Obter previsões de cada modelo para o período de validação
    pred_1_val = [model_1_trend_prediction([item['value'] for item in training_data[:i+1]]) for i in range(len(validation_data))]
    pred_2_val = [model_2_simple_average([item['value'] for item in training_data[:i+1]]) for i in range(len(validation_data))]
    pred_3_val = [model_3_linear_regression(training_data[:i+1], sentiment_score, 1) for i in range(len(validation_data))]
    pred_4_val = [model_4_arima_prediction(training_data[:i+1], 1) for i in range(len(validation_data))]

    # Calcular o Erro Absoluto Médio (MAE) para cada modelo
    mae_1 = np.mean(np.abs(np.array(pred_1_val) - np.array(validation_prices)))
    mae_2 = np.mean(np.abs(np.array(pred_2_val) - np.array(validation_prices)))
    mae_3 = np.mean(np.abs(np.array(pred_3_val) - np.array(validation_prices)))
    mae_4 = np.mean(np.abs(np.array(pred_4_val) - np.array(validation_prices)))

    # Calcular pesos dinâmicos. Modelos com menor MAE recebem maior peso.
    total_mae = mae_1 + mae_2 + mae_3 + mae_4 + 0.00001
    weight_1 = 1 - (mae_1 / total_mae)
    weight_2 = 1 - (mae_2 / total_mae)
    weight_3 = 1 - (mae_3 / total_mae)
    weight_4 = 1 - (mae_4 / total_mae)
    total_weights = weight_1 + weight_2 + weight_3 + weight_4

    if total_weights > 0:
        weight_1 /= total_weights
        weight_2 /= total_weights
        weight_3 /= total_weights
        weight_4 /= total_weights

    # Obter previsões finais usando os dados completos
    prediction_1 = model_1_trend_prediction(prices)
    prediction_2 = model_2_simple_average(prices)
    prediction_3 = model_3_linear_regression(historical_data, sentiment_score, days_to_predict)
    prediction_4 = model_4_arima_prediction(historical_data, days_to_predict)

    # Combinação final das previsões com pesos dinâmicos
    ensemble_prediction = (
        prediction_1 * weight_1 +
        prediction_2 * weight_2 +
        prediction_3 * weight_3 +
        prediction_4 * weight_4
    )

    final_prediction = ensemble_prediction * (1 + sentiment_score * 0.005)

    # Calcular a variância entre as previsões dos modelos
    predictions = [prediction_1, prediction_2, prediction_3, prediction_4]
    variance = np.var(predictions)

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
            "description": info["description"],
            "is_brics_member": country in BRICS_MEMBERS  # Adiciona esta linha
        })
    return jsonify(countries)

@app.route('/api/analyze', methods=['POST'])
def analyze_currency():
    data = request.json
    country = data.get('country')

    if not country or country not in MOEDAS_DISPONIVEIS:
        return jsonify({'error': 'País não encontrado'}), 400

    moeda_info = MOEDAS_DISPONIVEIS[country]

    last_rate, historical_data = fetch_currency_data(moeda_info['ticker'], "BRL", 180)

    if not historical_data:
        return jsonify({'error': 'Não foi possível obter dados da moeda'}), 500

    # Realiza análise de sentimento das notícias e armazena os artigos retornados
    sentiment_score, sentiment_label, news_articles = analyze_sentiment_from_news(moeda_info['keywords'])

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
        'today': datetime.now().isoformat(),
        'news': news_articles # Adiciona a lista de notícias à resposta
    }
    return jsonify(response)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index_F.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)