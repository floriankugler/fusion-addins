# LinearMarkingMenu Object

Derived from: [Base](Base.md) Object  

## Description

Represents the linear marking menu which is the vertical menu that's displayed when the user right-clicks within Fusion. This supports customizing the contents of the context menu.

## Methods

| Name | Description |
|----|----|
| [classType](LinearMarkingMenu_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](LinearMarkingMenu_clear.md) | Completely clears the contents of the context menu. If left in this state, the context menu will not be displayed. |

## Properties

| Name | Description |
| --- | --- |
| [controls](LinearMarkingMenu_controls.md) | Return the collection of top-level controls in the context menu. It's possible to have drop-down controls (fly-outs) that provide access to additional controls. You can remove and add controls to customize the contents of the context menu. |
| [isValid](LinearMarkingMenu_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](LinearMarkingMenu_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[MarkingMenuEventArgs.linearMarkingMenu](MarkingMenuEventArgs_linearMarkingMenu.md)

## Version

Introduced in version January 2017  

