# SetupEvent.add Method

Parent Object: [SetupEvent](SetupEvent.md)  

## Description

Add a handler to be notified when the file event occurs.

## Syntax

"setupEvent_var" is a variable referencing a [SetupEvent](SetupEvent.md) object.

```python
returnValue = setupEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SetupEventHandler](SetupEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version April 2023  

