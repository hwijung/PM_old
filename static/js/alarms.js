$(document).ready( function()
{
	var btnCreateEntry = $("#id_btn_create");

	btnCreateEntry.click( function (event ) {
		document.location.href = '/alarms/create'; 
	});
	
	// Activate button clicked
	$("#id_alarm_btn_group ul li a").click(function() {
		alarm_name = $(this).attr("name");
		id_of_clicked_button = "#id_btn_activate_" + alarm_name;
		$(id_of_clicked_button).contents().get(0).nodeValue = $(this).text() + " ";

		if ( $(this).text() == "Activate" ) {
			$(id_of_clicked_button).addClass( "btn-success" );
			$(id_of_clicked_button).removeClass( "btn-danger" );
			activateAlarm( alarm_name, "ON" );
		} else {
			$(id_of_clicked_button).addClass( "btn-danger" );
			$(id_of_clicked_button).removeClass( "btn-success" );	
			activateAlarm( alarm_name, "OFF" );
		}
	} );

} );

function activateAlarm( alarm_name, on ) {
	var requestURL = "/alarms/activate/";
	var jqXHR = $.ajax ( {
		xhr: function () {
			var xhrobj = $.ajaxSettings.xhr();
			return xhrobj;
		},
		url: requestURL,
		headers: { "X-CSRFToken": $.cookie('csrftoken') },
		type: "POST",
		cache: false,
		data: { alarm_name: alarm_name, activate: on },
		success: function( result ) {
			return jQuery.parseJSON( result );
		}
	});
}


function edit_click (clicked_id) {
	document.location.href = '/alarms/' + clicked_id;
}

function delete_click( clicked_id ) {
	var result = confirm('Are you sure you want to do this?');
	
	if ( result ) {
		$.ajax({
			url: '/alarms/' + clicked_id + '/',
			type: 'DELETE',
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
		    },
		    success: function(result) {
		    	// Delete it from the table
		    	result = jQuery.parseJSON ( result );
		    	if ( result.result == "success" ) {
		    		$("#id_btn_edit_" + clicked_id ).parent().parent().remove();
		            	    		
		    		if ( $("#id_alarm tbody tr").length == 0 ) {
		    			$("#id_alarm").remove();
		    			$("#id_alarm_list").append("<p>No monitoring site found.</p>");
	               	}
	           	}
		    }
		});
	}
}