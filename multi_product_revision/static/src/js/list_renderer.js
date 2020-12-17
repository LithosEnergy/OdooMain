odoo.define('multi_product_revision.customListRenderer', function (require) {
"use strict";

    var ListRenderer = require('web.ListRenderer'); 
    var BasicRenderer = require('web.BasicRenderer');
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');
    var field_utils = require('web.field_utils');
    var Pager = require('web.Pager');
    var utils = require('web.utils');
    var viewUtils = require('web.viewUtils');
    var basic_fields = require('web.basic_fields');


    var _t = core._t;
  

    ListRenderer.include({
        // You need to redefine the function here
        
        _renderButton: function (record, node) {
            var self = this;
            var nodeWithoutWidth = Object.assign({}, node);
            delete nodeWithoutWidth.attrs.width;
            var $button = viewUtils.renderButtonFromNode(nodeWithoutWidth, {
                extraClass: node.attrs.icon ? 'o_icon_button' : undefined,
                textAsTitle: !!node.attrs.icon,
            });
            this._handleAttributes($button, node);
            this._registerModifiers(node, record, $button);
                       

            if (record.data['generate_revision_depend'] == true){
                self.trigger_up('button_clicked', {
                    attrs: node.attrs,
                    record: record,
                });
            }      
            
            
            if (record.res_id) {
                // TODO this should be moved to a handler
                $button.on("click", function (e) {
                    e.stopPropagation();
                    self.trigger_up('button_clicked', {
                        attrs: node.attrs,
                        record: record,
                    });
                });
            } else {
                if (node.attrs.options.warn) {
                    $button.on("click", function (e) {
                        e.stopPropagation();
                        self.do_warn(_t("Warning"), _t('Please click on the "save" button first.'));
                    });
                } else {
                    $button.prop('disabled', true);
                }
            }

            return $button;
        }

 });



});