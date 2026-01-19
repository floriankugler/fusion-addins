# BoundaryFillFeature.tools Property

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

A collection of construction planes and open or closed BRepBody objects that define the set of boundaries that have been used in the calculation of available closed boundaries. Setting this property will clear all currently selected tools.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"boundaryFillFeature_var" is a variable referencing a BoundaryFillFeature object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeature_var.tools

# Set the value of the property.
boundaryFillFeature_var.tools = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

