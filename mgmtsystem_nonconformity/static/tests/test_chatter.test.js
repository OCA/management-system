import {
    contains,
    mailModels,
    onRpcBefore,
    openFormView,
    start,
    startServer,
} from "@mail/../tests/mail_test_helpers";

import {defineModels, serverState} from "@web/../tests/web_test_helpers";
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

function assertStepsContain(actualSteps, expectedSteps) {
    const missingSteps = expectedSteps.filter(
        (expectedStep) => !actualSteps.includes(expectedStep)
    );
    if (missingSteps.length) {
        throw new Error(
            `Missing expected RPC steps:\n${missingSteps.join("\n")}\n\nReceived RPC steps:\n${actualSteps.join("\n")}`
        );
    }
}

defineModels({...mailModels, MailThread: MailThreadNonConformity});

test("simple chatter on a record", async () => {
    const pyEnv = await startServer();
    const rpcSteps = [];
    onRpcBefore((route, args) => {
        if (route.startsWith("/mail") || route.startsWith("/discuss")) {
            rpcSteps.push(`${route} - ${JSON.stringify(args)}`);
        }
    });
    await start();
    assertStepsContain(rpcSteps, [
        `/mail/data - ${JSON.stringify({
            fetch_params: ["failures", "systray_get_activities", "init_messaging"],
            context: {
                lang: "en",
                tz: "taht",
                uid: serverState.userId,
                allowed_company_ids: [1],
            },
        })}`,
    ]);
    rpcSteps.length = 0;

    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    await openFormView("res.partner", partnerId);
    await contains(".o-mail-Chatter-topbar");
    await contains(".o-mail-Thread");
    assertStepsContain(rpcSteps, [
        `/mail/thread/messages - {"thread_id":${partnerId},"thread_model":"res.partner","fetch_params":{"limit":30}}`,
        `/mail/data - {"fetch_params":[["mail.thread",{"access_params":{},"request_list":["activities","attachments","contact_fields","followers","scheduledMessages","suggestedRecipients"],"thread_id":${partnerId},"thread_model":"res.partner"}]],"context":{"lang":"en","tz":"taht","uid":${serverState.userId},"allowed_company_ids":[1]}}`,
    ]);
    await contains(".o_ChatterTopbar_buttonNonConformities");
});
