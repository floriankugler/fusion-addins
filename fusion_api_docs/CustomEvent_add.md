# CustomEvent.add Method

Parent Object: [CustomEvent](CustomEvent.md)  

## Description

Add a handler to be notified when the event occurs.

## Syntax

"customEvent_var" is a variable referencing a [CustomEvent](CustomEvent.md) object.

```python
returnValue = customEvent_var.add(handler)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the addition of the handler was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| handler | [CustomEventHandler](CustomEventHandler.md) | The handler object to be called when this event is fired. |

## Samples

| Name | Description |
|----|----|
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |
| [Custom Event Sample](CustomEventSample_Sample.md) | Demonstrates the ability to call into the main thread from a worker thread. This sample is an **add-in**. To use it, use the **Scripts and Add-Ins** command to create a new add-in. Delete all of the code in the newly created add-in and replace it with the code below. Have a model open that has a parameter named "Length". Load the add-in. The add-in will change the value of the parameter every two seconds using a random value between 1 and 10. |

## Version

Introduced in version January 2017  

