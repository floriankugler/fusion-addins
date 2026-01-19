# NavigationEvent.add Method

Parent Object: [NavigationEvent](NavigationEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"navigationEvent_var" is a variable referencing a [NavigationEvent](NavigationEvent.md) object.

```python
returnValue = navigationEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [NavigationEventHandler](NavigationEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version March 2021  

