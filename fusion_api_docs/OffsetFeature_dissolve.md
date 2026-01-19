# OffsetFeature.dissolve Method

Parent Object: [OffsetFeature](OffsetFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"offsetFeature_var" is a variable referencing an [OffsetFeature](OffsetFeature.md) object.

```python
returnValue = offsetFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2015  

