$(function(){

    $('.icon-font').each(function(){

        letter = $(this).text();
        if(letter == 'F'){
            $(this).css('color', '#f00')
        }else{
            $(this).css('color', '#070')
        }
    });

});
