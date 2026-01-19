# SweepFeature.startFaces Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Property that returns the set of that cap one end of the sweep that are coincident with the sketch plane. In the cases where there aren't any start faces this property will return Nothing.

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.startFaces
```

## Property Value

This is a read only property whose value is a [BRepFaces](BRepFaces.md).

## Version

Introduced in version November 2014  

