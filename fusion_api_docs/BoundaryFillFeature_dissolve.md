# BoundaryFillFeature.dissolve Method

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"boundaryFillFeature_var" is a variable referencing a [BoundaryFillFeature](BoundaryFillFeature.md) object.

```python
returnValue = boundaryFillFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2015  

