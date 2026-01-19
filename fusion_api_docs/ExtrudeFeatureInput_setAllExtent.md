# ExtrudeFeatureInput.setAllExtent Method

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Sets the extrusion extents option to 'All' (i.e. the extrusion is through-all, in both directions.) This method will fail in the case of a non-parametric extrusion.

## Remarks

This method has been retired and is replaced with the setOneSideExtent and SetTwoSidesExtent, passing in a ThroughAllExtentDefinition. This method continues to work to allow the API to remain backward compatible, but it is no longer officially supported.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an [ExtrudeFeatureInput](ExtrudeFeatureInput.md) object.

```python
returnValue = extrudeFeatureInput_var.setAllExtent(direction)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| direction | [ExtentDirections](ExtentDirections.md) | The direction can be either positive, negative, or symmetric. |

## Version

Introduced in version August 2014  
Retired in version November 2016  

