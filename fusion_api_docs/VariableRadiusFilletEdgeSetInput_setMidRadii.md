# VariableRadiusFilletEdgeSetInput.setMidRadii Method

Parent Object: [VariableRadiusFilletEdgeSetInput](VariableRadiusFilletEdgeSetInput.md)  

## Description

Defines any additional points along the fillet where a radius is specified.

## Syntax

"variableRadiusFilletEdgeSetInput_var" is a variable referencing a [VariableRadiusFilletEdgeSetInput](VariableRadiusFilletEdgeSetInput.md) object.

```python
returnValue = variableRadiusFilletEdgeSetInput_var.setMidRadii(radii, positions)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| radii | ValueInput[] | An array of ValueInput objects that define the radii at positions along the edge(s). This array must have the same number of values as the positions argument. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the the units can be defined as part of the string (i.e. "2 in"). If no units are specified it will be interpreted using the current default units for length. |
| positions | ValueInput[] | An array of ValueInput objects that defines the positions of any additional radii along the edge(s). The value must be between 0 and 1 and defines the percentage along the curve where a radius is defined. This array must have the same number of values as the radii argument. If the ValueInput uses a real then it is interpreted as a unitless number. If it is a string then the the string must evaluate to a unitless number. |

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2022  

