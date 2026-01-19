# OperationInput.generationMode Property

Parent Object: [OperationInput](OperationInput.md)  

## Description

Defines the automatic generation during the creation of the operation. Can be used to force or skip the generation of the new operation. By default the newly created operation will not be generated. The default value is SkipGeneration.

## Syntax

"operationInput_var" is a variable referencing an OperationInput object.  

```python
# Get the value of the property.
propertyValue = operationInput_var.generationMode

# Set the value of the property.
operationInput_var.generationMode = propertyValue
```

## Property Value

This is a read/write property whose value is an [AutomaticGenerationModes](AutomaticGenerationModes.md).

## Version

Introduced in version April 2023  

