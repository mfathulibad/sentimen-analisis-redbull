document.addEventListener('DOMContentLoaded', (event) => {
    // const ctx = document.getElementById('myChart');
    // new Chart(ctx, {
    //   type: 'bar',
    //   data: {
    //     labels: ['8 Okt', '12 Okt', '16 Okt', '20 Okt', '24 Okt', '28 Okt', '1 Nov'],
    //     datasets: [
    //       {
    //         label: 'Prabowo',
    //         data: [0, 0, 0, 0, 444, 0, 0], 
    //         backgroundColor: ['#E0CA00'],
    //         borderColor: ['#E0CA00'],
    //         borderWidth: 1
    //       },
    //       {
    //         label: 'Ganjar',
    //         data: [0, 0, 0, 0, 444, 0, 0], 
    //         backgroundColor: ['#1EEEC9'],
    //         borderColor: ['#1EEEC9'],
    //         borderWidth: 1
    //       },
    //       {
    //         label: 'Anies',
    //         data: [0, 0, 0, 0, 444, 0, 0], 
    //         backgroundColor: ['#DD65E8'],
    //         borderColor: ['#DD65E8'],
    //         borderWidth: 1
    //       }
    //     ]
    //   },
    //   options: {
    //     scales: {
    //       y: {
    //         beginAtZero: true
    //       }
    //     }
    //   }
    // });
   
    const ctx2 = document.getElementById('myChart2');
    fetch('/get_sentiment_data')  
        .then(response => response.json())
        .then(data => {
            const labels = ['Prabowo', 'Ganjar', 'Anies'];
            
            // topicId yang di ambil topicId2 
            const topicId = 2;
            const dataset = data.find(item => item.topicId === topicId);

            if (dataset) {
                const positiveData = [dataset.prabowo.positif, dataset.ganjar.positif, dataset.anies.positif];
                const negativeData = [dataset.prabowo.negatif, dataset.ganjar.negatif, dataset.anies.negatif];
                const neutralData = [dataset.prabowo.netral, dataset.ganjar.netral, dataset.anies.netral];

                new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
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
                        ]
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
});
