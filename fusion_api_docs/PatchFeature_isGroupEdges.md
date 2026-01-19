# PatchFeature.isGroupEdges Property

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Gets and sets if the edges in the boundary curve are treated as a group , and they all use the same continuity. If this property is True (which is the default), the continuity for all edges is controlled by the continuity property. If this property is false; the continuity is set for each edge using the setContinuity method.  

When this property is set to true, the continuity and weight of the first edge will be used for all edges. When set to false, each edge will initially have the same continuity and weight. This property is typically set to false by calling the setContinuity method, which has the side effect of changing this to false.  

To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"patchFeature_var" is a variable referencing a PatchFeature object.  

```python
# Get the value of the property.
propertyValue = patchFeature_var.isGroupEdges

# Set the value of the property.
patchFeature_var.isGroupEdges = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

