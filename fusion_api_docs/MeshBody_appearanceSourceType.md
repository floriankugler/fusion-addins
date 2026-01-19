# MeshBody.appearanceSourceType Property

Parent Object: [MeshBody](MeshBody.md)  

## Description

Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists on this body. The override can be removed by setting the Appearance property to null.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.appearanceSourceType
```

## Property Value

This is a read only property whose value is an [AppearanceSourceTypes](AppearanceSourceTypes.md).

## Version

Introduced in version August 2016  

