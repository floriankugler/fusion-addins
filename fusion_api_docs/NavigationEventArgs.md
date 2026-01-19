# NavigationEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The NavigationEventArgs provides access to the information sent from the browser within a palette on a navigation event.

## Methods

| Name | Description |
|----|----|
| [classType](NavigationEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [browserCommandInput](NavigationEventArgs_browserCommandInput.md) | When the event is fired from a BrowserCommandInput object, this property returns the specific BrowserCommandInput that caused the event to fire. In all other cases this property returns null. |
| [firingEvent](NavigationEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](NavigationEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [launchExternally](NavigationEventArgs_launchExternally.md) | If True, the URL will be navigated to in an external browser by the operating system. If False, the default value, the URL will be navigated to in the palette's browser. |
| [navigationURL](NavigationEventArgs_navigationURL.md) | The URL that is being navigated to. |
| [objectType](NavigationEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [preventDefault](NavigationEventArgs_preventDefault.md) | If True, the default handling of this navigation event will not continue. If False, the default value, the default handling of this navigation event will continue. |

## Version

Introduced in version March 2021  

