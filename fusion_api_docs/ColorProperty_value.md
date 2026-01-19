# ColorProperty.value Property

Parent Object: [ColorProperty](ColorProperty.md)  

## Description

Gets and sets this property value if there is a color and not a texture defining this color. If a texture is used, this property returns null. Setting this property when a texture is used removes the texture and changes the color definition to a simple color.

## Syntax

"colorProperty_var" is a variable referencing a ColorProperty object.  

```python
# Get the value of the property.
propertyValue = colorProperty_var.value

# Set the value of the property.
colorProperty_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a [Color](Color.md).

## Version

Introduced in version August 2014  

