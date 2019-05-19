$(function(){

    var inital = ''
    var surname = ''

    $('#id_first_name').change(function(){
        fn = $(this).val();
        inital = fn.charAt(0).toLowerCase();
        updateUsername()
    });

    $('#id_last_name').change(function(){
        ln = $(this).val()
        surname = ln.toLowerCase();
        updateUsername()
    });


    function updateUsername(){
        $('#id_username').val(inital + '.' + surname);
    }

});
