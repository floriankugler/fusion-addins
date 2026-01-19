# ChamferFeatures.createInput Method

Parent Object: [ChamferFeatures](ChamferFeatures.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates a ChamferFeatureInput object. Use properties and methods on this object to define the chamfer you want to create and then use the Add method, passing in the ChamferFeatureInput object.

## Syntax

"chamferFeatures_var" is a variable referencing a [ChamferFeatures](ChamferFeatures.md) object.

```python
returnValue = chamferFeatures_var.createInput(edges, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferFeatureInput](ChamferFeatureInput.md) | Returns the newly created ChamferFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edges | [ObjectCollection](ObjectCollection.md) | The collection of edges that will be chamfered. |
| isTangentChain | boolean | Boolean indicating if all edges that are tangentially connected to any of the input edges should be included in the chamfer or not. |

## Version

Introduced in version November 2014  
Retired in version December 2020  

