# FloatProperty.connectedTexture Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

When the property is associated with an appearance, this gets the associated texture, if one exists. The HasConnectedTexture property controls if there is an associated texture or not. If it's parent writable you can edit the texture. If no texture exists, this property will return null.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.connectedTexture
```

## Property Value

This is a read only property whose value is an [AppearanceTexture](AppearanceTexture.md).

## Version

Introduced in version August 2014  

