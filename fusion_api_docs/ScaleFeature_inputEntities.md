# ScaleFeature.inputEntities Property

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Gets and sets the input entities. This collection can contain sketches, BRep bodies and T-Spline bodies in parametric modeling. It can contain sketches, BRep bodies, T-Spline bodies, mesh bodies, root component and occurrences in non-parametric modeling. If the scaling is non-uniform (the isUniform property is false), this collection cannot contain sketches or components.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"scaleFeature_var" is a variable referencing a ScaleFeature object.  

```python
# Get the value of the property.
propertyValue = scaleFeature_var.inputEntities

# Set the value of the property.
scaleFeature_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version January 2015  

