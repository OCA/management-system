/** @odoo-module **/

import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "Chatter",
    recordMethods: {
        async onClickShowNonConformities() {
            if (this.isTemporary) {
                const saved = await this.doSaveRecord();
                if (!saved) {
                    return;
                }
            }
            this.env.services.action.doAction(
                "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_thread_list",
                {
                    additionalContext: {
                        active_id: this.thread.id,
                        active_model: this.thread.model,
                    },
                }
            );
        },
    },
});
