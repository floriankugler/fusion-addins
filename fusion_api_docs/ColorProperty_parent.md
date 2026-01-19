# ColorProperty.parent Property

Parent Object: [ColorProperty](ColorProperty.md)  

## Description

Returns the parent of this property.For properties associated with an appearance this will return the parent Appearance. For properties associated with a material, this will return the parent Material. For other types of properties, this will return the PropertyGroup it is in.

## Syntax

"colorProperty_var" is a variable referencing a ColorProperty object.  

```python
# Get the value of the property.
propertyValue = colorProperty_var.parent
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

