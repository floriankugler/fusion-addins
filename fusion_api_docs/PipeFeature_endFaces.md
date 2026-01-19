# PipeFeature.endFaces Property

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Property that returns the set of faces that cap one end of the Pipe that are coincident with the sketch plane. The end faces are those not coincident to the sketch plane of the feature's profile. In the case of a symmetric Pipe these faces are the ones on the negative normal side of the sketch plane. In the cases where there aren't any end faces this property will return null.

## Syntax

"pipeFeature_var" is a variable referencing a PipeFeature object.  

```python
# Get the value of the property.
propertyValue = pipeFeature_var.endFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version October 2023  

