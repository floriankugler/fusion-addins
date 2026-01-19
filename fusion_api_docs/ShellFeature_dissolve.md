# ShellFeature.dissolve Method

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"shellFeature_var" is a variable referencing a [ShellFeature](ShellFeature.md) object.

```python
returnValue = shellFeature_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version November 2014  

