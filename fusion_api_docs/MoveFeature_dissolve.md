# MoveFeature.dissolve Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version March 2015  

