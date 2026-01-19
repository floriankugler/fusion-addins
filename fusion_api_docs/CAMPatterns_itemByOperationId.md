# CAMPatterns.itemByOperationId Method

Parent Object: [CAMPatterns](CAMPatterns.md)  

## Description

Returns the pattern with the specified operation id.

## Syntax

"cAMPatterns_var" is a variable referencing a [CAMPatterns](CAMPatterns.md) object.

```python
returnValue = cAMPatterns_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [CAMPattern](CAMPattern.md) | Returns the specified pattern or null in the case where there is no pattern with the specified operation id. |

## Parameters

| Name | Type    | Description            |
|------|---------|------------------------|
| id   | integer | The id of the pattern. |

## Version

Introduced in version May 2020  

