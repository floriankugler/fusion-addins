# ChoiceProperty Object

Derived from: [Property](Property.md) Object  

## Description

A property that is a predefined list of choices.  

This is most commonly used for properties associated with materials and appearances.

## Methods

| Name | Description |
|----|----|
| [classType](ChoiceProperty_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getChoices](ChoiceProperty_getChoices.md) | Method that returns the list of available choices. |

## Properties

| Name | Description |
| --- | --- |
| [id](ChoiceProperty_id.md) | Returns the unique ID of this property. |
| [isReadOnly](ChoiceProperty_isReadOnly.md) | Indicates if this property is read-only. If True any attempted edits will fail. |
| [isValid](ChoiceProperty_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ChoiceProperty_name.md) | Returns the name of this property as seen in the user interface. This name is localized and can change based on the current language |
| [objectType](ChoiceProperty_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](ChoiceProperty_parent.md) | Returns the parent of this property.For properties associated with an appearance this will return the parent Appearance. For properties associated with a material, this will return the parent Material. For other types of properties, this will return the PropertyGroup it is in. |
| [value](ChoiceProperty_value.md) | Gets and sets the which choice is selected from the set of choices. The value is a string that matches one of the predefined choices. The names of the available choices can be obtained using GetChoices method. |

## Version

Introduced in version August 2014  

