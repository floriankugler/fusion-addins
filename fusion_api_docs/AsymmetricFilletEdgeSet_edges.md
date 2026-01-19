# AsymmetricFilletEdgeSet.edges Property

Parent Object: [AsymmetricFilletEdgeSet](AsymmetricFilletEdgeSet.md)  

## Description

Gets and sets an ObjectCollection containing the BRepEdge, BRepFace, and Feature that are filleted. If the isTangentChain argument is true additional edges or faces may also get filleted if they are tangentially connected to any of the input edges or faces.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"asymmetricFilletEdgeSet_var" is a variable referencing an AsymmetricFilletEdgeSet object.  

```python
# Get the value of the property.
propertyValue = asymmetricFilletEdgeSet_var.edges

# Set the value of the property.
asymmetricFilletEdgeSet_var.edges = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2025  

