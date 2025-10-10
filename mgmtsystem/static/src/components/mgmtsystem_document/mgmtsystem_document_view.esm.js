import {MgmtsystemDocumentController} from "./mgmtsystem_document_controller.esm";
import {listView} from "@web/views/list/list_view";
import {registry} from "@web/core/registry";

export const mgmtsystemDocumentView = {
    ...listView,
    Controller: MgmtsystemDocumentController,
    buttonTemplate: "mgmtsystem.MgmtsystemDocumentView.Buttons",
};

registry.category("views").add("mgmtsystem_document", mgmtsystemDocumentView);
