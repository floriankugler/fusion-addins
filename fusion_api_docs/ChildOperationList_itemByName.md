# ChildOperationList.itemByName Method

Parent Object: [ChildOperationList](ChildOperationList.md)  

## Description

Returns the operation, folder or pattern with the specified name (the name seen in the browser).

## Syntax

"childOperationList_var" is a variable referencing a [ChildOperationList](ChildOperationList.md) object.

```python
returnValue = childOperationList_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md) | Returns the specified item or null in the case where there is no item with the specified name. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the operation, folder or pattern as seen in the browser. |

## Version

Introduced in version January 2016  

