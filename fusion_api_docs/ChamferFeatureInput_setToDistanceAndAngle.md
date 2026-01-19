# ChamferFeatureInput.setToDistanceAndAngle Method

Parent Object: [ChamferFeatureInput](ChamferFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Adds a set of edges to this input.

## Syntax

"chamferFeatureInput_var" is a variable referencing a [ChamferFeatureInput](ChamferFeatureInput.md) object.

```python
returnValue = chamferFeatureInput_var.setToDistanceAndAngle(distance, angle)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| distance | [ValueInput](ValueInput.md) | A ValueInput object that defines the distance of the chamfer. This distance is along the face which is on the right of the selected edge. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in"). If no units are specified it is interpreted using the current default units for length. |
| angle | [ValueInput](ValueInput.md) | A valueInput object that defines the angle. The direction will be towards to the face which is on the left of the selected edge. This can be a string or a value. If it's a string it is interpreted using the current document units and can include equations. For example all of the following are valid as long as they result in angle units; "45", "45 deg", "a1 / 2". If a value is input it is interpreted as radians. It cannot be negative. |

## Version

Introduced in version November 2014  
Retired in version December 2020  

