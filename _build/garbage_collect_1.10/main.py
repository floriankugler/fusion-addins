from lib import addin, combine, ui_placement, utils
from lib.fusionbootstrap.runtime import RuntimeInfo
import adsk.fusion


_addin: addin.Addin | None = None


def run(context, runtime_info: RuntimeInfo):
    global _addin
    _addin = GarbageCollect(runtime_info)


def stop(context):
    global _addin
    if _addin:
        _addin.shutdown()
    _addin = None


class GarbageCollect(addin.Addin):
    @property
    def plugin_name(self) -> str:
        return "Garbage Collect"

    @property
    def plugin_desc(self) -> str:
        return "Cleans up orphaned external combine/base/intersect features."

    @property
    def plugin_tooltip(self) -> str:
        return "Cleans up orphaned external combine/base/intersect features."

    @property
    def has_command_ui(self) -> bool:
        return False

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

    def execute(self):
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if not design:
            utils.fusion.log("[Garbage Collect] Active product is not a design.")
            return
        combine.garbage_collect_features(design)
        utils.fusion.log("[Garbage Collect] Completed external feature garbage collection.")
