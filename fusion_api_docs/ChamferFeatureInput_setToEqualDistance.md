# ChamferFeatureInput.setToEqualDistance Method

Parent Object: [ChamferFeatureInput](ChamferFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Adds a set of edges to this input.

## Syntax

"chamferFeatureInput_var" is a variable referencing a [ChamferFeatureInput](ChamferFeatureInput.md) object.

```python
returnValue = chamferFeatureInput_var.setToEqualDistance(distance)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the set of edges was successfully added to the ChamferFeatureInput. |

## Parameters

| Name | Type | Description |
|----|----|----|
| distance | [ValueInput](ValueInput.md) | A ValueInput object that defines the size of the chamfer. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in"). If no units are specified it is interpreted using the current default units for length. |

## Version

Introduced in version November 2014  
Retired in version December 2020  

