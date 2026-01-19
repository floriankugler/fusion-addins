# CAMParameter.expression Property

Parent Object: [CAMParameter](CAMParameter.md)  

## Description

Gets and sets the value expression of the parameter.

## Syntax

"cAMParameter_var" is a variable referencing a CAMParameter object.  

```python
# Get the value of the property.
propertyValue = cAMParameter_var.expression

# Set the value of the property.
cAMParameter_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
| --- | --- |
| [CAM Parameter Modification API Sample](CAMParameterChange_Sample_Sample.md) | Demonstrates changing parameters of existing toolpaths. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |

## Version

Introduced in version September 2020  

