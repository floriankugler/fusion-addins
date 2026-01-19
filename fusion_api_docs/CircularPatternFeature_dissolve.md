# CircularPatternFeature.dissolve Method

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"circularPatternFeature_var" is a variable referencing a [CircularPatternFeature](CircularPatternFeature.md) object.

```python
returnValue = circularPatternFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version November 2014  

