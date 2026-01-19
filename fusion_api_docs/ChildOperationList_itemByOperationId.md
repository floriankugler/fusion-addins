# ChildOperationList.itemByOperationId Method

Parent Object: [ChildOperationList](ChildOperationList.md)  

## Description

Returns the operation, folder or pattern with the specified operation id.

## Syntax

"childOperationList_var" is a variable referencing a [ChildOperationList](ChildOperationList.md) object.

```python
returnValue = childOperationList_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md) | Returns the specified item or null in the case where there is no item with the specified operation id. |

## Parameters

| Name | Type    | Description                                 |
|------|---------|---------------------------------------------|
| id   | integer | The id of the operation, folder or pattern. |

## Version

Introduced in version May 2020  

