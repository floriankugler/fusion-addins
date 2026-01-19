# ModelParameters.item Method

Parent Object: [ModelParameters](ModelParameters.md)  

## Description

Function that returns the specified Model Parameter using an index into the collection.

## Syntax

"modelParameters_var" is a variable referencing a [ModelParameters](ModelParameters.md) object.

```python
returnValue = modelParameters_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ModelParameter](ModelParameter.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

