# RipFeatures.add Method

Parent Object: [RipFeatures](RipFeatures.md)  

## Description

Creates a new Rip feature.

## Syntax

"ripFeatures_var" is a variable referencing a [RipFeatures](RipFeatures.md) object.

```python
returnValue = ripFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [RipFeature](RipFeature.md) | Returns the newly created RipFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [RipFeatureInput](RipFeatureInput.md) | A RipFeatureInput object that defines the desired rip. Use the createInput method to create a new RipFeatureInput object and then use methods on it (the RipFeatureInput object) to define the rip. |

## Version

Introduced in version September 2023  

