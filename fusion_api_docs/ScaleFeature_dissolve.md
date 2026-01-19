# ScaleFeature.dissolve Method

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"scaleFeature_var" is a variable referencing a [ScaleFeature](ScaleFeature.md) object.

```python
returnValue = scaleFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version January 2015  

