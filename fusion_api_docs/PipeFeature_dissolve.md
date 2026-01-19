# PipeFeature.dissolve Method

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"pipeFeature_var" is a variable referencing a [PipeFeature](PipeFeature.md) object.

```python
returnValue = pipeFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version September 2015  

