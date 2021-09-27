/*
https://github.com/xdan/datetimepicker
https://xdsoft.net/jqplugins/datetimepicker/
*/
$(document).ready(function () {
    console.log("I'm here!");
    $.datetimepicker.setLocale('en');
    $("#datetimepicker-start").datetimepicker({
        format: "d-m-Y H:i O",
        minDate: "0",
    });
    $("#datetimepicker-end").datetimepicker({
        format: "d-m-Y H:i O",
        minDate: "0",
    });
});
