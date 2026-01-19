# ShellFeatureInput.inputEntities Property

Parent Object: [ShellFeatureInput](ShellFeatureInput.md)  

## Description

Gets and sets the input faces/bodies. If IsTangentChain is true, all the faces that are tangentially connected to the input faces (if any) will also be included. Fails if any faces are input, and the owning bodies of the faces are also input.

## Syntax

"shellFeatureInput_var" is a variable referencing a ShellFeatureInput object.  

```python
# Get the value of the property.
propertyValue = shellFeatureInput_var.inputEntities

# Set the value of the property.
shellFeatureInput_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  

