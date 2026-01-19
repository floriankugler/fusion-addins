# InterferenceInput.entities Property

Parent Object: [InterferenceInput](InterferenceInput.md)  

## Description

Gets and set an ObjectCollection containing BRepBody and/or Occurrence entities that will be used when checking for interference. All entities must be in the context of the root component of the top-level design.

## Syntax

"interferenceInput_var" is a variable referencing an InterferenceInput object.  

```python
# Get the value of the property.
propertyValue = interferenceInput_var.entities

# Set the value of the property.
interferenceInput_var.entities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2015  

