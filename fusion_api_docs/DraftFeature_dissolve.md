# DraftFeature.dissolve Method

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"draftFeature_var" is a variable referencing a [DraftFeature](DraftFeature.md) object.

```python
returnValue = draftFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version January 2015  

