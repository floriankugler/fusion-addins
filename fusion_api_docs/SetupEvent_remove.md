# SetupEvent.remove Method

Parent Object: [SetupEvent](SetupEvent.md)  

## Description

Removes a handler from the event.

## Syntax

"setupEvent_var" is a variable referencing a [SetupEvent](SetupEvent.md) object.

```python
returnValue = setupEvent_var.remove(handler)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true if removal of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [SetupEventHandler](SetupEventHandler.md) | The handler object to be removed from the event. |

## Version

Introduced in version April 2023  

