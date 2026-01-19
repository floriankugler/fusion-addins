# RevolveFeature.setTwoSidesToExtent Method

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Changes the extent of the revolve to be defined as a two sided to extent.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a [RevolveFeature](RevolveFeature.md) object.

```python
returnValue = revolveFeature_var.setTwoSidesToExtent(toEntityOne, toEntityTwo)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| toEntityOne | [Base](Base.md) | The first entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For a revolve it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |
| toEntityTwo | [Base](Base.md) | The second entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For a revolve it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |

## Version

Introduced in version August 2014  

