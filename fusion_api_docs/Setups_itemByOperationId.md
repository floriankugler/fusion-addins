# Setups.itemByOperationId Method

Parent Object: [Setups](Setups.md)  

## Description

Returns the setup with the specified operation id.

## Syntax

"setups_var" is a variable referencing a [Setups](Setups.md) object.

```python
returnValue = setups_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [Setup](Setup.md) | Returns the specified setup or null in the case where there is no setup with the specified operation id. |

## Parameters

| Name | Type    | Description              |
|------|---------|--------------------------|
| id   | integer | The id of the operation. |

## Version

Introduced in version May 2020  

