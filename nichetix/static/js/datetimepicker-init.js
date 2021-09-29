/*
https://github.com/xdan/datetimepicker
https://xdsoft.net/jqplugins/datetimepicker/

datetimepicker configuration
*/
$(document).ready(function () {
    $.datetimepicker.setLocale('en');
    $("#datetimepicker-start").datetimepicker({
        format: "d-m-Y H:i",
        minDate: "0",
    });
    $("#datetimepicker-end").datetimepicker({
        format: "d-m-Y H:i",
        minDate: "0",
    });
});
