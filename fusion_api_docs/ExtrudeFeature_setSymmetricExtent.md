# ExtrudeFeature.setSymmetricExtent Method

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Redefines the extrusion to go symmetrically in both directions from the profile.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"extrudeFeature_var" is a variable referencing an [ExtrudeFeature](ExtrudeFeature.md) object.

```python
# Uses no optional arguments.
returnValue = extrudeFeature_var.setSymmetricExtent(distance, isFullLength)

# Uses optional arguments.
returnValue = extrudeFeature_var.setSymmetricExtent(distance, isFullLength, taperAngle)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true, if the call was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| distance | [ValueInput](ValueInput.md) | The distance of the extrusions. This is either the full length of half of the length of the final extrusion depending on the value of the isFullLength property. |
| isFullLength | boolean | Defines if the value defines the full length of the extrusion or half of the length. A value of true indicates it defines the full length. |
| taperAngle | [ValueInput](ValueInput.md) | Optional argument that specifies the taper angle. The same taper angle is used for both sides for a symmetric extrusion. If omitted a taper angle of 0 is used. This is an optional argument whose default value is null. |

## Version

Introduced in version November 2016  

