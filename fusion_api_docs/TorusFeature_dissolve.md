# TorusFeature.dissolve Method

Parent Object: [TorusFeature](TorusFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"torusFeature_var" is a variable referencing a [TorusFeature](TorusFeature.md) object.

```python
returnValue = torusFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

