# ThickenFeatureInput.creationOccurrence Property

Parent Object: [ThickenFeatureInput](ThickenFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Thicken feature is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the Thicken feature) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI

## Syntax

"thickenFeatureInput_var" is a variable referencing a ThickenFeatureInput object.  

```python
# Get the value of the property.
propertyValue = thickenFeatureInput_var.creationOccurrence

# Set the value of the property.
thickenFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version October 2022  

