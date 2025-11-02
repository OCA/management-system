import {
    assertSteps,
    contains,
    mailModels,
    onRpcBefore,
    openFormView,
    start,
    startServer,
    step,
} from "@mail/../tests/mail_test_helpers";

import {
    defineModels,
    getKwArgs,
    makeKwArgs,
    serverState,
} from "@web/../tests/web_test_helpers";
import {describe, test} from "@odoo/hoot";

describe.current.tags("desktop");

class MailThreadNonConformity extends mailModels.MailThread {
    _thread_to_store() {
        const result = super._thread_to_store(...arguments);
        const kwargs = getKwArgs(arguments, "ids", "store", "fields", "request_list");
        const store = kwargs.store;
        const id = kwargs.ids[0];
        store.add(
            this.env[this._name].browse(id),
            {
                non_conformity_count: 0,
            },
            makeKwArgs({as_thread: true})
        );
        return result;
    }
}

defineModels({...mailModels, MailThread: MailThreadNonConformity});

test("simple chatter on a record", async () => {
    const pyEnv = await startServer();
    onRpcBefore((route, args) => {
        if (route.startsWith("/mail") || route.startsWith("/discuss")) {
            step(`${route} - ${JSON.stringify(args)}`);
        }
    });
    await start();
    await assertSteps([
        `/mail/data - ${JSON.stringify({
            init_messaging: {},
            failures: true,
            systray_get_activities: true,
            context: {
                lang: "en",
                tz: "taht",
                uid: serverState.userId,
                allowed_company_ids: [1],
            },
        })}`,
    ]);
    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    await openFormView("res.partner", partnerId);
    await contains(".o-mail-Chatter-topbar");
    await contains(".o-mail-Thread");
    await assertSteps([
        `/mail/thread/data - {"request_list":["activities","attachments","followers","scheduledMessages","suggestedRecipients"],"thread_id":${partnerId},"thread_model":"res.partner"}`,
        `/mail/thread/messages - {"thread_id":${partnerId},"thread_model":"res.partner","limit":30}`,
    ]);
    await contains(".o_ChatterTopbar_buttonNonConformities");
});
