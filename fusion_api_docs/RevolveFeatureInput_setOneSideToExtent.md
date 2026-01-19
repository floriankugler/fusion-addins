# RevolveFeatureInput.setOneSideToExtent Method

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Defines the extent of the revolve to be from the sketch or profile plane to the specified "To" face.

## Syntax

"revolveFeatureInput_var" is a variable referencing a [RevolveFeatureInput](RevolveFeatureInput.md) object.

```python
# Uses no optional arguments.
returnValue = revolveFeatureInput_var.setOneSideToExtent(toEntity)

# Uses optional arguments.
returnValue = revolveFeatureInput_var.setOneSideToExtent(toEntity, directionHint)
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

