# BossFeatureInput.creationOccurrence Property

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the boss feature is created based on geometry (e.g. point) in another component AND (the boss) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI A value of null indicates that everything is in the context of a single component. The occurrence provided sets scope for detection of target participant bodies.

## Syntax

"bossFeatureInput_var" is a variable referencing a BossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = bossFeatureInput_var.creationOccurrence

# Set the value of the property.
bossFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version October 2022  

