import {ListController} from "@web/views/list/list_controller";
import {onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class MgmtsystemDocumentController extends ListController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.action = useService("action");
        onWillStart(async () => {
            this.documentTypes = await this.orm.call(
                "mgmtsystem.document",
                "get_document_types",
                [],
                {context: this.props.context}
            );
        });
    }
    async onAddElement(type) {
        const action = await this.orm.call(this.props.resModel, "add_element", [type], {
            context: this.props.context,
        });
        if (action) {
            this.action.doAction(action);
        }
    }

    async openRecord(record) {
        const action = await this.orm.call(
            this.props.resModel,
            "get_formview_action",
            [record.resId],
            {context: this.props.context}
        );
        if (action) {
            this.action.doAction(action);
        }
    }
}
