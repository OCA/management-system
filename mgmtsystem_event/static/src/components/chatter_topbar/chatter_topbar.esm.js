import {Chatter} from "@mail/chatter/web_portal/chatter";
import {patch} from "@web/core/utils/patch";

patch(Chatter.prototype, {
    async onClickShowEvents() {
        if (this.isTemporary) {
            const saved = await this.doSaveRecord();
            if (!saved) {
                return;
            }
        }
        this.env.services.action.doAction(
            "mgmtsystem_event.open_mgmtsystem_event_thread_list",
            {
                additionalContext: {
                    id: this.props.threadId,
                    mgmtsystem_event: this.props.threadModel,
                },
            }
        );
    },
});
