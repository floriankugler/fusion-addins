# OneSideToExtentDefinition.matchShape Property

Parent Object: [OneSideToExtentDefinition](OneSideToExtentDefinition.md)  

## Description

Specifies if the face should be extended or use adjacent faces if necessary to define the termination of the extrusion. When used for a revolve feature this is ignored and is always treated as true.

## Syntax

"oneSideToExtentDefinition_var" is a variable referencing an OneSideToExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = oneSideToExtentDefinition_var.matchShape

# Set the value of the property.
oneSideToExtentDefinition_var.matchShape = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2022  

