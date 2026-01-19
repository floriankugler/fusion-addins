# MergeFacesFeatureInput.creationOccurrence Property

Parent Object: [MergeFacesFeatureInput](MergeFacesFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Merge is created based on geometry (e.g. faces) in another component AND (Merge) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"mergeFacesFeatureInput_var" is a variable referencing a MergeFacesFeatureInput object.  

```python
# Get the value of the property.
propertyValue = mergeFacesFeatureInput_var.creationOccurrence

# Set the value of the property.
mergeFacesFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version September 2024  

