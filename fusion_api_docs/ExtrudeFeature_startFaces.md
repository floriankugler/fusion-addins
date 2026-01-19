# ExtrudeFeature.startFaces Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Property that returns the set of faces that cap the end of the extrusion and are coincident with the sketch plane. In the case of a symmetric extrusion, these faces are the ones on the positive normal side of the sketch plane. In the case where there are no start faces, this property will return null.

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.startFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version August 2014  

