/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
$(document).ready(function () {
  $('.wk_horizontal_categories_link').hover(function() {
    if(!$(this).hasClass('hoverd'))
    {
     $(this).parent().find('.wk_horizontal_cart').slideDown('slow');
   }
 },function(){
  $(this).parent().find('.wk_horizontal_cart').slideUp('slow');
});


  $('.wk_horizontal_cart').hide();
  window.onload = function () {
    if($('.products_price_filter input[type="checkbox"]').is(":checked")){
     $('.horizontal_category_unlink_list').show();

   }
 }


 $('.products_price_filter input[name="attrib_price"]').on('click',function(){
  var brands = $('.products_price_filter').data('brands');
  var brand= $(this).data('brand');
});



 $('.oe_website_sale').each(function () {
  var oe_website_sale = this;
  console.log($('.products_price_filter').find("input[name='attrib_price']:checked"));
    $('a.wk_price').on('change click', function () {
      var wk_price = $(this).data('wk_price');
      $.each($('.products_price_filter').find("input[name='attrib_price']:checked"),
        function(){
          if (wk_price==$(this).data('brand')){
            $(this).click();
          }
      });
    });

});


});
