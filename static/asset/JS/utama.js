var debug = true;
window.onscroll = () => {
    myFunction()
};

// Get the navbar
var navbar = document.getElementById("navbar");

console.log(navbar);
// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
} 
var fl_10 = document.getElementById("fl-10");
var fl_4 = document.getElementById("fl-4");
var wr = document.getElementById("wr");
var inp = document.getElementById("in");
var sb = document.getElementById("sb");
var img = document.getElementById("img");

wr.style.marginLeft = ((fl_10.offsetWidth - (inp.offsetWidth + sb.offsetWidth)) / 2).toString() + "px";

img.style.marginLeft =((fl_4.offsetWidth - img.offsetWidth) / 2).toString() + "px";

var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'pie',

    // The data for our dataset
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "My First dataset",
            backgroundColor: 'rgb(25, 255, 255)',
            borderColor: 'rgb(25, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }]
    },

    // Configuration options go here
    options: {}
});
var ctx_1 = document.getElementById('myChart_1').getContext('2d');
var chart_1 = new Chart(ctx_1, {
  // The type of chart we want to create
  type: 'line',

  // The data for our dataset
  data: {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [{
          label: "My First dataset",
          backgroundColor: 'rgb(255, 255, 132)',
          borderColor: 'rgb(255, 99, 132)',
          data: [0, 10, 5, 2, 20, 30, 45],
      }]
  },

  // Configuration options go here
  options: {}
});

if(debug){
  console.log(sb.offsetWidth);
  console.log(inp.offsetWidth);
  console.log(fl_10.offsetWidth);
  console.log(fl_10.offsetWidth - (inp.offsetWidth + sb.offsetWidth));

  console.log((fl_4.offsetWidth - img.offsetWidth));
}