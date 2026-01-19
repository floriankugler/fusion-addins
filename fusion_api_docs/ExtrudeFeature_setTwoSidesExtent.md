# ExtrudeFeature.setTwoSidesExtent Method

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Redefines the extrusion to go in both directions from the profile. The extent is defined independently for each direction using the input arguments.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extrudeFeature_var" is a variable referencing an [ExtrudeFeature](ExtrudeFeature.md) object.

```python
# Uses no optional arguments.
returnValue = extrudeFeature_var.setTwoSidesExtent(sideOneExtent, sideTwoExtent)

# Uses optional arguments.
returnValue = extrudeFeature_var.setTwoSidesExtent(sideOneExtent, sideTwoExtent, sideOneTaperAngle, sideTwoTaperAngle)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true, if the call was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| sideOneExtent | [ExtentDefinition](ExtentDefinition.md) | An ExtentDefinition object that defines how the extent of the extrusion towards side one is defined. This can be a specified distance (DistanceExtentDefinition), to an entity (ToEntityExtent), or through-all (AllExtentDefinition). These objects can be obtained by using the static create method on the appropriate class. |
| sideTwoExtent | [ExtentDefinition](ExtentDefinition.md) | An ExtentDefinition object that defines how the extent of the extrusion towards side two is defined. This can be a specified distance (DistanceExtentDefinition), to an entity (ToEntityExtent), or through-all (AllExtentDefinition). These objects can be obtained by using the static create method on the appropriate class. |
| sideOneTaperAngle | [ValueInput](ValueInput.md) | Optional argument that specifies the taper angle for side one. If omitted a taper angle of 0 is used. This is an optional argument whose default value is null. |
| sideTwoTaperAngle | [ValueInput](ValueInput.md) | Optional argument that specifies the taper angle for side two. If omitted a taper angle of 0 is used. This is an optional argument whose default value is null. |

## Version

Introduced in version November 2016  

