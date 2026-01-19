# InterferenceResult.interferenceBody Property

Parent Object: [InterferenceResult](InterferenceResult.md)  

## Description

Returns a transient BRepBody that represents the volume of interference.

## Syntax

"interferenceResult_var" is a variable referencing an InterferenceResult object.  

```python
# Get the value of the property.
propertyValue = interferenceResult_var.interferenceBody
```

## Property Value

This is a read only property whose value is a [BRepBody](BRepBody.md).

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |

## Version

Introduced in version November 2015  

