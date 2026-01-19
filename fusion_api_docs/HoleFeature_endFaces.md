# HoleFeature.endFaces Property

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Property that returns the faces at the bottom of the hole. This will typically be a single face but could return more than one face in the case where the bottom of the hole is uneven.

## Syntax

"holeFeature_var" is a variable referencing a HoleFeature object.  

```python
# Get the value of the property.
propertyValue = holeFeature_var.endFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version August 2014  

