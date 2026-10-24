import {Chatter} from "@mail/chatter/web_portal_project/chatter";
import {Thread} from "@mail/core/common/thread_model";
import {patch} from "@web/core/utils/patch";

patch(Thread.prototype, {
    setup() {
        super.setup(...arguments);
        this.non_conformity_count = undefined;
    },
});

patch(Chatter.prototype, {
    async onClickShowNonConformities() {
        if (!this.threadId()) {
            const saved = await this.webChatterProps.saveRecord?.();
            if (!saved) {
                return;
            }
        }
        this.env.services.action.doAction(
            "mgmtsystem_nonconformity.open_mgmtsystem_nonconformity_thread_list",
            {
                additionalContext: {
                    id: this.threadId(),
                    mgmtsystem_nonconformity: this.threadModel(),
                },
            }
        );
    },
});
