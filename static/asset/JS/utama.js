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
var sa = null;
function getChart(){
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
}

function getNetwork(){
  var width = (document.getElementById("coeg")).offsetWidth,
    height = 500;

  var svg = d3.select("#coeg").append("svg")
      .attr("width", width)
      .attr("height", height);

  var force = d3.layout.force()
      .gravity(.05)
      .distance(500)
      .charge(-100)
      .size([width, height]);

  d3.json("http://127.0.0.1:5000/ujiTampilan/json", function(json) {
      console.log(json);
    force
        .nodes(json.nodes)
        .links(json.links)
        .start();

    var link = svg.selectAll(".link")
        .data(json.links)
      .enter().append("line")
        .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

    var node = svg.selectAll(".node")
        .data(json.nodes)
      .enter().append("g")
        .attr("class", "node")
        .call(force.drag);

    node.append("circle")
        .attr("r","5");

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });
  });

  /* Tab */
  function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }
}

function getImage(){

}

function submitSearch(){
  var content = document.getElementById("content");
  content.style.display = "inherit";
  data = document.getElementById("in");
  console.log(JSON.stringify({"search" : data.value}));
  /*fetch("http://127.0.0.1:5000/search",{
    method : "POST",
    headers: {
      "Content-Type": "application/json",
      // "Content-Type": "application/x-www-form-urlencoded",
    },
    body:{"search" : data.value},
  }).then(response => {
    console.log(response);
  });*/
  document.getElementById("coeg").innerHTML = "";
  getChart();
  getNetwork();
  return false;
}

if(debug){
  console.log(sb.offsetWidth);
  console.log(inp.offsetWidth);
  console.log(fl_10.offsetWidth);
  console.log(fl_10.offsetWidth - (inp.offsetWidth + sb.offsetWidth));

  console.log((fl_4.offsetWidth - img.offsetWidth));
}