# RevolveFeature.startFaces Property

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Property that returns the set of faces that cap one end of the revolve and are coincident with the sketch plane. In the case of a symmetric revolve these faces are the ones on the positive normal side of the sketch plane. In the case where there aren't any start faces, this property will return null.

## Syntax

"revolveFeature_var" is a variable referencing a RevolveFeature object.  

```python
# Get the value of the property.
propertyValue = revolveFeature_var.startFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version August 2014  

