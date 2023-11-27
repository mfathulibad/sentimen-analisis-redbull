// Fungsi untuk menggambar chart
function drawChart(data) {
    // Mengurutkan data berdasarkan tanggal
    data.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Mengambil data unik untuk tanggal
    const uniqueDates = [...new Set(data.map(item => item.date))];
    
    // Menginisialisasi data yang akan digunakan oleh Chart.js
    const chartData = {
        labels: uniqueDates,
        datasets: []
    };

    // Membuat dataset untuk setiap keyword
    const uniqueKeywords = [...new Set(data.map(item => item.keyword))];
    uniqueKeywords.forEach(keyword => {
        const keywordData = data.filter(item => item.keyword === keyword);
        const counts = uniqueDates.map(date => keywordData.find(item => item.date === date)?.count || 0);

        chartData.datasets.push({
        label: keyword,
        data: counts,
        fill: false,
        borderColor: getRandomColor(), // Fungsi untuk mendapatkan warna acak
        });
    });

    // Membuat chart menggunakan Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
        scales: {
            x: {
            type: 'category',
            labels: uniqueDates,
            title: {
                display: true,
                text: 'Tanggal'
            }
            },
            y: {
            title: {
                display: true,
                text: 'Count'
            }
            }
        }
        }
    });
}

// Fungsi untuk mendapatkan warna acak
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const ctx2 = document.getElementById('myChart2');
    const allKeywordButton = document.getElementById('allKeyword');
    const topicIdString = document.getElementById('data-container').getAttribute('data-topicid');
    const topicId = parseInt(topicIdString);
    var selectedButtons = ['allKeyword']; 

    let myChart;

    function destroyChart() {
        if (myChart) {
            myChart.destroy();
            myChartPeak.destroy();
        }
    }


    // fetch(`/get_peak_time_data/${topicId}`)
    //     .then(response => response.json())
    //     .then(data => {
            
    //         if (selectedButtons.includes('allKeyword')) {
    //             labels = ['Prabowo', 'Ganjar', 'Anies'];
    //             console.log("ini coy 1", labels)
    //             drawChart(data)
    //         } else {
    //             labels = selectedButtons.map(button => button.charAt(0).toUpperCase() + button.slice(1));
    //             console.log("ini coy 2", labels)
    //         }
    //         // console.log("ini label di data", labels)
            
    //     })
    //     .catch(error => {
    //         console.error('Error fetching data:', error);
    //     });


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

    
    function fetchDataAndRenderPeak(labels) {
        destroyChart();

        fetch(`/get_peak_time_data/${topicId}`)
            .then(response => response.json())
            .then(data => {
                let lowercaseLabels = labels.map(label => label.toLowerCase());
                let filteredData = data.filter(item => lowercaseLabels.includes(item.keyword));
                // Mengurutkan data berdasarkan tanggal
                filteredData.sort((a, b) => new Date(a.date) - new Date(b.date));

                // Mengambil data unik untuk tanggal
                const uniqueDates = [...new Set(filteredData.map(item => item.date))];
                
                // Menginisialisasi data yang akan digunakan oleh Chart.js
                const chartData = {
                    labels: uniqueDates,
                    datasets: []
                };

                // Membuat dataset untuk setiap keyword
                const uniqueKeywords = [...new Set(filteredData.map(item => item.keyword))];
                uniqueKeywords.forEach(keyword => {
                    const keywordData = filteredData.filter(item => item.keyword === keyword);
                    const counts = uniqueDates.map(date => keywordData.find(item => item.date === date)?.count || 0);

                    chartData.datasets.push({
                    label: keyword,
                    data: counts,
                    fill: false,
                    borderColor: getRandomColor(), // Fungsi untuk mendapatkan warna acak
                    });
                });

                // Membuat chart menggunakan Chart.js
                const ctx = document.getElementById('myChart').getContext('2d');
                myChartPeak = new Chart(ctx, {
                    type: 'line',
                    data: chartData,
                    options: {
                    scales: {
                        x: {
                        type: 'category',
                        labels: uniqueDates,
                        title: {
                            display: true,
                            text: 'Tanggal'
                        }
                        },
                        y: {
                        title: {
                            display: true,
                            text: 'Count'
                        }
                        }
                    }
                    }
                });
            
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }


    function updateChartBasedOnSelection() {
        let labels = [];
        let selectedDataCallback;

        if (selectedButtons.includes('allKeyword')) {
            labels = ['Prabowo', 'Ganjar', 'Anies'];

            console.log("semua", labels)

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

            console.log("selected", labels)

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
        fetchDataAndRenderPeak(labels)
        
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
