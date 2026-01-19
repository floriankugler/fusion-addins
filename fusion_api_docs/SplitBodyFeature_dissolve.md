# SplitBodyFeature.dissolve Method

Parent Object: [SplitBodyFeature](SplitBodyFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"splitBodyFeature_var" is a variable referencing a [SplitBodyFeature](SplitBodyFeature.md) object.

```python
returnValue = splitBodyFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2015  

