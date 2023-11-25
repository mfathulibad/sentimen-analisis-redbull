document.addEventListener('DOMContentLoaded', (event) => {
    const ctx2 = document.getElementById('myChart2');
    const allKeywordButton = document.getElementById('allKeyword');
    const prabowoButton = document.getElementById('prabowo');
    const ganjarButton = document.getElementById('ganjar');
    const aniesButton = document.getElementById('anies');

    let myChart;

    function destroyChart() {
        if (myChart) {
            myChart.destroy();
        }
    }

    function fetchDataAndRender(topicId, labels, dataCallback) {
        destroyChart();

        fetch('/get_sentiment_data')
            .then(response => response.json())
            .then(data => {
                const dataset = data.find(item => item.topicId === topicId);

                if (dataset) {
                    const chartData = dataCallback(dataset);

                    myChart = new Chart(ctx2, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: chartData
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                } else {
                    console.error('Dataset not found for topicId:', topicId);
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    function renderAllKeywordChart() {
        const labels = ['Prabowo', 'Ganjar', 'Anies'];
        const topicId = 2;

        fetchDataAndRender(topicId, labels, (dataset) => {
            const positiveData = [dataset.prabowo.positif, dataset.ganjar.positif, dataset.anies.positif];
            const negativeData = [dataset.prabowo.negatif, dataset.ganjar.negatif, dataset.anies.negatif];
            const neutralData = [dataset.prabowo.netral, dataset.ganjar.netral, dataset.anies.netral];

            return [
                {
                    label: 'Positif',
                    data: positiveData,
                    backgroundColor: ['#00E096'],
                    borderColor: ['#00E096'],
                    borderWidth: 1
                },
                {
                    label: 'Negatif',
                    data: negativeData,
                    backgroundColor: ['#EE1E1E'],
                    borderColor: ['#EE1E1E'],
                    borderWidth: 1
                },
                {
                    label: 'Netral',
                    data: neutralData,
                    backgroundColor: ['#979797'],
                    borderColor: ['#979797'],
                    borderWidth: 1
                }
            ];
        });
    }

    //default all keywoard
    renderAllKeywordChart();

    allKeywordButton.addEventListener('click', renderAllKeywordChart);

    prabowoButton.addEventListener('click', function() {
        const labels = ['Prabowo'];
        const topicId = 2;

        fetchDataAndRender(topicId, labels, (dataset) => {
            const positive = [dataset.prabowo.positif];
            const negative = [dataset.prabowo.negatif];
            const netral = [dataset.prabowo.netral];

            return [
                {
                    label: 'Positif',
                    data: positive,
                    backgroundColor: ['#00E096'],
                    borderColor: ['#00E096'],
                    borderWidth: 1
                },
                {
                    label: 'Negatif',
                    data: negative,
                    backgroundColor: ['#EE1E1E'],
                    borderColor: ['#EE1E1E'],
                    borderWidth: 1
                },
                {
                    label: 'Netral',
                    data: netral,
                    backgroundColor: ['#979797'],
                    borderColor: ['#979797'],
                    borderWidth: 1
                }
            ];
        });
    });

    ganjarButton.addEventListener('click', function() {
        const labels = ['Ganjar'];
        const topicId = 2;

        fetchDataAndRender(topicId, labels, (dataset) => {
            const positive = [dataset.ganjar.positif];
            const negative = [dataset.ganjar.negatif];
            const netral = [dataset.ganjar.netral];

            return [
                {
                    label: 'Positif',
                    data: positive,
                    backgroundColor: ['#00E096'],
                    borderColor: ['#00E096'],
                    borderWidth: 1
                },
                {
                    label: 'Negatif',
                    data: negative,
                    backgroundColor: ['#EE1E1E'],
                    borderColor: ['#EE1E1E'],
                    borderWidth: 1
                },
                {
                    label: 'Netral',
                    data: netral,
                    backgroundColor: ['#979797'],
                    borderColor: ['#979797'],
                    borderWidth: 1
                }
            ];
        });
    });

    aniesButton.addEventListener('click', function() {
        const labels = ['Anies'];
        const topicId = 2;

        fetchDataAndRender(topicId, labels, (dataset) => {
            const positive = [dataset.anies.positif];
            const negative = [dataset.anies.negatif];
            const netral = [dataset.anies.netral];

            return [
                {
                    label: 'Positif',
                    data: positive,
                    backgroundColor: ['#00E096'],
                    borderColor: ['#00E096'],
                    borderWidth: 1
                },
                {
                    label: 'Negatif',
                    data: negative,
                    backgroundColor: ['#EE1E1E'],
                    borderColor: ['#EE1E1E'],
                    borderWidth: 1
                },
                {
                    label: 'Netral',
                    data: netral,
                    backgroundColor: ['#979797'],
                    borderColor: ['#979797'],
                    borderWidth: 1
                }
            ];
        });
    });
});
