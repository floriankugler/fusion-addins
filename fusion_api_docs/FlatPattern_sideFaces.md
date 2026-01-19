# FlatPattern.sideFaces Property

Parent Object: [FlatPattern](FlatPattern.md)  

## Description

Returns the "side" faces of the flat pattern B-Rep body. These are the faces around the edge of the flat pattern that connect the top and bottom faces.

## Syntax

"flatPattern_var" is a variable referencing a FlatPattern object.  

```python
# Get the value of the property.
propertyValue = flatPattern_var.sideFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version October 2022  

