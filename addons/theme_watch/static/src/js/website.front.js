odoo.define('theme_watch.front_js',function(require){
	'use strict';
  var animation = require('web_editor.snippets.animation');
  
  function set_resposive(product_slide){
			  var responsive="";
				if (product_slide==1)
				{
				responsive="responsive:{0: {items: 1,}}"
				}
				if(product_slide==2)
				{
				responsive="responsive: {0: {items: 1,},481: {items: 2,}}"							            
				}
				if(product_slide==3)
				{
				responsive="responsive: {0: {items: 1,},481: {items: 2,},768: {items: 3,}}"
							            
				}
				if(product_slide==4)
				{
				responsive="responsive: { 0: {items: 1,},481: {items: 2,},768: {items: 3,},1024: {items: 4,}}"
							            
				}	    					    				
	 return  responsive;
  }
  animation.registry.advance_product_slider = animation.Class.extend({
    selector : ".tqt_products_slider",
        start: function (editMode) {
            var self = this;
			if (editMode)
            {$('.tqt_products_slider .advance_product_slider').addClass("hidden");
			}
			if(!editMode){
			var auto_scroll=self.$target.attr('data-auto-scroll') || false,
			    scroll_speed=parseInt(self.$target.attr('data-scroll-speed') || 0),
			    product_slide=parseInt(self.$target.attr('data-product-slide') || 0),
				slider_id='tqt_products_slider'+new Date().getTime();

            $.get("/shop/get_products_content",{'product_count':self.$target.attr('data-product-count') || 0,
            									'slider_type':self.$target.attr('data-slider-type') || '',
            									'product_label': self.$target.attr('data-product-label') || '',
            									'auto_scroll':self.$target.attr('data-auto-scroll') || false,
            									'show_cart':self.$target.attr('data-show-cart') || false,
            									'show_product_price':self.$target.attr('data-show-product-price') || false,
            									'show_product_name':self.$target.attr('data-show-product-name') || false,
            									'scroll_speed':self.$target.attr('scroll-speed') || 0,
												'slider_id':slider_id,

            									}).then(function( data ) {
                if(data){                   
                    self.$target.empty().append(data);
					$(".tqt_products_slider").removeClass('hidden');
					$.getScript("/theme_watch/static/src/js/owl.carousel.min.js");
					var script = document.createElement("script");	
					script.type = "text/javascript";
					var script_data='$(document).ready(function() {$("#';
					script_data=script_data+slider_id;
					script_data=script_data+'").owlCarousel({margin: 30,responsiveClass: true,';
    			    var items;
    			    var responsive;
    				if(product_slide>0)
    				{
    				  items="items:"+product_slide;
    				  responsive=set_resposive(product_slide);
    				}
    				else
    				{
    				items="items:"+4+"";
    				responsive="responsive: {\
						            0: {\
						                items: 1,\
						            },\
						            481: {\
						                items: 2,\
						            },\
						            768: {\
						                items: 3,\
						            },\
						            1024: {\
						                items: 4,\
						            }\
						        }"    				
    				}
    				if(parseInt(scroll_speed)>0)
    				{
    				script_data=script_data+'slideSpeed:'+scroll_speed+',';
    				} 
    				if(auto_scroll==false)
    				{
    				script_data=script_data+'autoPlay:'+false+',';
    				}
    				script_data=script_data+items+',';
    				script_data=script_data+responsive;
    				
    			    script_data=script_data+"})});";
    				script.innerHTML=script_data;
    				document.getElementsByTagName("body")[0].appendChild(script);

    				
                }
            });}
        }
    });

    animation.registry.product_brand_slider = animation.Class.extend({
        selector: ".tqt_product_brand_slider",
        start: function(editable_mode) {
            var self = this;
            if (editable_mode) {
                $('.tqt_product_brand_slider .owl-carousel').empty();
            }
            if (!editable_mode) {
                $.get("/shop/get_product_brand_slider", {
                    'label': self.$target.attr('data-brand-label') || '',
                    'brand-count': self.$target.attr('data-brand-count') || 0,
                }).then(function(data) {
                    if (data) {
                    self.$target.empty().append(data);
					$(".tqt_product_brand_slider").removeClass('hidden');
					$.getScript("/theme_watch/static/src/js/owl.carousel.min.js");		
					$.getScript("/theme_watch/static/src/js/website.brand.js");												
							}
				});
			}
}
	});
});

