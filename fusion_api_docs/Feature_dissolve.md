# Feature.dissolve Method

Parent Object: [Feature](Feature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"feature_var" is a variable referencing a [Feature](Feature.md) object.

```python
returnValue = feature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version August 2014  

