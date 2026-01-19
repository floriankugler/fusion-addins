# CAMParameters.item Method

Parent Object: [CAMParameters](CAMParameters.md)  

## Description

Function that returns the specified parameter using an index into the collection.

## Syntax

"cAMParameters_var" is a variable referencing a [CAMParameters](CAMParameters.md) object.

```python
returnValue = cAMParameters_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CAMParameter](CAMParameter.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2020  

