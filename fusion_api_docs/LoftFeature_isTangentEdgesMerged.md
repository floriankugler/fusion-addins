# LoftFeature.isTangentEdgesMerged Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Specifies if the loft will keep or merge tangent edges. These are edges between tangent faces in the resulting loft surface. If true, the faces will be merged so the connecting edge no longer exists

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.isTangentEdgesMerged

# Set the value of the property.
loftFeature_var.isTangentEdgesMerged = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2022  

