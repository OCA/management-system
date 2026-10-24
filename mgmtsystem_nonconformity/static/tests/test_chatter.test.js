import {
    contains,
    mailModels,
    openFormView,
    start,
    startServer,
} from "@mail/../tests/mail_test_helpers";
import {describe, test} from "@odoo/hoot";
import {defineModels} from "@web/../tests/web_test_helpers";

describe.current.tags("desktop", "mgmtsystem_nonconformity");

class MailThreadNonConformity extends mailModels.MailThread {
    _store_thread_fields(res, {request_list = []} = {}) {
        super._store_thread_fields(...arguments);
        if (request_list.length) {
            res.attr("non_conformity_count", 0);
        }
    }
}

defineModels({...mailModels, MailThread: MailThreadNonConformity});

test("simple chatter on a record", async () => {
    const pyEnv = await startServer();
    const partnerId = pyEnv["res.partner"].create({name: "John Doe"});
    await start();
    await openFormView("res.partner", partnerId);
    await contains(".o-mail-Chatter-topbar");
    await contains(".o_ChatterTopbar_buttonNonConformities");
    await contains(".o_ChatterTopbar_buttonNonConformitiesCount", {text: "0"});
});
