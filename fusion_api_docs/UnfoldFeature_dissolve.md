# UnfoldFeature.dissolve Method

Parent Object: [UnfoldFeature](UnfoldFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"unfoldFeature_var" is a variable referencing a [UnfoldFeature](UnfoldFeature.md) object.

```python
returnValue = unfoldFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version August 2020  

