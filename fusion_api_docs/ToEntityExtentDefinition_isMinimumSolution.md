# ToEntityExtentDefinition.isMinimumSolution Property

Parent Object: [ToEntityExtentDefinition](ToEntityExtentDefinition.md)  

## Description

Gets and sets if the minimum or maximum solution is calculated. This is only used when the input entity is a body and defines if the extrusion to go to the near side (minimum solution) of the body or the far side. When a new ToEntityExtentDefinition object is created, this property defaults to True.

## Syntax

"toEntityExtentDefinition_var" is a variable referencing a ToEntityExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = toEntityExtentDefinition_var.isMinimumSolution

# Set the value of the property.
toEntityExtentDefinition_var.isMinimumSolution = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2016  

