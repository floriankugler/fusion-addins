# NCProgramPostProcessOptions.isFailOnToolNumberDuplication Property

Parent Object: [NCProgramPostProcessOptions](NCProgramPostProcessOptions.md)  

## Description

Toggles whether the post processing should abort if two tools with the same tool number have been detected. True by default. If true, an exception will be thrown if at least two tools map to the same tool number. If false, the post processor will not perform a tool change if the tool number is the same, which may mean that the wrong tool is used for an operation.

## Syntax

"nCProgramPostProcessOptions_var" is a variable referencing a NCProgramPostProcessOptions object.  

```python
# Get the value of the property.
propertyValue = nCProgramPostProcessOptions_var.isFailOnToolNumberDuplication

# Set the value of the property.
nCProgramPostProcessOptions_var.isFailOnToolNumberDuplication = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2023  

