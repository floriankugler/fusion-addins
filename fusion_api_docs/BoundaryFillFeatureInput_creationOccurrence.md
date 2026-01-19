# BoundaryFillFeatureInput.creationOccurrence Property

Parent Object: [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Boundary Fill is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the Boundary Fill) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"boundaryFillFeatureInput_var" is a variable referencing a BoundaryFillFeatureInput object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeatureInput_var.creationOccurrence

# Set the value of the property.
boundaryFillFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Samples

| Name | Description |
|----|----|
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |

## Version

Introduced in version June 2015  

