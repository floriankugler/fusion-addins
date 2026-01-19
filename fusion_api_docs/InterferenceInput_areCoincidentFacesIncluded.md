# InterferenceInput.areCoincidentFacesIncluded Property

Parent Object: [InterferenceInput](InterferenceInput.md)  

## Description

Gets and sets whether any coincident faces in the input bodies are considered as interference or not. This property defaults to False for a newly created InterferenceInput object.

## Syntax

"interferenceInput_var" is a variable referencing an InterferenceInput object.  

```python
# Get the value of the property.
propertyValue = interferenceInput_var.areCoincidentFacesIncluded

# Set the value of the property.
interferenceInput_var.areCoincidentFacesIncluded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |

## Version

Introduced in version November 2015  

