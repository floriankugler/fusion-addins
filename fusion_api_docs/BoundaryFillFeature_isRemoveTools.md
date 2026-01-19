# BoundaryFillFeature.isRemoveTools Property

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

Gets and sets whether any BRepBodys that were used as tools should be removed as part of the feature creation.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"boundaryFillFeature_var" is a variable referencing a BoundaryFillFeature object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeature_var.isRemoveTools

# Set the value of the property.
boundaryFillFeature_var.isRemoveTools = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2022  

