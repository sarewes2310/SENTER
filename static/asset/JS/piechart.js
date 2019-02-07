var ctx = document.getElementById('myChart').getContext('2d');
fetch("http://127.0.0.1:5000/ujiChart/json").then(response => {
  console.log("TEST");
  //console.log(response.json());
  return response.json();
}).then(hasil => {
  console.log(hasil.P+1);
  var chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'pie',

      // The data for our dataset
      data: {
          labels: ["Positif", "Negatif", "Netral"],
          datasets: [{
              label: "My First dataset",
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
              ],
              borderColor: 'rgb(25, 99, 132)',
              data: [hasil.P,hasil.N,hasil.L],
          }]
      },

      // Configuration options go here
      options: {}
  });
});