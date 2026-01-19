# ChamferFeature.edges Property

Parent Object: [ChamferFeature](ChamferFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the edges being chamfered. Specific edges can be defined using one or more BRepEdge objects or BRepFace objects can be used to chamfer all edges of the face or Feature objects can be used to chamfer all edges associated with the input features. If BRepEdge objects are provided and the isTangentChain argument is true additional edges may also get chamfered if they are tangentially connected to any of the input edges. When getting the property, your code should check for the different types in the returned collection and handle it appropriately.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

This property returns nothing in the case where the feature is non-parametric.

## Syntax

"chamferFeature_var" is a variable referencing a ChamferFeature object.  

```python
# Get the value of the property.
propertyValue = chamferFeature_var.edges

# Set the value of the property.
chamferFeature_var.edges = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  
Retired in version December 2020  

