# RevolveFeature.setOneSideToExtent Method

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Changes the extent of the revolve to be from the sketch plane to the specified "to" face.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a [RevolveFeature](RevolveFeature.md) object.

```python
# Uses no optional arguments.
returnValue = revolveFeature_var.setOneSideToExtent(toEntity)

# Uses optional arguments.
returnValue = revolveFeature_var.setOneSideToExtent(toEntity, directionHint)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| toEntity | [Base](Base.md) | The entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For a revolve it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |
| directionHint | [Vector3D](Vector3D.md) | Specifies the direction of the revolve. This is an optional argument whose default value is null. |

## Version

Introduced in version August 2014  

