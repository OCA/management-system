import {defineModels, fields, models, mountView} from "@web/../tests/web_test_helpers";
import {expect, test} from "@odoo/hoot";
import {defineMailModels} from "@mail/../tests/mail_test_helpers";

class Objective extends models.Model {
    _name = "mgmtsystem.objective";
    value_state = fields.Selection({
        string: "Value State",
        selection: [
            ["on_target", "On Target"],
            ["below_target", "Below Target"],
            ["above_target", "Above Target"],
            ["no_target", "No Target"],
        ],
    });
    _records = [
        {id: 1, value_state: "on_target"},
        {id: 2, value_state: "below_target"},
        {id: 3, value_state: "above_target"},
        {id: 4, value_state: "no_target"},
    ];
    _views = {
        form: `
            <form>
                <sheet>
                    <group>
                        <field name="value_state" widget="objective_state_selection"/>
                    </group>
                </sheet>
            </form>`,
    };
}
defineModels([Objective]);
defineMailModels();

test("Check Objective State Widget On Target", async () => {
    await mountView({
        type: "form",
        resIds: [1],
        resId: 1,
        resModel: "mgmtsystem.objective",
    });
    expect(".o_status").toHaveCount(1);
    expect(".o_status.o_status_green").toHaveCount(1);
    expect(".o_status.o_status_red").toHaveCount(0);
});

test("Check Objective State Widget Below Target", async () => {
    await mountView({
        type: "form",
        resIds: [2],
        resId: 2,
        resModel: "mgmtsystem.objective",
    });
    expect(".o_status").toHaveCount(1);
    expect(".o_status.o_status_green").toHaveCount(0);
    expect(".o_status.o_status_red").toHaveCount(1);
});
test("Check Objective State Widget Above Target", async () => {
    await mountView({
        type: "form",
        resIds: [3],
        resId: 3,
        resModel: "mgmtsystem.objective",
    });
    expect(".o_status").toHaveCount(1);
    expect(".o_status.o_status_green").toHaveCount(0);
    expect(".o_status.o_status_red").toHaveCount(1);
});
test("Check Objective State Widget No Target", async () => {
    await mountView({
        type: "form",
        resIds: [4],
        resId: 4,
        resModel: "mgmtsystem.objective",
    });
    expect(".o_status").toHaveCount(1);
    expect(".o_status.o_status_green").toHaveCount(0);
    expect(".o_status.o_status_red").toHaveCount(0);
});
