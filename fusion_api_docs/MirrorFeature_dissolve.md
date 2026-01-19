# MirrorFeature.dissolve Method

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"mirrorFeature_var" is a variable referencing a [MirrorFeature](MirrorFeature.md) object.

```python
returnValue = mirrorFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version November 2014  

