# SetupInput.stockSolids Property

Parent Object: [SetupInput](SetupInput.md)  

## Description

An array of models, where a model can be an Occurrence, ManufacturingModel, BRepBody, or MeshBody. Setting this property, or adding the first object to the returned array will automatically set the stockMode to "SolidStock".  

The returned array is connected to the SetupInput and can be added to directly without needing to create a new array, populate it, and assign it using this property, although, that is supported too.

## Syntax

"setupInput_var" is a variable referencing a SetupInput object.  

```python
# Get the value of the property.
propertyValue = setupInput_var.stockSolids

# Set the value of the property.
setupInput_var.stockSolids = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version April 2023  

