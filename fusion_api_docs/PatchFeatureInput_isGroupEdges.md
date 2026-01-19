# PatchFeatureInput.isGroupEdges Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets if the edges in the boundary curve are treated as a group, and they all use the same continuity. If this property is True (which is the default), the continuity property controls the continuity for all edges. If this property is false; the continuity is set for each edge using the setContinuity method.  

When this property is set to true, the continuity and weight of the first edge will be used for all edges. When set to false, each edge will initially have the same continuity and weight. This is typically set to false as a side-effect of calling the setContinuity method.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.isGroupEdges

# Set the value of the property.
patchFeatureInput_var.isGroupEdges = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

