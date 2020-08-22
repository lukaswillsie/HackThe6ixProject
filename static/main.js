
$(function() {
    $('a#process_input').bind('click', function(){
        $.getJSON('/background_process', {
            location: $('input[name="location"]').val(),
        }, function(data) {
            console.log('got here')
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
