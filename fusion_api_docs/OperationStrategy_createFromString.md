# OperationStrategy.createFromString Method

Parent Object: [OperationStrategy](OperationStrategy.md)  

## Description

Create an OperationStrategy for a given name.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.OperationStrategy.createFromString(name)
```

## Return Value

| Type | Description |
|----|----|
| [OperationStrategy](OperationStrategy.md) | Returns the OperationStrategy for given strategy name. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the strategy. Throws an error if the strategy name is unknown. |

## Version

Introduced in version April 2023  

