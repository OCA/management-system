/** @odoo-module **/

import BasicModel from "web.BasicModel";

BasicModel.include({
    /**
     * Extend `_fetchModelFieldReference` to support `model_field_char`
     */
    _fetchModelFieldReference: async function (record, fieldName, fieldInfo) {
        if (fieldInfo.options.model_field) {
            // Call the original method if `model_field` is defined
            return this._super.apply(this, arguments);
        } else if (fieldInfo.options.model_field_char) {
            const modelFieldChar = fieldInfo.options.model_field_char;
            const modelCharValue =
                (record._changes && record._changes[modelFieldChar]) ||
                record.data[modelFieldChar];

            if (modelCharValue) {
                return {
                    modelName: modelCharValue,
                    hasChanged: true,
                };
            }

            return Promise.resolve();
        }
    },

    /**
     * Extend `_fetchSpecialReference` to also consider `model_field_char`
     */
    _fetchSpecialReference: function (record, fieldName, fieldInfo) {
        const field = record.fields[fieldName];
        if (field.type === "char") {
            return Promise.resolve(this._fetchReference(record, fieldName));
        } else if (fieldInfo.options.model_field) {
            return this._fetchModelFieldReference(record, fieldName, fieldInfo);
        } else if (fieldInfo.options.model_field_char) {
            return this._fetchModelFieldReference(record, fieldName, fieldInfo);
        }
        return Promise.resolve();
    },
});
