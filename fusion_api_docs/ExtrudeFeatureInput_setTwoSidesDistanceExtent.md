# ExtrudeFeatureInput.setTwoSidesDistanceExtent Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Sets the extrusion extents option to 'Two Side'. This method will fail in the case of a non-parametric extrusion.

## Remarks

This method has been retired and is replaced with the new SetTwoSidesExtent, passing in a DistanceExtentDefinition for both sides. This method continues to work to allow the API to remain backward compatible, but it is no longer officially supported.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
returnValue = extrudeFeatureInput_var.setTwoSidesDistanceExtent(distanceOne, distanceTwo)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| distanceOne | [ValueInput](ValueInput.md) | ValueInput object that defines the extrude distance for the first side. |
| distanceTwo | [ValueInput](ValueInput.md) | ValueInput object that defines the extrude distance for the second side. |

## Version

Introduced in version August 2014  
Retired in version November 2016  

