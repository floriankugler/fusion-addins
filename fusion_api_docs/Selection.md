# Selection Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a selection of an entity in the user interface.

## Methods

| Name | Description |
|----|----|
| [classType](Selection_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [entity](Selection_entity.md) | Gets the selected entity. |
| [isValid](Selection_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Selection_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [point](Selection_point.md) | Gets the selection point on the object. |

## Accessed From

[ActiveSelectionEventArgs.currentSelection](ActiveSelectionEventArgs_currentSelection.md), [SelectionCommandInput.selection](SelectionCommandInput_selection.md), [SelectionEventArgs.selection](SelectionEventArgs_selection.md), [Selections.asArray](Selections_asArray.md), [Selections.item](Selections_item.md), [UserInterface.selectEntity](UserInterface_selectEntity.md)

## Version

Introduced in version August 2014  

