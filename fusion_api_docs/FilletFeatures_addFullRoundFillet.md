# FilletFeatures.addFullRoundFillet Method

Parent Object: [FilletFeatures](FilletFeatures.md)  

## Description

Creates a new full round fillet feature.

## Syntax

"filletFeatures_var" is a variable referencing a [FilletFeatures](FilletFeatures.md) object.

```python
returnValue = filletFeatures_var.addFullRoundFillet(input)
```

## Return Value

| Type | Description |
|----|----|
| [FilletFeature](FilletFeature.md) | Returns the newly created FilletFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [FullRoundFilletFeatureInput](FullRoundFilletFeatureInput.md) | A FullRoundFilletFeatureInput object that defines the desired fillet. Use the createFullRoundFilletInput method to create a new FullRoundFilletFeatureInput object and then use methods on it (the FullRoundFilletFeatureInput object) to define the fillet. |

## Version

Introduced in version September 2025  

