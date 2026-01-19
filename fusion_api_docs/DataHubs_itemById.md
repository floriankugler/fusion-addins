# DataHubs.itemById Method

Parent Object: [DataHubs](DataHubs.md)  

## Description

Returns the hub specified using the ID of the hub.

## Syntax

"dataHubs_var" is a variable referencing a [DataHubs](DataHubs.md) object.

```python
returnValue = dataHubs_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataHub](DataHub.md) | Returns the hub or null if a hub with the specified ID is not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the hub to return. This is the same ID used by the APS Data Management API. |

## Version

Introduced in version December 2020  

