# UserParameters.item Method

Parent Object: [UserParameters](UserParameters.md)  

## Description

Function that returns the specified User Parameter using an index into the collection.

## Syntax

"userParameters_var" is a variable referencing a [UserParameters](UserParameters.md) object.

```python
returnValue = userParameters_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [UserParameter](UserParameter.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

