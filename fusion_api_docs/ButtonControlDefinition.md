# ButtonControlDefinition Object

Derived from: [ControlDefinition](ControlDefinition.md) Object  

## Description

Represents the information used to define a button. This isn't the visible button control but is the information needed to create a button control and fully defines a button except for it's position within the user interface.

## Methods

| Name | Description |
|----|----|
| [classType](ButtonControlDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isEnabled](ButtonControlDefinition_isEnabled.md) | Gets or sets if this definition is enabled or not. This has the effect of enabling and disabling any associated controls. |
| [isValid](ButtonControlDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ButtonControlDefinition_isVisible.md) | Gets or sets if this definition is visible or not. This has the effect of making any associated controls visible or invisible in the user interface. |
| [name](ButtonControlDefinition_name.md) | Gets or sets the name for this control. This is the visible name displayed in the user interface. |
| [objectType](ButtonControlDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

