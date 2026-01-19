# PipeFeature.startFaces Property

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Property that returns the set of faces that cap one end of the Pipe that are coincident with the sketch plane. In the cases where there aren't any start faces this property will return null.

## Syntax

"pipeFeature_var" is a variable referencing a PipeFeature object.  

```python
# Get the value of the property.
propertyValue = pipeFeature_var.startFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version October 2023  

