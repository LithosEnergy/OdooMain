odoo.define('boms_via_plm.CustomFormView', function (require) {
"use strict";

const FormView = require('web.FormView');
var utils = require('web.utils');
var Widget = require('web.Widget');


    FormView.include({

    _setSubViewLimit: function (attrs) {

        if (this.loadParams.modelName === "mrp.bom"){
            attrs.limit = 1000;
        }
        else{
            var view = attrs.views && attrs.views[attrs.mode];
            var limit = view && view.arch.attrs.limit && parseInt(view.arch.attrs.limit, 10);
            attrs.limit = limit || attrs.Widget.prototype.limit || 40;
        }
    },
});

});
