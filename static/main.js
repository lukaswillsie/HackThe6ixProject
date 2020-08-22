
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