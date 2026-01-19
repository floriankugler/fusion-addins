# TrimFeature.dissolve Method

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"trimFeature_var" is a variable referencing a [TrimFeature](TrimFeature.md) object.

```python
returnValue = trimFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version July 2015  

