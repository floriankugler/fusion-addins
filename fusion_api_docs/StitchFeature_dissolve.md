# StitchFeature.dissolve Method

Parent Object: [StitchFeature](StitchFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"stitchFeature_var" is a variable referencing a [StitchFeature](StitchFeature.md) object.

```python
returnValue = stitchFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2015  

