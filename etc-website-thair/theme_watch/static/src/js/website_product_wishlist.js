odoo.define('theme_watch.product_wishlist', function (require) {
"use strict";
var ajax = require('web.ajax');
$(document).ready(function ()
	{ 	
	
	$(".add_to_wishlist").on("click",function(ev) {        
      	ev.preventDefault();
      	ev.stopPropagation();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().find("input");
        var product_id = $input.val();
        var product_id = parseInt(product_id,10);
        ajax.jsonRpc("/shop/product/whishlists/add_to_wishlist", 'call', {
		'product_id':product_id,})
	.then(function (data) {
                    $(ev.currentTarget).toggleClass("fa-heart-o");
                    $(ev.currentTarget).toggleClass("fa-heart");
					alert("Your Product is successfully added in wishlist");
                    return false;
			});
        return false;
        });
	$(".clear_whishlist").click(function(ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().find("input");
        console.log($input)
        var line_id = parseInt($input.data('line-id'),10);
        ajax.jsonRpc("/shop/product/whishlists/delete_json", 'call', {
            'line_id': line_id
			})
	.then(function (data) {
                    location.reload();
                    return;
			});
        return false;

	});
	
	$(".update_whishlist").click(function(ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().find("input");
        var line_id = parseInt($input.data('line-id'),10);
        var $textarea=$link.parent().find("textarea");
        var comment = $textarea.val();
        console.log(comment,"Coment");      
        ajax.jsonRpc("/shop/product/whishlists/comment", 'call', {
            'wishlist_id': line_id,
            'comment': comment
			})
	.then(function (data) {
                    location.reload();
                    return;
			});
        return false;

	});	
	$("#clear_all_wishlist").click(function(ev){
      	ev.preventDefault();
      	ev.stopPropagation();
        ajax.jsonRpc("/shop/product/whishlists/delete_all_json", 'call', {})
		.then(function (data) {
                    location.reload();
                    return;
			});
        return false;	
	});
	
	$("#move_to_cart").click(function(ev){
        ev.preventDefault();
      	ev.stopPropagation();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().find("input");
        var line_id = parseInt($input.data('line-id'),10);
        console.log(line_id);
        ajax.jsonRpc("/shop/product/whishlists/move_to_cart", 'call', {
            'line_id': line_id
			})
	.then(function (data) {
                    location.reload();
                    return;
			});
        return false;
			});
			
	$("#add_all_cart").click(function(ev){
        ev.preventDefault();
      	ev.stopPropagation();
        ajax.jsonRpc("/shop/product/whishlists/add_all_to_cart", 'call', {
			})
	.then(function (data) {
                    location.reload();
                    return;
			});
        return false;
			});       

$('.oe_website_sale').each(function () {
    var oe_website_sale = this;



    $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (ev) {
        var $ul = $(ev.target).closest('form');
        var  $product_id = $ul.find("input[name='product_id']").first();    
            if ($product_id)
            {
            var image_url="/web/image/product.product/" + $product_id.val() + "/image";
		    $('.main_image').attr('src', image_url);
			$('.product_detail_img').parent().parent().attr('href',image_url);
		    $('.variant_img .sub-images').attr('src', image_url);
		    $('.product_detail_img').removeData('elevateZoom');
			$('.product_detail_img').elevateZoom({
		                    constrainType: "height",
		                    constrainSize: 274,
		                    zoomType: "lens",
		                    containLensZoom: true,
		                    cursor: 'pointer'
		                });
            ajax.jsonRpc("/shop/product/check_wishlist","call",
                {'product_id':parseInt($product_id.val()),
                })
                .then(function (data) {
                    if(data==false)
                    {
                     $('.add_to_wishlist').addClass("fa-heart-o");
                     $('.add_to_wishlist').removeClass("fa-heart");
                    }
                    else{
                     $('.add_to_wishlist').removeClass("fa-heart-o");
                     $('.add_to_wishlist').addClass("fa-heart");   
                    } 
                    

                });
    }

});

$(oe_website_sale).on("change", ".oe_cart input.js_quantity[data-product-id]", function () {
      var $input = $(this);
        if ($input.data('update_change')) {
            return;
        }
      var value = parseInt($input.val(), 10);
      var $dom = $(this).closest('tr');
      var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
      var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
      var line_id = parseInt($input.data('line-id'),10);
      var product_id = parseInt($input.data('product-id'),10);
      var product_ids = [product_id];
	  var clickwatch = (function(){
		      var timer = 0;
		      return function(callback, ms){
		        clearTimeout(timer);
		        timer = setTimeout(callback, ms);
		      };
		})();
      clickwatch(function(){

        $dom_optional.each(function(){
            $(this).find('.js_quantity').text(value);
            product_ids.push($(this).find('span[data-product-id]').data('product-id'));
        });
        $input.data('update_change', true);

        ajax.jsonRpc("/shop/cart/update_json", 'call', {
        'line_id': line_id,
        'product_id': parseInt($input.data('product-id'),10),
        'set_qty': value})
        .then(function (data) {
            $input.data('update_change', false);
            if (value !== parseInt($input.val(), 10)) {
                $input.trigger('change');
                return;
            }
            var $q = $(".my_cart_quantity");
            if (data.cart_quantity) {
                $q.parent().parent().removeClass("hidden");
            }
            else {
                $q.parent().parent().addClass("hidden");
                $('a[href^="/shop/checkout"]').addClass("hidden")
            }
            

			$.get("/shop/product/update_cart_popup",{})
				.then(function (data) {
		                	if(data)
							{
							$(".hm-cart-item").html(data);
        					$('.hm-cart-item').toggleClass("hm-cart-item-open");
							}
				});
	

		  
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

            $(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();

            if (data.warning) {
                var cart_alert = $('.oe_cart').parent().find('#data_warning');
                if (cart_alert.length === 0) {
                    $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                }
                else {
                    cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                }
                $input.val(data.quantity);
            }
        });
      }, 500);
    });
        $(oe_website_sale).on('change', 'input.js_product_change', function () {
			$('.variant_img .sub-images').attr("src", "/web/image/product.product/" + $(this).val() + "/image");
			$('.variant_img').parent().find('a').attr('href',"/web/image/product.product/" + $(this).val() + "/image");
		    $('.product_detail_img').removeData('elevateZoom');
			$('.product_detail_img').elevateZoom({
		                    constrainType: "height",
		                    constrainSize: 274,
		                    zoomType: "lens",
		                    containLensZoom: true,
		                    cursor: 'pointer'
		                });
        });
        $('.js_add_cart_variants', oe_website_sale).each(function () {
        $('input.js_variant_change, select.js_variant_change', this).first().trigger('change');
    });
});
        
});
});
