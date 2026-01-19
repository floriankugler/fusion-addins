# ReverseNormalFeature.dissolve Method

Parent Object: [ReverseNormalFeature](ReverseNormalFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"reverseNormalFeature_var" is a variable referencing a [ReverseNormalFeature](ReverseNormalFeature.md) object.

```python
returnValue = reverseNormalFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

