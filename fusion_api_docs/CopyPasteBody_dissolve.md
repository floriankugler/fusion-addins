# CopyPasteBody.dissolve Method

Parent Object: [CopyPasteBody](CopyPasteBody.md)  

## Description

Dissolves the feature so that the feature information is lost and only the B-Rep geometry defined by the feature remains. This is only valid for non-parametric features.

## Syntax

"copyPasteBody_var" is a variable referencing a [CopyPasteBody](CopyPasteBody.md) object.

```python
returnValue = copyPasteBody_var.dissolve()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns a bool indicating if the dissolve was successful or not. |

## Version

Introduced in version June 2017  

