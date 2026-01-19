# ColorProperty.hasConnectedTexture Property

Parent Object: [ColorProperty](ColorProperty.md)  

## Description

Specifies if this color is specified using a simple color or a texture. If this returns true the color is defined using a texture. If the parent is writable, this property can be set to true to change the definition from a simple color to a texture. You can then use the ConnectedTexture property to get the associated texture and modify it.

## Syntax

"colorProperty_var" is a variable referencing a ColorProperty object.  

```python
# Get the value of the property.
propertyValue = colorProperty_var.hasConnectedTexture

# Set the value of the property.
colorProperty_var.hasConnectedTexture = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

