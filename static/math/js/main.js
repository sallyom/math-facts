//  Create support for HTML5 autofocus (IE9 and below) //
$(document).ready(function() {
if ( !("autofocus" in document.createElement("input")) ) {
        $("[autofocus]").focus();
    }
});
