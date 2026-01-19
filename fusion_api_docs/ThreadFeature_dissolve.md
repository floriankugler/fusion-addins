# ThreadFeature.dissolve Method

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"threadFeature_var" is a variable referencing a [ThreadFeature](ThreadFeature.md) object.

```python
returnValue = threadFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version January 2015  

