# LoftFeatureInput.creationOccurrence Property

Parent Object: [LoftFeatureInput](LoftFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the loft is created based on geometry (e.g. a profile and/or face(s)) when the loft is being created in another component AND the loft is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"loftFeatureInput_var" is a variable referencing a LoftFeatureInput object.  

```python
# Get the value of the property.
propertyValue = loftFeatureInput_var.creationOccurrence

# Set the value of the property.
loftFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version August 2016  

