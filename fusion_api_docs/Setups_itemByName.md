# Setups.itemByName Method

Parent Object: [Setups](Setups.md)  

## Description

Returns the setup with the specified name.

## Syntax

"setups_var" is a variable referencing a [Setups](Setups.md) object.

```python
returnValue = setups_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Setup](Setup.md) | Returns the specified setup or null in the case where there is no setup with the specified name. |

## Parameters

| Name | Type   | Description                                               |
|------|--------|-----------------------------------------------------------|
| name | string | The name (as it appears in the browser) of the operation. |

## Version

Introduced in version January 2016  

