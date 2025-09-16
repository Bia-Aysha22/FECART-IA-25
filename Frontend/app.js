document.addEventListener('DOMContentLoaded', () => {
    const backendUrl = 'http://127.0.0.1:5000/api';

    const cardsContainer = document.getElementById('currency-cards');
    const analysisSection = document.getElementById('analysis-section');
    const loadingIndicator = document.getElementById('loading-indicator');
    const loadingText = document.getElementById('loading-text');

    let myChart;
    let currentCountry = '';

    // Mostrar loading
    const showLoading = (message = 'Processando dados...') => {
        loadingText.textContent = message;
        loadingIndicator.classList.remove('hidden');
    };

    // Esconder loading
    const hideLoading = () => {
        loadingIndicator.classList.add('hidden');
    };

    // Criar card de moeda
    const createCard = (country) => {
        const cardDiv = document.createElement('div');
        cardDiv.className = `currency-card bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer`;
        cardDiv.style.borderLeft = `8px solid ${country.color}`;
        cardDiv.innerHTML = `
            <div class="flex items-center space-x-4">
                <span class="text-4xl">${country.flag}</span>
                <div>
                    <h3 class="text-xl font-bold text-gray-800">${country.name}</h3>
                    <p class="text-sm text-gray-600">${country.moeda}</p>
                </div>
            </div
        `;
        cardDiv.addEventListener('click', () => analyzeCurrency(country.name));
        return cardDiv;
    };

    // Buscar lista de países
    const fetchCountries = async () => {
        try {
            const response = await fetch(`${backendUrl}/countries`);
            const countries = await response.json();

            if (cardsContainer) {
                cardsContainer.innerHTML = '';
                countries.forEach(country => {
                    const card = createCard(country);
                    cardsContainer.appendChild(card);
                });
            }
        } catch (error) {
            console.error('Erro ao buscar países:', error);
            if (cardsContainer) {
                cardsContainer.innerHTML = '<p class="text-red-500 text-center col-span-full">Erro ao carregar países</p>';
            }
        }
    };

    // Analisar moeda
    const analyzeCurrency = async (countryName) => {
        currentCountry = countryName;
        showLoading(`Analisando dados de ${countryName}...`);

        try {
            const response = await fetch(`${backendUrl}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ country: countryName }),
            });

            if (!response.ok) {
                throw new Error('Erro na análise');
            }

            const data = await response.json();
            renderAnalysis(data);
            analysisSection.classList.remove('hidden');

        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao analisar moeda. Verifique o backend.');
        } finally {
            hideLoading();
        }
    };

    // Renderizar análise
    const renderAnalysis = (data) => {
        const info = data.country_info;

        // Análse do País
        const countryDescriptionElement = document.getElementById('country-analysis-content').querySelector('p');
        countryDescriptionElement.textContent = data.country_info.description;

        // Atualizar elementos da página
        document.getElementById('currency-title').textContent = `${info.name} - ${info.moeda}`;
        document.getElementById('reliability-text').textContent = `Confiabilidade do modelo: ${data.reliability}%`;
        document.getElementById('country-flag').src = info.flag_img;
        document.getElementById('country-silhouette').src = info.silhouette;

        // Atualizar taxas
        document.getElementById('last-rate').textContent = data.last_rate.toFixed(4);
        document.getElementById('predicted-rate').textContent = data.predicted_rate_1m.toFixed(4);
        document.getElementById('predicted-rate-3months').textContent = data.predicted_rate_3m.toFixed(4);
        document.getElementById('predicted-rate-6months').textContent = data.predicted_rate_6m.toFixed(4);

        // Variação percentual
        const changePercent = document.getElementById('change-percent');
        changePercent.textContent = `${data.change >= 0 ? '+' : ''}${data.change.toFixed(2)}%`;
        changePercent.className = `text-2xl font-bold ${data.change >= 0 ? 'text-green-900' : 'text-red-900'}`;

        // Barra de confiabilidade
        const reliabilityBar = document.getElementById('reliability-bar');
        reliabilityBar.style.width = `${data.reliability}%`;
        reliabilityBar.className = `h-full transition-all duration-1000 ${getReliabilityColor(data.reliability)}`;

        document.getElementById('reliability-percent').textContent = `${data.reliability}%`;

        // Nível de risco
        const riskLevel = document.getElementById('risk-level-text');
        riskLevel.textContent = data.risk_level;
        riskLevel.className = `font-semibold ${getRiskColor(data.risk_level)}`;

        // Renderizar gráfico
        renderChart(data.historical_data, info, data);

        // Atualizar datas
        const today = new Date();
        document.getElementById('last-date').textContent = formatDate(today);
        document.getElementById('prediction-date').textContent = formatDate(addDays(today, 30));
        document.getElementById('prediction-date-3months').textContent = formatDate(addDays(today, 90));
        document.getElementById('prediction-date-6months').textContent = formatDate(addDays(today, 180));
        document.getElementById('risk-updated-text').textContent = `Última atualização: ${formatDateTime(today)}`;
    };

// Renderizar gráfico
// Renderizar gráfico
const renderChart = (historicalData, countryInfo, data) => {
    const ctx = document.getElementById('currency-chart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    // Dados de previsão
    const lastHistoricalPoint = historicalData[historicalData.length - 1];
    const today = new Date();
    const predictionPoint1m = {
        x: addDays(today, 30).toISOString(),
        y: data.predicted_rate_1m
    };
    const predictionPoint3m = {
        x: addDays(today, 90).toISOString(),
        y: data.predicted_rate_3m
    };
    const predictionPoint6m = {
        x: addDays(today, 180).toISOString(),
        y: data.predicted_rate_6m
    };

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Cotação Histórica',
                data: historicalData.map(d => ({
                    x: d.date,
                    y: d.value
                })),
                borderColor: countryInfo.color,
                backgroundColor: `${countryInfo.color}20`,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: countryInfo.color,
            }, {
                // Segmento de linha verde (Histórico -> 1 Mês)
                label: '',
                data: [{
                    x: lastHistoricalPoint.date,
                    y: lastHistoricalPoint.value
                }, predictionPoint1m],
                borderColor: '#22c55e',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                pointRadius: 0,
                showLine: true,
            }, {
                // Ponto da Previsão de 1 Mês (para a legenda)
                label: 'Previsão (1 Mês)',
                data: [predictionPoint1m],
                backgroundColor: '#22c55e',
                pointRadius: 6,
                pointBorderColor: '#fff',
                pointBackgroundColor: '#22c55e',
                pointHoverRadius: 8,
                showLine: false,
            }, {
                // Segmento de linha amarela (1 Mês -> 3 Meses)
                label: '',
                data: [predictionPoint1m, predictionPoint3m],
                borderColor: '#eab308',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                pointRadius: 0,
                showLine: true,
            }, {
                // Ponto da Previsão de 3 Meses (para a legenda)
                label: 'Previsão (3 Meses)',
                data: [predictionPoint3m],
                backgroundColor: '#eab308',
                pointRadius: 6,
                pointBorderColor: '#fff',
                pointBackgroundColor: '#eab308',
                pointHoverRadius: 8,
                showLine: false,
            }, {
                // Segmento de linha vermelha (3 Meses -> 6 Meses)
                label: '',
                data: [predictionPoint3m, predictionPoint6m],
                borderColor: '#ef4444',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                pointRadius: 0,
                showLine: true,
            }, {
                // Ponto da Previsão de 6 Meses (para a legenda)
                label: 'Previsão (6 Meses)',
                data: [predictionPoint6m],
                backgroundColor: '#ef4444',
                pointRadius: 6,
                pointBorderColor: '#fff',
                pointBackgroundColor: '#ef4444',
                pointHoverRadius: 8,
                showLine: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    mode: 'point',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'month',
                        tooltipFormat: 'dd/MM/yyyy',
                        displayFormats: {
                            day: 'dd/MM'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Data'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Valor (R$)'
                    }
                }
            }
        }
    });
};

    // Funções auxiliares
    const getReliabilityColor = (percent) => {
        if (percent >= 70) return 'bg-green-500';
        if (percent >= 40) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    const getRiskColor = (risk) => {
        if (risk === 'Baixo') return 'text-green-600';
        if (risk === 'Médio') return 'text-yellow-600';
        return 'text-red-600';
    };

    const formatDate = (date) => {
        return date.toLocaleDateString('pt-BR');
    };

    const formatDateTime = (date) => {
        return date.toLocaleString('pt-BR');
    };

    const addDays = (date, days) => {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    };

    // Event listeners
    document.getElementById('refresh-btn').addEventListener('click', () => {
        if (currentCountry) {
            analyzeCurrency(currentCountry);
        }
    });

    document.getElementById('change-currency-btn').addEventListener('click', () => {
        analysisSection.classList.add('hidden');
    });

    // Botões de período (exemplo simplificado)
    document.getElementById('btn-1month').addEventListener('click', () => {
        // Implementar filtro de período se necessário
    });

    // Inicializar
    fetchCountries();
});