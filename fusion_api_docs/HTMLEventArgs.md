# HTMLEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The HTMLEventArgs provides access to the information sent from the JavaScript that's associated with HTML being displayed within a palette.

## Methods

| Name | Description |
|----|----|
| [classType](HTMLEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [action](HTMLEventArgs_action.md) | The action string sent from the JavaScript associated with HTML displayed in the palette. The string can represent any type of data in any format but JSON is commonly used to pass more complex data. |
| [browserCommandInput](HTMLEventArgs_browserCommandInput.md) | When the event is fired from a BrowserCommandInput object, this property returns the specific BrowserCommandInput that caused the event to fire. In all other cases this property returns null. |
| [data](HTMLEventArgs_data.md) | The data string sent from the JavaScript associated with HTML displayed in the palette. The string can represent any type of data in any format but JSON is commonly used to pass more complex data. |
| [firingEvent](HTMLEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](HTMLEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](HTMLEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [returnData](HTMLEventArgs_returnData.md) | Set this property to return data back to the JavaScript that's associated with the HTML. |

## Version

Introduced in version March 2017  

