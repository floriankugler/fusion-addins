# Application.fireCustomEvent Method

Parent Object: [Application](Application.md)  

## Description

Fires a previously registered custom event. This method is used by a worker thread or another add-in to fire an event to the add-in that registered the event and is running in the primary thread.  

Firing a custom event does not immediately result in the event handler being called. When a custom event is fired the event is put on the queue and will be handled in the main thread when Fusion is idle.

## Syntax

"application_var" is a variable referencing an [Application](Application.md) object.

```python
# Uses no optional arguments.
returnValue = application_var.fireCustomEvent(eventId)

# Uses optional arguments.
returnValue = application_var.fireCustomEvent(eventId, additionalInfo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the event was successfully added to the event queue. A value of true does not indicate that the event was fired and handled but only that it's been put on the primary thread's event queue to be fired when application is idle. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| eventId | string | The ID of the custom event you want to fire. |
| additionalInfo | string | Any additional information you want to pass through the event to the add-in in the primary thread. This is an optional argument whose default value is "". |

## Samples

| Name | Description |
| --- | --- |
| [Custom Event for Command Dialog](CustomEventCommandDialog_Sample.md) | Demonstrates using a custom event to process getting information in the background to display in a command dialog. This is an add-in and should be copied and pasted into an add-in project. |
| [Custom Event Sample](CustomEventSample_Sample.md) | Demonstrates the ability to call into the main thread from a worker thread. This sample is an add-in. To use it, use the Scripts and Add-Ins command to create a new add-in. Delete all of the code in the newly created add-in and replace it with the code below. Have a model open that has a parameter named "Length". Load the add-in. The add-in will change the value of the parameter every two seconds using a random value between 1 and 10. |
| [Rendering Sample](RenderSample_Sample.md) | Demonstrates using the Rendering capabilities in the API. This starts a series of local renderings to generate a series of frames, where the camera is repositioned and a parameter is modified for each frame to create a dynamic animation. To use the sample, have a design open that contains a parameter named "Length". It can be a user or model parameter. The sample will modify this parameter from a value of 0.1 cm to 15 cm, but you can change these values by editing the values of the paramStartVal and paramEndVal variables on lines 90 and 91 of the sample. It expects a folder named "C:\Temp\RenderSample" to exist, and will fail if it doesn't. The rendered frames will be written to that folder. An example rendering is shown below where [this file](../ExtraFiles/RenderSample.f3d) was used. The parameter is modifying a move feature which results in changing the shape of an extrusion. The parameter could be driving anything and you could modify the code to edit more than one parameter. The result of this sample is a folder containing all of the rendered frames. You can process these to create an animation. The sample animation was created using GIMP. |

## Version

Introduced in version January 2017  

