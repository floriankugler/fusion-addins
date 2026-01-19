# Application.unregisterCustomEvent Method

Parent Object: [Application](Application.md)  

## Description

Unregisters an existing CustomEvent.

## Syntax

"application_var" is a variable referencing an [Application](Application.md) object.

```python
returnValue = application_var.unregisterCustomEvent(eventId)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns True if the unregister succeeded. |

## Parameters

| Name    | Type   | Description                                              |
|---------|--------|----------------------------------------------------------|
| eventId | string | Th unique ID of the custom event you want to unregister. |

## Samples

| Name | Description |
|----|----|
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |
| [Custom Event Sample](CustomEventSample_Sample.md) | Demonstrates the ability to call into the main thread from a worker thread. This sample is an **add-in**. To use it, use the **Scripts and Add-Ins** command to create a new add-in. Delete all of the code in the newly created add-in and replace it with the code below. Have a model open that has a parameter named "Length". Load the add-in. The add-in will change the value of the parameter every two seconds using a random value between 1 and 10. |

## Version

Introduced in version January 2017  

