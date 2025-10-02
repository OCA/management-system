import {
    assertSteps,
    contains,
    defineMailModels,
    onRpcBefore,
    openFormView,
    start,
    startServer,
    step,
} from "@mail/../tests/mail_test_helpers";
import {describe, test} from "@odoo/hoot";
import {serverState} from "@web/../tests/web_test_helpers";

describe.current.tags("desktop");
defineMailModels();

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
