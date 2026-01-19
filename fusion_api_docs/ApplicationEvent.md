# ApplicationEvent Object

Derived from: [Event](Event.md) Object  

## Description

An ApplicationEvent represents a Fusion application related event. For example, startupCompleted or OnlineStatusChanged

## Methods

| Name | Description |
|----|----|
| [add](ApplicationEvent_add.md) | Add a handler to be notified when the event occurs. |
| [classType](ApplicationEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](ApplicationEvent_remove.md) | Removes a handler from the event. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ApplicationEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ApplicationEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](ApplicationEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](ApplicationEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Application.onlineStatusChanged](Application_onlineStatusChanged.md), [Application.startupCompleted](Application_startupCompleted.md)

## Samples

| Name | Description |
|----|----|
| [Application Event API Sample](ApplicationEventSample_Sample.md) | Add-In that demonstrates application events. To use this sample, create a new folder using the name you want to use for the new add-in. Inside the folder, create a new file that is the same name as the folder but has a .py extension. Copy the code below into the .py file. Create another file that is the same name as the folder but has a .manifest extension and copy the JSON data below into that file. { "autodeskProduct": "Fusion360", "type": "addin", "author": "", "description": { "": "" }, "supportedOS": "windows\|mac", "editEnabled": true } Run the "Scripts and Add-Ins" command and click the green plus button near the top of the dialog. Browse to the location where you created the folder and select the folder. The add-in should now be displayed in the list of add-ins on the "Add-Ins" tab of the dialog. Select the add-in and click the "Run" button. This will load the add-in and when any of the application events occurr that it is watching for it will report them in the TEXT COMMAND window. |

## Version

Introduced in version January 2016  

