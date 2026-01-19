# HoleFeatureInput.creationOccurrence Property

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Hole is created based on geometry (e.g. a face or point) in another component AND (the Hole) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI A value of null indicates that everything is in the context of a single component.

## Syntax

"holeFeatureInput_var" is a variable referencing a HoleFeatureInput object.  

```python
# Get the value of the property.
propertyValue = holeFeatureInput_var.creationOccurrence

# Set the value of the property.
holeFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version August 2014  

