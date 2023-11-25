// Fungsi untuk mengelompokkan data berdasarkan tanggal
function groupDataByDate(data) {
    const groupedData = {};
    data.forEach(item => {
        if (!groupedData[item.date]) {
            groupedData[item.date] = [];
        }
        groupedData[item.date].push(item);
    });
    return groupedData;
}

// Fungsi untuk membuat chart
function createChart(data) {
    const groupedData = groupDataByDate(data);

    // Mengumpulkan label tanggal
    const dates = Object.keys(groupedData);

    // Mengumpulkan data untuk setiap kata kunci
    const datasets = [];
    data.forEach(item => {
        const keywordIndex = datasets.findIndex(dataset => dataset.label === item.keyword);
        if (keywordIndex === -1) {
            datasets.push({
                label: item.keyword,
                data: [item.count],
                backgroundColor: randomColor() // Fungsi untuk mendapatkan warna acak
            });
        } else {
            datasets[keywordIndex].data.push(item.count);
        }
    });

    // Membuat chart
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Fungsi untuk mendapatkan warna acak
function randomColor() {
    return '#' + Math.floor(Math.random()*16777215).toString(16);
}

document.addEventListener('DOMContentLoaded', (event) => {
    const ctx2 = document.getElementById('myChart2');
    const allKeywordButton = document.getElementById('allKeyword');
    const topicIdString = document.getElementById('data-container').getAttribute('data-topicid');
    const topicId = parseInt(topicIdString);

    let myChart;

    function destroyChart() {
        if (myChart) {
            myChart.destroy();
        }
    }


    fetch(`/get_peak_time_data/${topicId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data); // Data yang diambil dari server
            createChart(data)
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });


    function fetchDataAndRender(labels, dataCallback) {
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
                    console.error('Dataset not found for topicId:', 2);
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    var selectedButtons = ['allKeyword']; 

    function updateChartBasedOnSelection() {
        let labels = [];
        let selectedDataCallback;

        if (selectedButtons.includes('allKeyword')) {
            labels = ['Prabowo', 'Ganjar', 'Anies'];
            selectedDataCallback = (dataset) => {
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
            };
        } else {
            labels = selectedButtons.map(button => button.charAt(0).toUpperCase() + button.slice(1));

            selectedDataCallback = (dataset) => {
                const data = selectedButtons.map(button => {
                    const sentimentData = dataset[button];
                    return [sentimentData.positif, sentimentData.negatif, sentimentData.netral];
                });

                const backgroundColors = ['#00E096', '#EE1E1E', '#979797'];

                return [
                    {
                        label: 'Positive',
                        data: data.map(value => value[0]),
                        backgroundColor: backgroundColors[0],
                        borderColor: backgroundColors[0],
                        borderWidth: 1
                    },
                    {
                        label: 'Negative',
                        data: data.map(value => value[1]),
                        backgroundColor: backgroundColors[1],
                        borderColor: backgroundColors[1],
                        borderWidth: 1
                    },
                    {
                        label: 'Netral',
                        data: data.map(value => value[2]),
                        backgroundColor: backgroundColors[2],
                        borderColor: backgroundColors[2],
                        borderWidth: 1
                    }
                ];                
            };
        }

        fetchDataAndRender(labels, selectedDataCallback);
    }

    allKeywordButton.classList.add('active'); 
    updateChartBasedOnSelection(); 

    document.querySelectorAll('.filter-button').forEach(function (button) {
        button.addEventListener('click', function () {
            if (button.id === 'allKeyword') {
                selectedButtons = [button.id];
            } else {
                var index = selectedButtons.indexOf(button.id);
                if (index === -1) {
                    if (selectedButtons.includes('allKeyword')) {
                        selectedButtons = [button.id];
                    } else if (selectedButtons.length < 2) {
                        selectedButtons.push(button.id);
                    } else {
                        selectedButtons = [button.id];
                    }
                } else {
                    selectedButtons.splice(index, 1);
                }
            }

            document.querySelectorAll('.filter-button').forEach(function (btn) {
                btn.classList.remove('active');
            });

            selectedButtons.forEach(function (selectedButton) {
                document.getElementById(selectedButton).classList.add('active');
            });

            updateChartBasedOnSelection();
        });
    });
});
