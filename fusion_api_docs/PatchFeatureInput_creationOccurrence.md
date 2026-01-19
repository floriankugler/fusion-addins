# PatchFeatureInput.creationOccurrence Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

For geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Patch feature is created based on geometry (e.g., a profile, edges, faces) in another component AND (the Patch feature) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.creationOccurrence

# Set the value of the property.
patchFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version July 2016  

