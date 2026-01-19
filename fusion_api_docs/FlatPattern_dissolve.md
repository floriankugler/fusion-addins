# FlatPattern.dissolve Method

Parent Object: [FlatPattern](FlatPattern.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"flatPattern_var" is a variable referencing a [FlatPattern](FlatPattern.md) object.

```python
returnValue = flatPattern_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version October 2022  

