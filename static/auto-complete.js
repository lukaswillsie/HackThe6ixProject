function initAutoComplete() {
  var input = document.getElementById('searchTextField');
  autocomplete = new google.maps.places.Autocomplete(input, {types : ["geocode"]});
  autocomplete.setFields(["address_component"]);
  autocomplete.addListener("place_changed", getDataFromSelection);
  console.log("Got here")
}

function getDataFromSelection() {
  const place = autocomplete.getPlace();
  console.log(place.address_components);
}
  
  // google.maps.event.addDomListener(window, 'load', initialize);