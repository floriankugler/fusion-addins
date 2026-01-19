# ToolbarControlList Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a list of toolbar controls.

## Methods

| Name | Description |
|----|----|
| [classType](ToolbarControlList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ToolbarControlList_item.md) | Returns the ToolbarControl at the specified index. When iterating by index, the controls are returned in the same order as they are shown in the user interface. |
| [itemById](ToolbarControlList_itemById.md) | Returns the ToolbarControl at the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](ToolbarControlList_count.md) | Gets the number of toolbar controls. |
| [isValid](ToolbarControlList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToolbarControlList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ToolbarPanel.promotedControls](ToolbarPanel_promotedControls.md)

## Version

Introduced in version August 2014  

