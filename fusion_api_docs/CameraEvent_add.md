# CameraEvent.add Method

Parent Object: [CameraEvent](CameraEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"cameraEvent_var" is a variable referencing a [CameraEvent](CameraEvent.md) object.

```python
returnValue = cameraEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CameraEventHandler](CameraEventHandler.md) | The handler object to be called when this event is fired. |

## Version

Introduced in version December 2017  

