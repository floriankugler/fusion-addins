# DataProjects Object

Derived from: [Base](Base.md) Object  

## Description

Collection object that provides a list of all available projects.

## Methods

| Name | Description |
|----|----|
| [add](DataProjects_add.md) | Creates a new project in the parent hub. |
| [asArray](DataProjects_asArray.md) | Get the current list of all projects. |
| [classType](DataProjects_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DataProjects_item.md) | Returns the specified project. |
| [itemById](DataProjects_itemById.md) | Returns the project specified using the ID of the project. |

## Properties

| Name | Description |
| --- | --- |
| [count](DataProjects_count.md) | The number of projects in this collection. |
| [isValid](DataProjects_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataProjects_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Data.dataProjects](Data_dataProjects.md), [DataHub.dataProjects](DataHub_dataProjects.md)

## Version

Introduced in version January 2015  

