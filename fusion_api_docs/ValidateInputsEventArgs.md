# ValidateInputsEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing ValidateInputsEvent to a ValidateInputsEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](ValidateInputsEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [areInputsValid](ValidateInputsEventArgs_areInputsValid.md) | Used with AreInputsValid event to specify if the all of the inputs for the command are valid or not. If you set this to false, indicating they are not valid, the OK button for the dialog is disabled forcing the user to correct the inputs before continuing. If you set this to true the OK button will be enabled, as long as the inputs satisfy their own requirements. For example, if a SelectionCommandInput is defined to have at minimum number of entities selected, that requirement must be met, or if a ValueCommandInput has an invalid value specified, the OK button will still be disabled. |
| [firingEvent](ValidateInputsEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [inputs](ValidateInputsEventArgs_inputs.md) | Returns the collection of command inputs that are associated with the command this event is being fired for. |
| [isValid](ValidateInputsEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ValidateInputsEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

