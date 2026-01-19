# BRepBody.appearanceSourceType Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Read-write property that gets the source of the appearance for the body. If this returns OverrideAppearanceSource, an override exists on this body. The override can be removed by setting the Appearance property to null.  

This property is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.appearanceSourceType
```

## Property Value

This is a read only property whose value is an [AppearanceSourceTypes](AppearanceSourceTypes.md).

## Version

Introduced in version August 2014  

