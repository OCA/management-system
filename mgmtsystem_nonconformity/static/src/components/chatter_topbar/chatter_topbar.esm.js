/* @odoo-module */
import {Chatter} from "@mail/core/web/chatter";
import {ThreadService} from "@mail/core/common/thread_service";
import {patch} from "@web/core/utils/patch";

patch(ThreadService.prototype, {
    async fetchData(thread, ...args) {
        const result = await super.fetchData(thread, ...args);
        thread.non_conformity_count = result.non_conformity_count;
        return result;
    },
});
patch(Chatter.prototype, {
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
                    id: this.props.threadId,
                    mgmtsystem_nonconformity: this.props.threadModel,
                },
            }
        );
    },
});
