# SweepFeatureInput.creationOccurrence Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the sweep is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the sweep) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.creationOccurrence

# Set the value of the property.
sweepFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version November 2014  

