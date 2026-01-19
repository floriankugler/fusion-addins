# CAMPatterns.itemByName Method

Parent Object: [CAMPatterns](CAMPatterns.md)  

## Description

Returns the pattern with the specified name (as appears in the browser).

## Syntax

"cAMPatterns_var" is a variable referencing a [CAMPatterns](CAMPatterns.md) object.

```python
returnValue = cAMPatterns_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CAMPattern](CAMPattern.md) | Returns the specified pattern or null in the case where there is no pattern with the specified name. |

## Parameters

| Name | Type   | Description                                             |
|------|--------|---------------------------------------------------------|
| name | string | The name (as it appears in the browser) of the pattern. |

## Version

Introduced in version January 2016  

