# PatchFeatureInput.groupIsContinuityDirectionFlipped Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets the continuity direction for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to false. The value of this property is ignored if the isGroupEdges property is false.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.groupIsContinuityDirectionFlipped

# Set the value of the property.
patchFeatureInput_var.groupIsContinuityDirectionFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

