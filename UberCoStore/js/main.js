$(document).ready(function () {
    $(document).bind("contextmenu", function(e) {
        return false;
    });
    
//    $("#item-to-add").focus();
//
//    $("#item-to-add").focus().bind('blur', function() {
//        $(this).focus();
//    });
//
//    $("html").click(function() {
//        $("#item-to-add").val($("#item-to-add").val()).focus();
//    });
//    
//    setTimeout(function(){ $("#item-to-add").focus(); }, 200);
//
//    //disable the tab key
//    $(document).keydown(function(objEvent) {
//        if (objEvent.keyCode == 9) {  //tab pressed
//            objEvent.preventDefault(); // stops its action
//        }
//    })
});