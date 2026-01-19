# BRepFace.appearance Property

Parent Object: [BRepFace](BRepFace.md)  

## Description

Read-write property that gets and sets the current appearance of the face. Setting this property will result in applying an override appearance to the face and the AppearanceSourceType property will return OverrideAppearanceSource. Setting this property to null will remove any override.

## Syntax

"bRepFace_var" is a variable referencing a BRepFace object.  

```python
# Get the value of the property.
propertyValue = bRepFace_var.appearance

# Set the value of the property.
bRepFace_var.appearance = propertyValue
```

## Property Value

This is a read/write property whose value is an [Appearance](Appearance.md).

## Version

Introduced in version August 2014  

