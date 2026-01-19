# IntegerProperty Object

Derived from: [Property](Property.md) Object  

## Description

An integer value property.

## Methods

| Name | Description |
| --- | --- |
| [classType](IntegerProperty_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getLimits](IntegerProperty_getLimits.md) | Method that returns any limits for the value of this property. The HasLimits property can be used to see if there are any limits or not. This is most commonly used for properties associated with materials and appearances. |

## Properties

| Name | Description |
| --- | --- |
| [hasLimits](IntegerProperty_hasLimits.md) | Gets the boolean flag that indicates if the value of this property has any limits it must be within to be valid. If True, use the GetLimits method to get the limit values. This is most commonly used for properties associated with materials and appearances. |
| [hasMultipleValues](IntegerProperty_hasMultipleValues.md) | Gets the boolean flag that indicates if this property has multiple values or not. This is most commonly used for properties associated with materials and appearances. |
| [id](IntegerProperty_id.md) | Returns the unique ID of this property. |
| [isReadOnly](IntegerProperty_isReadOnly.md) | Indicates if this property is read-only. If True any attempted edits will fail. |
| [isValid](IntegerProperty_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](IntegerProperty_name.md) | Returns the name of this property as seen in the user interface. This name is localized and can change based on the current language |
| [objectType](IntegerProperty_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](IntegerProperty_parent.md) | Returns the parent of this property.For properties associated with an appearance this will return the parent Appearance. For properties associated with a material, this will return the parent Material. For other types of properties, this will return the PropertyGroup it is in. |
| [value](IntegerProperty_value.md) | Gets and sets this property value. The value of this property should be ignored if the HasConnectedTexture property is true. Setting this will remove any associated texture, if there is one. |
| [values](IntegerProperty_values.md) | Gets and sets the values associated with this property. HasMultipleValues property indicates if this property will be returning more than one value. This is most commonly used for properties associated with materials and appearances. |

## Version

Introduced in version August 2014  

