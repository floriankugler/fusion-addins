# SetupChangeEvent.remove Method

Parent Object: [SetupChangeEvent](SetupChangeEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"setupChangeEvent_var" is a variable referencing a [SetupChangeEvent](SetupChangeEvent.md) object.

```python
returnValue = setupChangeEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SetupChangeEventHandler](SetupChangeEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version April 2023  

