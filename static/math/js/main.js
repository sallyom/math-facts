$(document).ready(function() {
//  Create support for HTML5 autofocus (IE9 and below)
	if ( !("autofocus" in document.createElement("input")) ) {
	        $("[autofocus]").focus();
    }
// Hide warnings on click event
    $( ".warning" ).click(function( event ) {
        event.preventDefault();
        $( this ).hide();
    });
});
