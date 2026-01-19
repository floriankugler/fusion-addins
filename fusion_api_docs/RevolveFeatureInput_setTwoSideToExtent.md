# RevolveFeatureInput.setTwoSideToExtent Method

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Defines the extents of the revolve to be from the sketch plane to specified faces in both directions. If the matchShape argument is true, the faces to revolve to are extended to fully intersect the revolve.

## Syntax

"revolveFeatureInput_var" is a variable referencing a [RevolveFeatureInput](RevolveFeatureInput.md) object.

```python
returnValue = revolveFeatureInput_var.setTwoSideToExtent(toEntityOne, toEntityTwo)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| toEntityOne | [Base](Base.md) | The first entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For a revolve it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |
| toEntityTwo | [Base](Base.md) | The second entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For a revolve it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |

## Version

Introduced in version August 2014  

