# ExtrudeFeatureInput.setTwoSidesToExtent Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Set the extrusion Direction option to 'Two Side'. This method will fail in the case of a non-parametric extrusion.

## Remarks

This method has been retired and is replaced with the new setTwoSidesExtent and passing in a ToEntityExtentDefinition for both sides. This method continues to work to allow the API to remain backward compatible, but it is no longer officially supported.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
returnValue = extrudeFeatureInput_var.setTwoSidesToExtent(toEntityOne, toEntityTwo, matchShape)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| toEntityOne | [Base](Base.md) | The first entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For an extrude it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |
| toEntityTwo | [Base](Base.md) | The second entity that defines the "to" extent. The valid types of entities can vary depending on the type of feature this is being used with. For an extrude it can be a BRepBody, BRepFace, BRepVertex, ConstructionPlane, or ConstructionPoint. |
| matchShape | boolean | If the matchShape argument is 'true', the toEntity is extended to fully intersect the extrusion. |

## Version

Introduced in version August 2014  
Retired in version November 2016  

