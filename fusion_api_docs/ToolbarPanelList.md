# ToolbarPanelList Object

Derived from: [Base](Base.md) Object  

## Description

A ToolbarPanelList is a list of ToolbarPanel objects.

## Methods

| Name | Description |
|----|----|
| [classType](ToolbarPanelList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ToolbarPanelList_item.md) | Returns the specified work space using an index into the collection. |
| [itemById](ToolbarPanelList_itemById.md) | Returns the ToolbarPanel of the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](ToolbarPanelList_count.md) | Gets the number of toolbar panels in the collection. |
| [isValid](ToolbarPanelList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToolbarPanelList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[UserInterface.allToolbarPanels](UserInterface_allToolbarPanels.md), [UserInterface.toolbarPanelsByProductType](UserInterface_toolbarPanelsByProductType.md)

## Version

Introduced in version June 2015  

