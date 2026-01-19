# RipFeature.dissolve Method

Parent Object: [RipFeature](RipFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"ripFeature_var" is a variable referencing a [RipFeature](RipFeature.md) object.

```python
returnValue = ripFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2023  

