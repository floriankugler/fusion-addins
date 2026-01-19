# ExtrudeFeature.endFaces Property

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Property that returns the set of faces that cap the end of the extrusion, opposite the start faces. In the case where there are no end faces, this property will return null.

## Syntax

"extrudeFeature_var" is a variable referencing an ExtrudeFeature object.  

```python
# Get the value of the property.
propertyValue = extrudeFeature_var.endFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

