odoo.define("mgmtsystem_evaluation.evaluation_reference", function (require) {
    "use strict";

    var relational_fields = require("web.relational_fields");
    var FieldRegistry = require("web.field_registry");

    var EvaluationReferenceField = relational_fields.FieldReference.extend({
        resetOnAnyFieldChange: true,
        _setState: function () {
            this._super.apply(this, arguments);
            this.field.relation = this.recordData[this.nodeOptions.model_field];
        },
        _reset: function (record) {
            if (
                record.data[this.nodeOptions.model_field] &&
                (!this.value ||
                    this.value.model_field !==
                        record.data[this.nodeOptions.model_field])
            ) {
                this.$("select").val(record.data[this.nodeOptions.model_field]);
            }
            this._super.apply(this, arguments);
        },
    });
    FieldRegistry.add("evaluation_reference", EvaluationReferenceField);
});
