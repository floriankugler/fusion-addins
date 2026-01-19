# ExtrudeFeature.setThinExtrude Method

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Changes the extrude feature to be a thin extrude. This is only valid if the isThinExtrude property is False. If the extrusion is already a thin extrude, you can use the properties on the ExtrudeFeature to modify the thin extrude specific values.

## Syntax

"extrudeFeature_var" is a variable referencing an [ExtrudeFeature](ExtrudeFeature.md) object.

```python
# Uses no optional arguments.
returnValue = extrudeFeature_var.setThinExtrude(thinExtrudeWallLocationOne, thinExtrudeWallThicknessOne)

# Uses optional arguments.
returnValue = extrudeFeature_var.setThinExtrude(thinExtrudeWallLocationOne, thinExtrudeWallThicknessOne, thinExtrudeWallLocationTwo, thinExtrudeWallThicknessTwo)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| thinExtrudeWallLocationOne | [ThinExtrudeWallLocation](ThinExtrudeWallLocation.md) | Specifies the position of the thin wall extrude with respect to the profile being extruded. This defines the direction for a single sided thin extrude or side one of a two-sided extrusion. |
| thinExtrudeWallThicknessOne | [ValueInput](ValueInput.md) | A ValueInput object that defines the thickness for a single sided thin extrude or side one of a two-sided extrusion . |
| thinExtrudeWallLocationTwo | [ThinExtrudeWallLocation](ThinExtrudeWallLocation.md) | Optional argument that specifies the position of side two of a two-sided extrusion. This argument is ignored for a single sided thin extrude. This is an optional argument whose default value is ThinExtrudeWallLocation.Side1. |
| thinExtrudeWallThicknessTwo | [ValueInput](ValueInput.md) | Optional argument that is a ValueInput object that defines the thickness for side two of a two-sided extrusion. This argument is ignored for a single sided thin extrude. This is an optional argument whose default value is null. |

## Version

Introduced in version April 2021  

