# SetupChangeEvent.add Method

Parent Object: [SetupChangeEvent](SetupChangeEvent.md)  

## Description

Add a handler to be notified when the file event occurs.

## Syntax

"setupChangeEvent_var" is a variable referencing a [SetupChangeEvent](SetupChangeEvent.md) object.

```python
returnValue = setupChangeEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SetupChangeEventHandler](SetupChangeEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version April 2023  

