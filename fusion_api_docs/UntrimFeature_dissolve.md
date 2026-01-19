# UntrimFeature.dissolve Method

Parent Object: [UntrimFeature](UntrimFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"untrimFeature_var" is a variable referencing a [UntrimFeature](UntrimFeature.md) object.

```python
returnValue = untrimFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version January 2021  

