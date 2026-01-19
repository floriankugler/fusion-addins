# DataHub Object

Derived from: [Base](Base.md) Object  

## Description

Represents a hub within the data.

## Methods

| Name | Description |
|----|----|
| [classType](DataHub_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [dataProjects](DataHub_dataProjects.md) | Returns the projects within this hub. |
| [fusionWebURL](DataHub_fusionWebURL.md) | Returns a URL that can be used to access the Fusion Web interface for this hub within a browser. The person using the URL must have an Autodesk account and have authority to access the hub. |
| [hubType](DataHub_hubType.md) | Gets if this hub is a Personal (PersonalHubType) or Team (TeamHubType) type hub. |
| [id](DataHub_id.md) | Returns the unique ID for this hub. This is the same id used in the APS Data Management API in an unencoded form and will look something like this: "a.45637". |
| [isCollaborativeEditingEnabled](DataHub_isCollaborativeEditingEnabled.md) | Returns true if Concurrent Editing is enabled. |
| [isValid](DataHub_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [mfgdmId](DataHub_mfgdmId.md) | Get the MFGDM ID for this hub. |
| [name](DataHub_name.md) | Returns the name of the hub. |
| [objectType](DataHub_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [version](DataHub_version.md) | Returns the version of the hub. |

## Accessed From

[Data.activeHub](Data_activeHub.md), [DataHubs.asArray](DataHubs_asArray.md), [DataHubs.item](DataHubs_item.md), [DataHubs.itemById](DataHubs_itemById.md), [DataProject.parentHub](DataProject_parentHub.md)

## Version

Introduced in version September 2016  

