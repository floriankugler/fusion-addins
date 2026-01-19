# MeshBody.appearance Property

Parent Object: [MeshBody](MeshBody.md)  

## Description

Read-write property that gets and sets the current appearance of the body. Setting this property will result in applying an override appearance to the body and the AppearanceSourceType property will return OverrideAppearanceSource. Setting this property to null will remove any override.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.appearance

# Set the value of the property.
meshBody_var.appearance = propertyValue
```

## Property Value

This is a read/write property whose value is an [Appearance](Appearance.md).

## Version

Introduced in version August 2016  

