import {Chatter} from "@mail/chatter/web_portal/chatter";
import {patch} from "@web/core/utils/patch";

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
