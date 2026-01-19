# MachineQuery Object

Derived from: [Base](Base.md) Object  

## Description

MachineQuery defines the query to access Machines.

## Methods

| Name | Description |
|----|----|
| [classType](MachineQuery_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [execute](MachineQuery_execute.md) | Executes the query for specific machines based on the query's properties. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MachineQuery_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [location](MachineQuery_location.md) | The location specifies the location to search in the machine library. Setting the location clears any previous specified URL. |
| [model](MachineQuery_model.md) | The case-insensitive model specifies the model of the machine. The default empty model applies to all machines. |
| [objectType](MachineQuery_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [url](MachineQuery_url.md) | The URL specifies the location and folder to search for in the machine library. Setting the URL updates the location. |
| [vendor](MachineQuery_vendor.md) | The case-insensitive vendor specifies the vendor of the machine. The default empty vendor applies to all machines. |

## Accessed From

[MachineLibrary.createQuery](MachineLibrary_createQuery.md)

## Version

Introduced in version April 2023  

