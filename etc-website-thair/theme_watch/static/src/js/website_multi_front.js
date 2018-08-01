odoo.define('theme_watch.front_js_multi',function(require){
    'use strict';
  var animation = require('web_editor.snippets.animation');
  function initialize_owl(el){
   el.owlCarousel({
    items: 4,
            margin: 30,
            navigation: true,
            pagination: false,
            responsive: {
                0: {
                    items: 1,
                },
                481: {
                    items: 2,
                },
                768: {
                    items: 3,
                },
                1024: {
                    items: 4,
                }
            }

   })
  }
  function destory_owl(el){
    if(el && el.data('owlCarousel'))
   {
    el.data('owlCarousel').destroy();
    el.find('.owl-stage-outer').children().unwrap();
    el.removeData();
    }
  }
  animation.registry.s_product_multi_with_header = animation.Class.extend({
        selector : ".js_multi_collection",
            start: function (editMode) {
            var self = this;
            if (editMode)
            {
			//$('.js_multi_collection').addClass("hidden");
            }
            if(!editMode){
            var list_id=self.$target.attr('data-list-id') || false;
            $.get("/shop/get_multi_tab_content",{'collection_id':list_id}).then(function (data){
				console.log("aaaaaaaaaaaaaaaaaa");
                if(data){                   
                    self.$target.empty().append(data);
                    $(".js_multi_collection").removeClass('hidden');
                    $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
                        initialize_owl($(".multi_tab_slider .tab-content .active .multi_slider"));
                    }).on('hide.bs.tab', function () {
                    destory_owl($(".multi_tab_slider .tab-content .active .multi_slider"));
                    });       
    
                    initialize_owl($(".multi_tab_slider .tab-content .active .multi_slider"));
    }
            });
            }
        },
  });
 animation.registry.s_product_multi_snippet = animation.Class.extend({
        selector : ".multi_tab_product_snippet",
            start: function (editMode) {
            var self = this;
            if(!editMode){
            var list_id=self.$target.attr('data-list-id') || false;
            $.get("/shop/multi_tab_product_snippet",{'collection_id':list_id}).then(function (data){
                if(data){                   
                    self.$target.empty().append(data);
                    $(".multi_tab_product_snippet").removeClass('hidden');
                    }
            });
            }
        },
  });

$(document).ready(function() {


    $('.multi_tab_slider li a[data-toggle="tab"]').on('shown.bs.tab', function () {
    $(".multi_slider").owlCarousel({
        items: 4,
        margin: 30,
        navigation: true,
        pagination: false,
        responsive: {
            0: {
                items: 1,
            },
            481: {
                items: 2,
            },
            768: {
                items: 3,
            },
            1024: {
                items: 4,
            }
        }

    });
    });
});
});

