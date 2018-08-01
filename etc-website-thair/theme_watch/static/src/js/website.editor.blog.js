odoo.define('theme_watch.editor_blog', function (require) {
'use strict';

var Model = require('web.Model');
var ajax = require('web.ajax');
var core = require('web.core');
var base = require('web_editor.base');
var web_editor = require('web_editor.editor');
var options = require('web_editor.snippets.options');
var snippet_editor = require('web_editor.snippet.editor');
var website = require('website.website');
var _t = core._t;


options.registry.latest_blog = options.Class.extend({
    popup_template_id: "editor_new_blog_slider_template",
    popup_title: _t("Select Collection"),
    website_blog_configure: function (type, value) {
        var self = this;
        if (type !== "click") return;
        var def = website.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Collection"),
            'init': function (field) {
                return new Model('blog.configure').call('name_search', ['', []], { context: base.get_context() });
            },
        });
        def.then(function (collection_id) {
            self.$target.attr("data-list-id", collection_id);
            new Model('blog.configure').call('read', [[parseInt(collection_id)]], { context: base.get_context() }).then(function (data){
                if(data && data[0] && data[0].name)
                {
                 self.$target.empty().append('<div class="seaction-head"><h1>'+ data[0].name+'</h1></div>');   
                }
            });
            
        });
        return def;
    },
    drop_and_build_snippet: function() {
        var self = this;
        this._super();
        this.website_blog_configure('click').fail(function () {
            self.editor.on_remove($.Event( "click" ));
        });
    },
    clean_for_save: function () {
        $('section.web_blog_slider').empty();
    },
});

});
