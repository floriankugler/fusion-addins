# LoftFeatureInput.isTangentEdgesMerged Property

Parent Object: [LoftFeatureInput](LoftFeatureInput.md)  

## Description

Specifies if the loft will keep or merge tangent edges. These are edges between tangent faces in the resulting loft surface. If true, the faces will be merged so the connecting edge no longer exists

## Syntax

"loftFeatureInput_var" is a variable referencing a LoftFeatureInput object.  

```python
# Get the value of the property.
propertyValue = loftFeatureInput_var.isTangentEdgesMerged

# Set the value of the property.
loftFeatureInput_var.isTangentEdgesMerged = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2022  

