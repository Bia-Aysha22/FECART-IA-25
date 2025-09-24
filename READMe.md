# FECART 2025 - Previsão de Moedas BRICS+

Este é um projeto acadêmico desenvolvido para a FECART 2025 que visa analisar e prever a cotação de moedas dos países BRICS+ (Brasil, Rússia, Índia, China, África do Sul e outros) usando inteligência artificial e análise de sentimentos.

O aplicativo web permite visualizar dados históricos, analisar a confiabilidade das previsões e entender o nível de risco de cada moeda, oferecendo uma interface interativa e visualmente clara para o usuário.

---

### 🚀 Tecnologias Utilizadas

**Backend (API)**
* **Python**
* **Flask**: Framework para a construção da API.
* **Requests**: Para fazer requisições a APIs externas (AwesomeAPI).
* **Numpy, scikit-learn, pmdarima, prophet**: Bibliotecas para a análise de dados e criação de modelos de previsão.
* **Flask-CORS**: Para permitir requisições do frontend.

**Frontend (Interface do Usuário)**
* **HTML5, CSS3, JavaScript**: A base do projeto web.
* **Chart.js**: Para renderização de gráficos de linha com dados de cotação.
* **Luxon & chartjs-adapter-luxon**: Para manipulação de datas no gráfico.
* **Tailwind CSS**: Para o design e a estilização da interface.

---

### ⚙️ Como Rodar o Projeto

Siga estes passos para configurar e executar o projeto na sua máquina local.

**1. Pré-requisitos**

Certifique-se de ter o **Python** e o **Git** instalados na sua máquina.

**2. Clone o Repositório**

Abra o seu terminal ou prompt de comando e clone o projeto.

```bash
git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
cd SEU-REPOSITORIO

# FECART 2025 - Sistema de Previsão de Moedas BRICS+

## 📋 Descrição do Projeto

Sistema web desenvolvido para o evento acadêmico FECART 2025 que realiza análise preditiva de câmbio de moedas dos países BRICS+ em relação ao Real Brasileiro (BRL). A aplicação combina dados históricos de câmbio com análise de sentimento de notícias para gerar previsões de curto e médio prazo.

## ✨ Funcionalidades Principais

- **Análise de 12 Moedas**: Rússia, Índia, China, África do Sul, Argentina, Egito, Arábia Saudita, EUA, União Europeia, Japão, Reino Unido e Emirados Árabes Unidos
- **Previsões Multiperíodo**: 1 mês, 3 meses e 6 meses
- **Análise de Sentimento**: Integração com API de notícias para análise de contexto econômico
- **Modelo Ensemble**: Combinação de múltiplos algoritmos preditivos
- **Visualização Interativa**: Gráficos dinâmicos e interface responsiva
- **Indicadores de Confiabilidade**: Métricas de risco e confiabilidade das previsões

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **Flask-CORS** - Controle de requisições cross-origin
- **scikit-learn** - Algoritmos de machine learning
- **requests** - Requisições HTTP para APIs externas

### Frontend
- **HTML5/CSS3/JavaScript** - Estrutura base
- **Tailwind CSS** - Framework de estilização
- **Chart.js** - Visualização de gráficos
- **Font Awesome** - Ícones

### APIs Externas
- **AwesomeAPI** - Dados históricos de câmbio
- **NewsAPI** - Notícias para análise de sentimento

## 📁 Estrutura do Projeto

```
fecart-2025/
├── app_B.py                 # Aplicação Flask principal
├── requirements.txt         # Dependências Python
├── index_F.html            # Página principal de análise
├── home_F.html             # Página inicial com slideshow
├── app.js                  # Lógica frontend
├── style.css               # Estilos adicionais
└── README.md               # Este arquivo
```

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação e Execução

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd fecart-2025
```

2. **Instale as dependências Python**:
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação Flask**:
```bash
python app_B.py
```

4. **Acesse a aplicação**:
   - Abra o navegador e acesse: `http://127.0.0.1:5000`
   - A página inicial (`home_F.html`) será carregada automaticamente

## 📊 Modelos Preditivos Implementados

O sistema utiliza uma abordagem ensemble que combina:

1. **Modelo de Tendência por Média Móvel** - Análise de tendências recentes
2. **Modelo de Média Simples** - Baseado na média dos últimos 7 dias
3. **Regressão Linear com Sentimento** - Incorpora análise de notícias

## 🌐 Países e Moedas Suportadas

| País | Moeda | Código |
|------|-------|--------|
| Rússia | Rublo Russo | RUB |
| Índia | Rúpia Indiana | INR |
| China | Yuan Chinês | CNY |
| África do Sul | Rand Sul-Africano | ZAR |
| Argentina | Peso Argentino | ARS |
| Egito | Libra Egípcia | EGP |
| Arábia Saudita | Riyal Saudita | SAR |
| Estados Unidos | Dólar Americano | USD |
| União Europeia | Euro | EUR |
| Japão | Iene Japonês | JPY |
| Reino Unido | Libra Esterlina | GBP |
| Emirados Árabes Unidos | Dirham | AED |

## 👥 Equipe do Projeto

### Alunos
- Beatriz Aysha de Lima São Bernardo
- Miguel Rodrigues Pereira Francisco
- Rafael Riquena Salto
- Vitor Yuji Aguiar Marques Kurahassi

### Professores Supervisores
- Claudineia de Araujo Jacob
- Glenarison Luiz Ferreira
- Katia Milani Lara Bossi
- Luis Fernando dos Santos Pires
- Robson de Oliveira Cardoso

## ⚠️ Observações Importantes

- **Propósito Acadêmico**: Desenvolvido para fins educacionais no contexto da FECAP
- **Limitações das APIs**: Algumas chaves de API podem ter limites de uso
- **Previsões**: Resultados são simulados e não devem ser utilizados para decisões financeiras reais

## 🔧 Configuração de APIs

Para funcionamento completo, configure as chaves de API no arquivo `app_B.py`:

```python
NEWS_API_KEYS = [
    "sua_chave_newsapi_1",
    "sua_chave_newsapi_2"
]
```

## 📞 Suporte

Em caso de dúvidas ou problemas técnicos, entre em contato com a equipe do projeto ou os professores responsáveis.

---

**FECART 2025** - Projeto Acadêmico de Inteligência Artificial
**FECAP** - Fundação Escola de Comércio Álvares Penteado
*Desenvolvido para o evento FECART 2025*