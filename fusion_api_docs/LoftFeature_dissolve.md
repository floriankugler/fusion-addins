# LoftFeature.dissolve Method

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"loftFeature_var" is a variable referencing a [LoftFeature](LoftFeature.md) object.

```python
returnValue = loftFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

