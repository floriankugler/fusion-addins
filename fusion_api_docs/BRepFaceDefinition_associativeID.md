# BRepFaceDefinition.associativeID Property

Parent Object: [BRepFaceDefinition](BRepFaceDefinition.md)  

## Description

Gets and sets the associate ID of this face definition. This ID will be copied to the corresponding face when the BRepBodyDefinition is used to create a BrepBody. It is used by Fusion as the identifier for the face and is used for tracking this geometry for parametric recomputes.

## Syntax

"bRepFaceDefinition_var" is a variable referencing a BRepFaceDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepFaceDefinition_var.associativeID

# Set the value of the property.
bRepFaceDefinition_var.associativeID = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version September 2020  

