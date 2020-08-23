var daily_cases = document.getElementsByClassName('daily-cases')[0];
var daily_deaths = document.getElementsByClassName('daily-deaths')[0];
var total_cases = document.getElementsByClassName('total-cases')[0];
var total_deaths = document.getElementsByClassName('total-deaths')[0];
var weekly_cases = document.getElementsByClassName('weekly-cases')[0];
var weekly_deaths = document.getElementsByClassName('weekly-deaths')[0];
var monthly_cases = document.getElementsByClassName('monthly-cases')[0];
var monthly_deaths = document.getElementsByClassName('monthly-deaths')[0];

// $.getJSON("../static/stats.json", function(json) {
    // console.log('starting');
    // data = json.data;
    // console.log(data)
    
// });


var data = sessionStorage.getItem('myArray').split(' ');
console.log(data);
daily_cases.textContent = data[2]
daily_deaths.textContent = data[3];
total_cases.textContent = data[0];
total_deaths.textContent = data[1];
weekly_cases.textContent = data[4];
weekly_deaths.textContent = data[5];
monthly_cases.textContent = data[6];
monthly_deaths.textContent = data[7];

var arr1 = ['sa-warning1', 'sa-warning2', 'sa-warning3', 'sa-warning4']
var arr2 = ['sa-success1', 'sa-success2', 'sa-success3', 'sa-success4']

var act1 = document.getElementsByClassName('activity1')[0];
var act2 = document.getElementsByClassName('activity2')[0];
var act3 = document.getElementsByClassName('activity3')[0];
var act4 = document.getElementsByClassName('activity4')[0];

var arr3 = [act1, act2, act3, act4]

var i;
for (i = 8; i < 12; i++) {

  if  (arr3[i - 8].classList.contains("success")) {
    arr3[i - 8].classList.remove("success");
  }
  if  (arr3[i - 8].classList.contains("warning")) {
    arr3[i - 8].classList.remove("warning");
  }
  if (data[i] == 'Yes') {
      arr3[i - 8].classList.add("success")
  } else if (data[i] == 'No') {
    arr3[i - 8].classList.add("warning")
  }
}







