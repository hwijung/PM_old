$(document).ready( function()
{
	var btnCreateEntry = $("#id_btn_create");

	btnCreateEntry.click( function (event ) {
		document.location.href = '/alarms/create'; 
	});

} );