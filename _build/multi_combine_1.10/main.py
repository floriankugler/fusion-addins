from lib import addin, inputs, ui_placement
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = MultiCombine(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class MultiCombineInputs(inputs.Inputs):
    class Operations:
        JOIN = inputs.DropDownInput.Item("Join", 0)
        CUT = inputs.DropDownInput.Item("Cut", 1)
        INTERSECT = inputs.DropDownInput.Item("Intersect", 2)

    def __init__(self):
        self.targets = inputs.SelectionByEntityTokenInput(
            id="targetBodies",
            name="Targets",
            filter=["Bodies", "Occurrences"],
            lower_bound=1,
            upper_bound=0,
            tool_tip="Select one or more target bodies and/or occurrences.",
        )
        self.tool_bodies = inputs.SelectionByEntityTokenInput(
            id="toolBodies",
            name="Tool Bodies",
            filter=["Bodies"],
            lower_bound=1,
            upper_bound=0,
            tool_tip="Select one or more tool bodies to combine with each target.",
        )
        self.operation = inputs.DropDownInput(
            id="operation",
            name="Operation",
            options=[
                MultiCombineInputs.Operations.JOIN,
                MultiCombineInputs.Operations.CUT,
                MultiCombineInputs.Operations.INTERSECT,
            ],
            default_value=MultiCombineInputs.Operations.JOIN.value,
            tool_tip="Combine operation to apply for each target body.",
        )
        super().__init__()


class MultiCombine(addin.Addin):
    inputs: MultiCombineInputs

    @property
    def plugin_name(self) -> str:
        return "Multi Combine"

    @property
    def plugin_desc(self) -> str:
        return "Apply one combine setup across multiple target bodies."

    @property
    def plugin_tooltip(self) -> str:
        return "Creates one combine feature per selected target body."

    def get_ui_placement(self) -> ui_placement.UIPlacement:
        section = ui_placement.PlacementSpec(
            id="SeparatorBeforeCustomAddins",
            anchor_id="FusionMoveCommand",
            insert_before=True,
        )
        command = ui_placement.PlacementSpec(
            id=self.create_command_id,
            anchor_id=section.id,
            insert_before=True,
        )
        return ui_placement.UIPlacement(
            panel_id="SolidModifyPanel",
            command=command,
            section=section,
        )

    def create_inputs(self) -> MultiCombineInputs:
        return MultiCombineInputs()

    def execute(self):
        targets = self._flatten_target_bodies(cast(list[adsk.core.Base], self.inputs.targets.value))
        tools = cast(list[adsk.fusion.BRepBody], self.inputs.tool_bodies.value)
        operation = self._feature_operation(self.inputs.operation.value)

        for target in targets:
            applicable_tools = [tool for tool in tools if tool != target]
            if len(applicable_tools) == 0:
                continue

            combine_input = target.parentComponent.features.combineFeatures.createInput(
                target, adsk.core.ObjectCollection.createWithArray(cast(list[adsk.core.Base], applicable_tools))
            )
            combine_input.operation = operation
            combine_input.isKeepToolBodies = True
            target.parentComponent.features.combineFeatures.add(combine_input)

    def _flatten_target_bodies(self, selected_targets: list[adsk.core.Base]) -> list[adsk.fusion.BRepBody]:
        bodies: list[adsk.fusion.BRepBody] = []
        seen: set[str] = set()

        for target in selected_targets:
            body = adsk.fusion.BRepBody.cast(target)
            if body:
                self._append_body(bodies, seen, body)
                continue

            occ = adsk.fusion.Occurrence.cast(target)
            if occ:
                self._append_occurrence_bodies(bodies, seen, occ)
                continue

        return bodies

    def _append_occurrence_bodies(
        self, bodies: list[adsk.fusion.BRepBody], seen: set[str], occ: adsk.fusion.Occurrence
    ) -> None:
        for body in occ.bRepBodies:
            self._append_body(bodies, seen, body)
        for child in occ.childOccurrences:
            self._append_occurrence_bodies(bodies, seen, child)

    def _append_body(
        self, bodies: list[adsk.fusion.BRepBody], seen: set[str], body: adsk.fusion.BRepBody
    ) -> None:
        token = body.entityToken
        if token in seen:
            return
        seen.add(token)
        bodies.append(body)

    def _feature_operation(self, op_value: int) -> adsk.fusion.FeatureOperations:
        if op_value == MultiCombineInputs.Operations.JOIN.value:
            return adsk.fusion.FeatureOperations.JoinFeatureOperation  # type: ignore
        if op_value == MultiCombineInputs.Operations.CUT.value:
            return adsk.fusion.FeatureOperations.CutFeatureOperation  # type: ignore
        if op_value == MultiCombineInputs.Operations.INTERSECT.value:
            return adsk.fusion.FeatureOperations.IntersectFeatureOperation  # type: ignore
        raise ValueError(f"Unsupported combine operation: {op_value}")
