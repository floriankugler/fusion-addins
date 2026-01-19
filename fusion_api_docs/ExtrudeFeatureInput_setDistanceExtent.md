# ExtrudeFeatureInput.setDistanceExtent Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Sets the extrusion extents option to 'Distance'.

## Remarks

This method has been retired and is replaced with the new SetOneSideExtent and passing in either a DistanceExtentDefinition or SymmetricExtentDefinition. This method continues to work for the API to remain backward compatible but it is not longer officially supported.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
returnValue = extrudeFeatureInput_var.setDistanceExtent(isSymmetric, distance)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| isSymmetric | boolean | Set to 'true' for an extrusion symmetrical about the profile plane |
| distance | [ValueInput](ValueInput.md) | ValueInput object that defines the extrude distance. If the isSymmetric argument is 'false', a positive or negative distance can be used to control the direction. |

## Version

Introduced in version November 2016  
Retired in version September 2022  

