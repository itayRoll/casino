function placeBet(clicked_id, match_start){
  // now = Date.now();
  // if (now > match_start){
  //   alert("past");
  //   return;
  // } else {
  //   alert("future");
  // }
  document.getElementById(clicked_id).disabled = true;
	var cpk = clicked_id.substring(7);
	var tmp = clicked_id.substring(3,7);
	if (tmp.localeCompare("Home") == 0){
		bet = "1";
    document.getElementById("bet".concat("Draw").concat(cpk)).disabled = false;
    document.getElementById("bet".concat("Away").concat(cpk)).disabled = false;
	}
	else if (tmp.localeCompare("Draw") == 0){
		bet = "X";
    document.getElementById("bet".concat("Home").concat(cpk)).disabled = false;
    document.getElementById("bet".concat("Away").concat(cpk)).disabled = false;
	} else {
		bet = "2";
    document.getElementById("bet".concat("Home").concat(cpk)).disabled = false;
    document.getElementById("bet".concat("Draw").concat(cpk)).disabled = false;
	}
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

function disableUserBtn(cpk, user_bet){
  alert("shit");
  if (user_bet.localeCompare("1") == 0){
    document.getElementById("bet".concat("Home").concat(cpk)).disabled = true;
  }
  else if (user_bet.localeCompare("X") == 0){
    document.getElementById("bet".concat("Draw").concat(cpk)).disabled = true;
  }
  else {
    document.getElementById("bet".concat("Away").concat(cpk)).disabled = true;
  }
}