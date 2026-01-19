# ExtrudeFeature.dissolve Method

Parent Object: [ExtrudeFeature](ExtrudeFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"extrudeFeature_var" is a variable referencing an [ExtrudeFeature](ExtrudeFeature.md) object.

```python
returnValue = extrudeFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version August 2014  

