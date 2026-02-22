from lib import inputs, ui_placement
from lib.addin import Addin
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.core, adsk.fusion
from typing import cast

_addin: Addin


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = FlattenDesign(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class FlattenInputs(inputs.Inputs):
    def __init__(self, units_manager: adsk.core.UnitsManager):
        units = units_manager.defaultLengthUnits
        self.minimum_extent = inputs.FloatInput(
            id="minimumExtent",
            name="Minimum Extent",
            default_value=5,
            tool_tip="Minimum extent of bodies to keep.",
            units=units,
        )
        super().__init__()


class FlattenDesign(Addin):
    inputs: FlattenInputs

    @property
    def plugin_name(self) -> str:
        return "Flatten Design"

    @property
    def plugin_desc(self) -> str:
        return "Flatten hierarchy into root and remove small bodies."

    @property
    def plugin_tooltip(self) -> str:
        return "Flatten hierarchy into root and remove small bodies."

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

    def create_inputs(self) -> FlattenInputs:
        return FlattenInputs(self.app.activeProduct.unitsManager)

    def execute(self):
        design = cast(adsk.fusion.Design, self.app.activeProduct)
        root_comp = design.rootComponent
        min_extent = self.inputs.minimum_extent.value

        occurrences = [occ for occ in root_comp.allOccurrences]

        for occ in occurrences:
            for body in occ.bRepBodies:
                if _max_extent(body) > min_extent:
                    body.copyToComponent(root_comp)

        # Remove small bodies already in root.
        for body in list(root_comp.bRepBodies):
            if _max_extent(body) <= min_extent:
                body.deleteMe()

        if occurrences:
            design.deleteEntities(adsk.core.ObjectCollection.createWithArray(cast(list[adsk.core.Base], occurrences)))


def _max_extent(body: adsk.fusion.BRepBody) -> float:
    bb = body.boundingBox
    return max(
        abs(bb.maxPoint.x - bb.minPoint.x),
        abs(bb.maxPoint.y - bb.minPoint.y),
        abs(bb.maxPoint.z - bb.minPoint.z),
    )
