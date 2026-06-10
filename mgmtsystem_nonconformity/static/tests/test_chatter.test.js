import {
    STORE_FETCH_ROUTES,
    contains,
    listenStoreFetch,
    mailModels,
    onRpcBefore,
    openFormView,
    start,
    startServer,
    waitStoreFetch,
} from "@mail/../tests/mail_test_helpers";

import {asyncStep, defineModels} from "@web/../tests/web_test_helpers";
import {describe, test} from "@odoo/hoot";

describe.current.tags("desktop", "mgmtsystem_nonconformity");

class MailThreadNonConformity extends mailModels.MailThread {
    _thread_to_store(store, fields, request_list) {
        const result = super._thread_to_store(...arguments);
        const id = this[0].id;

        if (request_list) {
            store._add_record_fields(
                this.env[this._name].browse(id),
                {
                    non_conformity_count: 0,
                },
                true
            );
        }

        return result;
    }
}

defineModels({...mailModels, MailThread: MailThreadNonConformity});

test("simple chatter on a record", async () => {
    const pyEnv = await startServer();
    onRpcBefore((route, args) => {
        if (
            (route.startsWith("/mail") || route.startsWith("/discuss")) &&
            !STORE_FETCH_ROUTES.includes(route)
        ) {
            asyncStep(`${route} - ${JSON.stringify(args)}`);
        }
    });
    listenStoreFetch(undefined, {logParams: ["mail.thread"]});
    await start();
    await waitStoreFetch(["failures", "systray_get_activities", "init_messaging"]);
    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    await openFormView("res.partner", partnerId);
    await contains(".o-mail-Chatter-topbar");
    await contains(".o-mail-Thread");
    await waitStoreFetch(
        [
            [
                "mail.thread",
                {
                    access_params: {},
                    request_list: [
                        "activities",
                        "attachments",
                        "contact_fields",
                        "followers",
                        "scheduledMessages",
                        "suggestedRecipients",
                    ],
                    thread_id: partnerId,
                    thread_model: "res.partner",
                },
            ],
        ],
        {
            ignoreOrder: true,
            stepsAfter: [
                `/mail/thread/messages - {"thread_id":${partnerId},"thread_model":"res.partner","fetch_params":{"limit":30}}`,
            ],
        }
    );
    await contains(".o_ChatterTopbar_buttonNonConformities");
});
