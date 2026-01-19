# BRepFace.appearanceSourceType Property

Parent Object: [BRepFace](BRepFace.md)  

## Description

Read-write property that gets the source of the appearance for the face. If this returns OverrideAppearanceSource, an override exists on this face. The override can be removed by setting the Appearance property to null.

## Syntax

"bRepFace_var" is a variable referencing a BRepFace object.  

```python
# Get the value of the property.
propertyValue = bRepFace_var.appearanceSourceType
```

## Property Value

This is a read only property whose value is an [AppearanceSourceTypes](AppearanceSourceTypes.md).

## Version

Introduced in version August 2014  

