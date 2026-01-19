# ParameterList.item Method

Parent Object: [ParameterList](ParameterList.md)  

## Description

Function that returns the specified parameter using an index into the collection.

## Syntax

"parameterList_var" is a variable referencing a [ParameterList](ParameterList.md) object.

```python
returnValue = parameterList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Parameter](Parameter.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

