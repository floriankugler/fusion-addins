# FilletFeature.convert Method

Parent Object: [FilletFeature](FilletFeature.md)  

## Description

Method that converts this feature to another fillet feature type.  

To use this method you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"filletFeature_var" is a variable referencing a [FilletFeature](FilletFeature.md) object.

```python
returnValue = filletFeature_var.convert(input)
```

## Return Value

| Type    | Description                                    |
|---------|------------------------------------------------|
| boolean | Returns true if the conversion was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [Base](Base.md) | Input a fillet feature input object that defines the desired fillet. Use the FilletFeatures.create\*Input methods to create a new fillet feature input object. This can be a feature input for fillet type, rule fillet type or full round fillet type. |

## Version

Introduced in version September 2025  

