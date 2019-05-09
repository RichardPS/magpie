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
        var form_management = $('#id_form-TOTAL_FORMS');

        var newElement = $(selector).clone(true);
        var desc = $(newElement).find('input:eq(0)');
        var qty = $(newElement).find('input:eq(1)');
        var price = $(newElement).find('input:eq(2)');

        $(desc).attr('id', 'id_form-' + x + '-item_name');
        $(desc).attr('name', 'form-' + x + '-item_name');
        $(desc).attr('required', 'required');
        $(desc).val('');

        $(qty).attr('id', 'id_form-' + x + '-item_qty');
        $(qty).attr('name', 'form-' + x + '-item_qty');
        $(qty).attr('required', 'required');
        $(qty).val('');

        $(price).attr('id', 'id_form-' + x + '-item_price');
        $(price).attr('name', 'form-' + x + '-item_price');
        $(price).attr('required', 'required');
        $(price).val('');

        $(selector).after(newElement);

        x++;

        $(form_management).val(x);

        if(x > 1 && x < 3){
            showRemoveBtn();
        }

    }

    function removeItemRow(){
        var selector = $('.item-row:last');
        var form_management = $('#id_form-TOTAL_FORMS');

        $(selector).remove();

        x--;

        $(form_management).val(x);

        if(x < 2){
            hideRemoveBtn();
        }
    }

    function addRequired(){
        console.log('got here');
        $('.item-row > li').children('input').each(function(){
            console.log('each');
            $(this).attr('required', 'required');
        });
    }

    $(document).on('click', '.add-row', function(e){
        e.preventDefault();
        addItemRow();
    });

    $(document).on('click', '.remove-row', function(e){
        e.preventDefault();
        removeItemRow();
    });

    addRequired();

});
