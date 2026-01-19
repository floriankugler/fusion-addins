# BaseFeature.dissolve Method

Parent Object: [BaseFeature](BaseFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"baseFeature_var" is a variable referencing a [BaseFeature](BaseFeature.md) object.

```python
returnValue = baseFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

