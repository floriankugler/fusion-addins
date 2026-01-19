# StatusMessages.item Method

Parent Object: [StatusMessages](StatusMessages.md)  

## Description

Returns the specified status message using an index into the collection.

## Syntax

"statusMessages_var" is a variable referencing a [StatusMessages](StatusMessages.md) object.

```python
returnValue = statusMessages_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [StatusMessage](StatusMessage.md) | Returns the specified StatusMessage or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the status message within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version July 2021  

