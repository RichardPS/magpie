$(function(){

    x = 1;

    function showRemoveBtn(){
        var btnRemove = document.createElement('button');
        var btnText = document.createTextNode('Remove last item row');
        btnRemove.appendChild(btnText);
        btnRemove.className = 'remove-row';
        btnRemove.id = 'remove-row';

        document.getElementById('add-remove').appendChild(btnRemove);
    }

    function hideRemoveBtn(){
        var btnRemove = document.getElementById('remove-row').remove();

    }

    function addItemRow(){
        console.log('Add Row Fired');

        var selector = $('.item-row:last');

        var newElement = $(selector).clone(true);
        var desc = $(newElement).find('.desc-col input');
        var qty = $(newElement).find('.qty-col input');
        var price = $(newElement).find('.price-col input');

        $(desc).attr('id', 'id_form-' + x + '-item_name');
        $(desc).attr('name', 'form-' + x + '-item_name');
        $(desc).val('');

        $(qty).attr('id', 'id_form-' + x + '-item_qty');
        $(qty).attr('name', 'form-' + x + '-item_qty');
        $(qty).val('');

        $(price).attr('id', 'id_form-' + x + '-item_price');
        $(price).attr('name', 'form-' + x + '-item_price');
        $(price).val('');

        $(selector).after(newElement);

        x++;

        if(x > 1 && x < 3){
            showRemoveBtn();
        }

    }

    function removeItemRow(){
        var selector = $('.item-row:last');

        $(selector).remove();

        x--;

        if(x < 2){
            hideRemoveBtn();
        }
    }


    $(document).on('click', '.add-row', function(e){
        e.preventDefault();
        addItemRow();
    });

    $(document).on('click', '.remove-row', function(e){
        e.preventDefault();
        removeItemRow();
    });

});
