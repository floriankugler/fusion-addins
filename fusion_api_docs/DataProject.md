# DataProject Object

Derived from: [Base](Base.md) Object  

## Description

Represents the master branch project within a hub.

## Methods

| Name | Description |
|----|----|
| [classType](DataProject_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [id](DataProject_id.md) | Returns the unique ID for this project. This is the same id used in the APS Data Management API in an unencoded form and will look something like this: "a.45637". |
| [isValid](DataProject_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](DataProject_name.md) | Gets and sets the name of the project. |
| [objectType](DataProject_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentHub](DataProject_parentHub.md) | Returns the parent DataHub of this project. |
| [rootFolder](DataProject_rootFolder.md) | Returns the project's root folder. This provides access to all of the folders and the files in the top level of the project. |

## Accessed From

[Data.activeProject](Data_activeProject.md), [DataFile.parentProject](DataFile_parentProject.md), [DataFolder.parentProject](DataFolder_parentProject.md), [DataProjects.add](DataProjects_add.md), [DataProjects.asArray](DataProjects_asArray.md), [DataProjects.item](DataProjects_item.md), [DataProjects.itemById](DataProjects_itemById.md), [DesignDataFile.parentProject](DesignDataFile_parentProject.htm)

## Version

Introduced in version January 2015  

