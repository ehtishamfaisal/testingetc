odoo.define('theme_watch.website_multi_editor', function (require) {
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


var multi_tab_configure = options.Class.extend({
    popup_template_id: "editor_new_multi_tab_configure_template",
    popup_title: _t("Select Collection"),
    select_collection: function (type, value) {
        var self = this;
        if (type !== "click") return;
        var def = website.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Collection"),
            'init': function (field) {
                return new Model('collection.configure').call('name_search', ['', []], { context: base.get_context() });
            },
        });
        def.then(function (collection_id) {
            self.$target.attr("data-list-id", collection_id);
            new Model('collection.configure').call('read', [[parseInt(collection_id)]], { context: base.get_context() }).then(function (data){
                if(data && data[0] && data[0].name)
                {
                 self.$target.empty().append('<div class="container"><div class="product_slide" contentEditable="false"><div class="col-md-12"><div class="seaction-head"<h1>'+ data[0].name +'</h1></div></div></div></div>');   
                }
            });
            
        });
        return def;
    },
    drop_and_build_snippet: function() {
        var self = this;
        this._super();
        this.select_collection('click').fail(function () {
            self.editor.on_remove($.Event( "click" ));
        });
    },
});

options.registry.s_product_multi_with_header = multi_tab_configure.extend({
    clean_for_save: function () {
        $('.js_multi_collection').empty();
    },
});

options.registry.s_product_multi_snippet = options.Class.extend({
    popup_template_id: "editor_new_multi_tab_configure_template",
    popup_title: _t("Select Collection"),
    select_collection: function (type, value) {
        var self = this;
        if (type !== "click") return;
        var def = website.prompt({
            'id': this.popup_template_id,
            'window_title': this.popup_title,
            'select': _t("Collection"),
            'init': function (field) {
                return new Model('collection.configure').call('name_search', ['', []], { context: base.get_context() });
            },
        });
        def.then(function (collection_id) {
            self.$target.attr("data-list-id", collection_id);
            new Model('collection.configure').call('read', [[parseInt(collection_id)]], { context: base.get_context() }).then(function (data){
                if(data && data[0] && data[0].name)
                {
                 self.$target.empty().append('<div class="container"><div class="product_slide" contentEditable="false"><div class="col-md-12"><div class="seaction-head"<h1>'+ data[0].name +'</h1></div></div></div></div>');   
                }
            });
            
        });
        return def;
    },
    drop_and_build_snippet: function() {
        var self = this;
        this._super();
        this.select_collection('click').fail(function () {
            self.editor.on_remove($.Event( "click" ));
        });
    },    
    clean_for_save: function () {
        $('.multi_tab_product_snippet').empty();
    },
});

});



