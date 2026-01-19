# Toolbar Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a toolbar in the user interface. A toolbar is a collection of toolbar controls.

## Methods

| Name | Description |
|----|----|
| [classType](Toolbar_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [controls](Toolbar_controls.md) | Gets the controls in this toolbar. |
| [id](Toolbar_id.md) | Gets the unique ID of the toolbar that can be used programmatically to find a specific toolbar. |
| [isValid](Toolbar_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Toolbar_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentUserInterface](Toolbar_parentUserInterface.md) | Gets the owning UserInterface object. |

## Accessed From

[Toolbars.item](Toolbars_item.md), [Toolbars.itemById](Toolbars_itemById.md), [UserInterface.activeToolbar](UserInterface_activeToolbar.md)

## Version

Introduced in version August 2014  

