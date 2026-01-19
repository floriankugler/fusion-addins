# Operations.itemByName Method

Parent Object: [Operations](Operations.md)  

## Description

Returns the operation with the specified name (as appears in the browser).

## Syntax

"operations_var" is a variable referencing an [Operations](Operations.md) object.

```python
returnValue = operations_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Operation](Operation.md) | Returns the specified operation or null in the case where there is no operation with the specified name. |

## Parameters

| Name | Type   | Description                                               |
|------|--------|-----------------------------------------------------------|
| name | string | The name (as it appears in the browser) of the operation. |

## Version

Introduced in version January 2016  

