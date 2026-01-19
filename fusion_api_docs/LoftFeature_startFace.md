# LoftFeature.startFace Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Property that returns the face that caps the start of the loft and is coincident with the first section. In the case where the loft isn't capped and there isn't a start face, this property will return null.

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.startFace
```

## Property Value

This is a read only property whose value is a [BRepFace](BRepFace.md).

## Version

Introduced in version August 2016  

