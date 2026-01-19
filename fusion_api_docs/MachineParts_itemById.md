# MachineParts.itemById Method

Parent Object: [MachineParts](MachineParts.md)  

## Description

Get the part with the given ID.

## Syntax

"machineParts_var" is a variable referencing a [MachineParts](MachineParts.md) object.

```python
returnValue = machineParts_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [MachinePart](MachinePart.md) | Returns the MachinePart with the given ID, or null if the given ID does not match any part in the collection. |

## Parameters

| Name | Type   | Description                 |
|------|--------|-----------------------------|
| id   | string | The ID for the part to get. |

## Version

Introduced in version April 2023  

