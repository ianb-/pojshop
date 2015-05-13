$(document).ready(function() {
    var display_trolley = false;
    $('#trolley').mouseenter(function(event) {
        $('#dropdown-trolley').css("display","block");
    });
    $('#trolley > a').click(function(event) {
        if(display_trolley == false) {
            display_trolley = true;
            $('#dropdown-trolley').css("display","block");
        }else {
            $('#dropdown-trolley').css("display","none");
            display_trolley = false;
        }
    });
    $('#trolley').mouseleave(function() {
        if (display_trolley == false) {
            $('#dropdown-trolley').fadeOut(750);
        }
    });
    $('.edit-trolley').click(function() {
        var pid;
        var url;
        var shopping = '<tr><th>Shopping Trolley</th><th><a href="trolley"><i class="fa fa-cogs"></i></a></th></tr>';
        var feedback = function(message) {
            return '<div class="notifier-popup btn-success">'+message+'</div>';
        }
        pid = $(this).attr("data-pid");
        url = $(this).attr("data-url");
        var x = $(this).attr("data-direction");
        var qty = $(this).attr("data-qty");
        $.get(url, {product_id: pid, quantity: qty}, function(data){
            for (var i in data.contents) {
                var item = data.contents[i]
                if (item) {
                    shopping += ('<tr class="trolley-item"><td>' + item.p_name + '</td><td>' + item.quantity + '</td>');
                }
            }
            $('#trolley-contents').html(shopping);
            $('#amount').html('('+data.meta.amount+')');
            $(feedback(data.meta.message)).insertAfter('#buy-'+pid).delay(250).fadeOut();
            if (data.contents[pid] && x === "take") {
                $('#n'+data.contents[pid].slug).html(data.contents[pid].quantity);
                $('#cart-icon').css("color", "#CF000F")
            }
            if (x === "return") {
                var item = data.contents[pid]
                if (item) {
                    $('#n'+item.slug).html(item.quantity);
                } else {
                    $('#row-'+pid).hide();
                }
            }
            $('.totalPrice').html(data.meta.total.toFixed(2));
        });
    });
    $('#emptyTrolley').click(function() {
        var url;
        var shopping = '<tr><th>Shopping Trolley</th><th><a href="{% url '+"'shop:trolley'"+' %}"><i class="fa fa-cogs"></i></a></th></tr>';
        url = $(this).attr("data-url");
        $.get(url, function() {
            $('#trolley-contents').html(shopping+'<tr><td><em>No Items</em></td></tr>');
            $('#amount').html('0');
            $('.totalPrice').html('0.00');
        });
    });
});