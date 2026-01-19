# ColorProperty.connectedTexture Property

Parent Object: [ColorProperty](ColorProperty.md)  

## Description

Used for appearances and gets the associated texture, if one exists. The HasConnectedTexture property controls if there is an associated texture or not. If the parent is writable you can edit the texture. If no texture exists, this property will return null.

## Syntax

"colorProperty_var" is a variable referencing a ColorProperty object.  

```python
# Get the value of the property.
propertyValue = colorProperty_var.connectedTexture
```

## Property Value

This is a read only property whose value is an [AppearanceTexture](AppearanceTexture.md).

## Version

Introduced in version August 2014  

