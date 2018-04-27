odoo.define('max_web_draggable_dialog', function (require) {
'use strict';

    var Dialog = require('web.Dialog');

    Dialog.include({
        open: function () {
            this._super.apply(this, arguments);
            this._opened.done(function(){
                $(".modal.in").draggable({
                    handle: ".modal-header"
                });
                $('.modal-content').resizable({
				    //alsoResize: ".modal-dialog",
				    minHeight: 225,
				    minWidth: 500
				});
				$('.modal.in').on('show.bs.modal', function () {
				    $(this).find('.modal-body').css({
				        'max-height':'100%'
				    });
				});
            });
            return this;
        },
    });
});