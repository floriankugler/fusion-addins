# Selections Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to and control over the set of selected entities in the user interface.

## Methods

| Name | Description |
|----|----|
| [add](Selections_add.md) | Adds the entity to the set of currently selected entities. The user will see the entity become selected in the user interface. |
| [asArray](Selections_asArray.md) | Returns an array containing all of the current selections. This is useful in cases where you need to iterate over the set of selected entities but need to create or edit data as you process each one. Selections are fragile and creation and edit operations will clear the selections so you won't have access to the complete list after processing the first one. |
| [classType](Selections_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clear](Selections_clear.md) | Clears the selection set so no entities are currently selected. |
| [item](Selections_item.md) | Returns the specified selection using an index into the collection. |
| [removeByEntity](Selections_removeByEntity.md) | Removes the selections that are associated with the specified entity from the set of selected entities. |
| [removeByIndex](Selections_removeByIndex.md) | Removes an item from the set of selected entities. |
| [removeBySelection](Selections_removeBySelection.md) | Removes the specified selection from the set of selected entities. |

## Properties

| Name | Description |
| --- | --- |
| [all](Selections_all.md) | Gets or sets all entities currently selected. |
| [count](Selections_count.md) | Gets the number of entities currently selected. |
| [isValid](Selections_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Selections_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[UserInterface.activeSelections](UserInterface_activeSelections.md)

## Version

Introduced in version August 2014  

