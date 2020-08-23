
$(function() {
    $('a#process_input').bind('click', function(){
        place = autocomplete.getPlace()
        console.log(place)
        if(!place) {
            return false;
        }
        else {
            var val = getDataFromSelection(place);
        }
        console.log(place)

        $.getJSON('/background_process', {
            location: val,
        }, function(data) {
            console.log('got here')
            var testArray = data.result.join(' ')
            sessionStorage.setItem('myArray', testArray);
            window.location.href = "/result/";
        });
        return false;
    });
});

var time_range = document.getElementsByClassName('time-range')[0];


$(function() {
    $('a#process_heat_map').bind('click', function(){
        $.getJSON('/heat_map_process', {
            time_range: time_range.textContent,
        }, function(data) {
            if (time_range.textContent == 'Time Range: Today'){
                window.location.href = "/map_day/";
            } else if (time_range.textContent == 'Time Range: One Week'){
                window.location.href = "/map_week/";
            } else if (time_range.textContent == 'Time Range: One Month'){
                window.location.href = "/map_month/";
            } else if (time_range.textContent == 'Time Range: Total'){
                window.location.href = "/map_total/";
            }
            console.log('got-here')
        });
        return false;
    });
});

var dropdown = document.getElementsByClassName('wrapper-dropdown-1')[0];
dropdown.addEventListener("click", dropDown);

function dropDown(){
    if (dropdown.classList.contains("active")){
        dropdown.classList.remove('active');
    } else {
        dropdown.classList.add('active');
    }
  }


 
var today = document.getElementsByClassName('today')[0];
var one_week = document.getElementsByClassName('one-week')[0];
var one_month = document.getElementsByClassName('one-month')[0];
var total = document.getElementsByClassName('total')[0];
var time_range = document.getElementsByClassName('time-range')[0];

today.addEventListener('click', todayz);
one_week.addEventListener('click', one_weekz);
one_month.addEventListener('click', one_monthz);
total.addEventListener('click', totalz);

function todayz(){
    console.log('got-here');
    time_range.textContent = 'Time Range: Today';
}

function one_weekz(){
    time_range.textContent = 'Time Range: One Week';
}

function one_monthz(){
    time_range.textContent = 'Time Range: One Month';
}

function totalz(){
    time_range.textContent = 'Time Range: Total';
}




var autocomplete;

function initAutoComplete() {
  var input = document.getElementById('searchTextField');
  autocomplete = new google.maps.places.Autocomplete(input, {types : ["geocode"]});
  autocomplete.setFields(["address_component"]);
  console.log("Got here")
}

function getDataFromSelection(place) {
  for(const component of place.address_components) {
    if(component.types[0] == "administrative_area_level_2") {
      var name = component.long_name
      var pos = name.indexOf(" County")
      var county = name.substring(0, pos)
    }
    else if(component.types[0] == "administrative_area_level_1") {
      var state = component.long_name
    }
  }

  console.log(county + "," + state)
  return county + "," + state
}
