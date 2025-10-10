import {X2ManyField, x2ManyField} from "@web/views/fields/x2many/x2many_field";
import {registry} from "@web/core/registry";

export class DocumentPageWidget extends X2ManyField {
    setup() {
        super.setup();
        this.canOpenRecord = false;
    }

    get isMany2Many() {
        // The field is used like a many2many to allow for adding existing lines to the sheet.
        return true;
    }
}

export const documentPageWidget = {
    ...x2ManyField,
    component: DocumentPageWidget,
    additionalClasses: ["o_field_many2many"],
};

registry.category("fields").add("document_page_widget", documentPageWidget);
