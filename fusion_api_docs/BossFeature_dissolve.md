# BossFeature.dissolve Method

Parent Object: [BossFeature](BossFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"bossFeature_var" is a variable referencing a [BossFeature](BossFeature.md) object.

```python
returnValue = bossFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version October 2022  

