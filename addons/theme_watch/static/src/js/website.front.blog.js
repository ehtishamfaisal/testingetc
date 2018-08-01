odoo.define('theme_watch.front_js_blog',function(require){
    'use strict';
var ajax = require('web.ajax');
var utils = require('web.utils');
var animation = require('web_editor.snippets.animation');
var website = require('website.website');

      animation.registry.latest_blog = animation.Class.extend({
        selector : ".web_blog_slider",
            start: function (editMode) {
            var self = this;
            if (editMode)
            {
            }
            if(!editMode){
            var list_id=self.$target.attr('data-list-id') || false;
            $.get("/blog/get_blog_content",{'blog_config_id':list_id}).then(function (data){
                if(data){                   
                    self.$target.empty().append(data);
                }});
        }
        },
});
});

