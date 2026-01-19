# SplitFaceFeature.dissolve Method

Parent Object: [SplitFaceFeature](SplitFaceFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"splitFaceFeature_var" is a variable referencing a [SplitFaceFeature](SplitFaceFeature.md) object.

```python
returnValue = splitFaceFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2015  

