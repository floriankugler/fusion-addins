# ExtrudeFeatureInput.setThinExtrude Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Changes the extrude feature to be a thin extrude. This is only valid if the isThinExtrude property is False. If the extrusion is already a thin extrude, you can use the properties on the ExtrudeFeature to modify the thin extrude specific values.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
# Uses no optional arguments.
returnValue = extrudeFeatureInput_var.setThinExtrude(thinExtrudeWallLocationOne, thinExtrudeWallThicknessOne)

# Uses optional arguments.
returnValue = extrudeFeatureInput_var.setThinExtrude(thinExtrudeWallLocationOne, thinExtrudeWallThicknessOne, thinExtrudeWallLocationTwo, thinExtrudeWallThicknessTwo)
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

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.add using thin extrude](extrudeFeaturesThin_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setThinExtrude method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the thin extrusion. |

## Version

Introduced in version April 2021  

