# ExtrudeFeatureInput.setOneSideExtent Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Defines the extrusion to go in one direction from the profile. The extent of the extrusion is defined by the extent argument.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
# Uses no optional arguments.
returnValue = extrudeFeatureInput_var.setOneSideExtent(extent, direction)

# Uses optional arguments.
returnValue = extrudeFeatureInput_var.setOneSideExtent(extent, direction, taperAngle)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true is setting the input to a one sided extent was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| extent | [ExtentDefinition](ExtentDefinition.md) | An ExtentDefinition object that defines how the extent of the extrusion is defined. This can be a specified distance (DistanceExtentDefinition), to an entity (ToEntityExtent), or through-all (AllExtentDefinition). These objects can be obtained by using the static create method on the appropriate class. |
| direction | [ExtentDirections](ExtentDirections.md) | Specifies the direction of the extrusion. PositiveExtentDirection and NegativeExtentDirection are valid values. PositiveExtentDirection is in the same direction as the normal of the profile's parent sketch plane. |
| taperAngle | [ValueInput](ValueInput.md) | Optional argument that specifies the taper angle. If omitted a taper angle of 0 is used. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [extrudeFeatures.add using setOneSideExtent](extrudeFeaturesOneSideExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setOneSideExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion. |
| [extrudeFeatures.add using ThroughAllExtent](extrudeFeaturesThroughAllExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the ThroughAllExtent method. |
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |

## Version

Introduced in version November 2016  

