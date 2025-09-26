import {
    StateSelectionField,
    stateSelectionField,
} from "@web/views/fields/state_selection/state_selection_field";
import {registry} from "@web/core/registry";

export const STATUS_COLORS = {
    on_target: "green",
    below_target: "red",
    above_target: "red",
};
export class ObjectiveStateSelectionField extends StateSelectionField {
    setup() {
        super.setup();
        this.colors = STATUS_COLORS;
    }
}

export const objectiveStateSelectionField = {
    ...stateSelectionField,
    component: ObjectiveStateSelectionField,
};

registry
    .category("fields")
    .add("objective_state_selection", objectiveStateSelectionField);
