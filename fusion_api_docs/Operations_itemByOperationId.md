# Operations.itemByOperationId Method

Parent Object: [Operations](Operations.md)  

## Description

Returns the operation with the specified operation id.

## Syntax

"operations_var" is a variable referencing an [Operations](Operations.md) object.

```python
returnValue = operations_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [Operation](Operation.md) | Returns the specified operation or null in the case where there is no operation with the specified operation id. |

## Parameters

| Name | Type    | Description              |
|------|---------|--------------------------|
| id   | integer | The id of the operation. |

## Version

Introduced in version May 2020  

