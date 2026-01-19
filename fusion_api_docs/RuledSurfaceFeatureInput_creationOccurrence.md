# RuledSurfaceFeatureInput.creationOccurrence Property

Parent Object: [RuledSurfaceFeatureInput](RuledSurfaceFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Ruled Surface is created based on geometry (e.g. a profile) in another component AND (the Ruled Surface) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"ruledSurfaceFeatureInput_var" is a variable referencing a RuledSurfaceFeatureInput object.  

```python
# Get the value of the property.
propertyValue = ruledSurfaceFeatureInput_var.creationOccurrence

# Set the value of the property.
ruledSurfaceFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version September 2020  

