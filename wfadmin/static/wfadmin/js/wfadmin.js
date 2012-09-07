/*** drag & drop sortings in admin inline ***/
jQuery(function($) {
    $('div.inline-group').sortable({
        items: 'tr.has_original',
        handle: 'td',
        update: function() {
           $(this).find('tr.has_original').each(function(i) {
               $(this).find('input[name$=order]').val(i+1);
               $(this).removeClass('row1').removeClass('row2');
               $(this).addClass('row'+((i%2)+1));
           });
        }
    });
    $('.module table').find('input[id$=order]').parent('td').hide();
    $('.module table thead th:eq(2)').hide();
    $('tr.has_original').css('cursor', 'move');
})
