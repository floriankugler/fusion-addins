# ListControlDefinition Object

Derived from: [ControlDefinition](ControlDefinition.md) Object  

## Description

Represents the information used to define a list of check boxes, radio buttons, or text with icons. This class isn't the visible list control but is the information needed to create a list control and fully defines a list except for it's position within the user interface.

## Methods

| Name | Description |
|----|----|
| [classType](ListControlDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isEnabled](ListControlDefinition_isEnabled.md) | Gets or sets if this definition is enabled or not. This has the effect of enabling and disabling any associated controls. |
| [isValid](ListControlDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ListControlDefinition_isVisible.md) | Gets or sets if this definition is visible or not. This has the effect of making any associated controls visible or invisible in the user interface. |
| [lastSelected](ListControlDefinition_lastSelected.md) | Gets the item in the list that was last selected. This can return null in the case where this control is displayed as a list of check boxes and there hasn't been any interaction by the end-user. In the case of a list of check boxes, this returns the item that was last clicked by the user, whether it was to check or uncheck the item. In the case of a list of radio buttons, this always returns the item that is currently selected. |
| [listControlDisplayType](ListControlDefinition_listControlDisplayType.md) | Gets how this list control will be displayed; as a standard list, a list of check boxes, or a list of radio buttons. |
| [listItems](ListControlDefinition_listItems.md) | Gets the associated ListControlItems collection through which you can add and modify items in the list. |
| [name](ListControlDefinition_name.md) | Gets or sets the name for this control. This is the visible name displayed in the user interface. |
| [objectType](ListControlDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

