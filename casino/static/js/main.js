function placeBet(clicked_id){
	var cpk = clicked_id.substring(7);
	var tmp = clicked_id.substring(3,7);
	var cpk;
	if (tmp.localeCompare("Home") == 0){
		bet = "1";
	}
	else if (tmp.localeCompare("Draw") == 0){
		bet = "X";
	} else {
		bet = "2";
	}
  var elem = document.getElementById(clicked_id);
  elem.innerHTML = '<span id="glyphBtn" class="glyphicon glyphicon-ok"></span>';
	$.ajax({
				url: "/place-bet/",
				type: 'POST',
				data: {
					'bet': bet,
					'match_pk': cpk,
					csrfmiddlewaretoken: CSRF_TOKEN,
				},
			success: function(response) {
  				result = JSON.parse(response);  // Get the results sended from ajax to here
  				if (result.error) {
      				// Error
      				alert(result.error_text);
  				} else {
              // Success
      			}
  			}
		});
}