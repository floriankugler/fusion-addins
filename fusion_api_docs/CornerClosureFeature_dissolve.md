# CornerClosureFeature.dissolve Method

Parent Object: [CornerClosureFeature](CornerClosureFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"cornerClosureFeature_var" is a variable referencing a [CornerClosureFeature](CornerClosureFeature.md) object.

```python
returnValue = cornerClosureFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version January 2026  

