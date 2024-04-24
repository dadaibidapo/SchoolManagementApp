const ctx = document.getElementById('chart').getContext('2d');

$.ajax({
    url:'/graph-data',
    dataType:'json',
    success:function(data){
        console.log('Data received', data);

        
        const labels = data.labels;
        const datasets = data.datasets[0].data;

        
        console.log(labels);
        console.log(datasets);

        new Chart(ctx, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [{
                label: 'Summary of School Data ',
                data: datasets,
                borderWidth: 3,
              //   backgroundColor: 'rgb(255,99,132)',
                // backgroundColor: ['red','blue', 'yellow', 'green', 'purple', 'orange', 'black'],
                borderColor: 'rgba(255, 99, 132, 0.8)'
              },
            ]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              },
              plugins: {
                datalabels: {
                    anchor: 'end',
                    align: 'top',
                    formatter: function(value, context) {
                        return value; // Display the actual value on the bar
                    }
                }
            }
            }
          });
  
    },
    error:function(Xhr, status, error){
        console.error("Error while fetching the data: ", error);
    }
})