# PrintSettingQuery Object

Derived from: [Base](Base.md) Object  

## Description

A PrintSettingQuery can be used to search a LibraryLocation for a set of PrintSetting objects matching the required properties.

## Methods

| Name | Description |
|----|----|
| [classType](PrintSettingQuery_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [execute](PrintSettingQuery_execute.md) | Query for specific PrintSettings. This PrintSettingQuery query. |

## Properties

| Name | Description |
| --- | --- |
| [filamentDiameter](PrintSettingQuery_filamentDiameter.md) | **RETIRED** The filament diameter specifies filament diameter for FFF Printer. This should match the FFF PrintSetting filament diameter in cm. |
| [isValid](PrintSettingQuery_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [layerHeight](PrintSettingQuery_layerHeight.md) | The layer height specifies layer height of the PrintSetting. This should match the PrintSetting layer height in cm. |
| [location](PrintSettingQuery_location.md) | The location specifies the location to search in the PrintSetting library. Setting the location clears any previous specified URL. |
| [machine](PrintSettingQuery_machine.md) | The machine specifies which machine the found print setting are compatible with. |
| [material](PrintSettingQuery_material.md) | The case-insensitive material specifies material of the MPBF PrintSetting. |
| [name](PrintSettingQuery_name.md) | The case-insensitive name specifies the name of the PrintSetting. |
| [objectType](PrintSettingQuery_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [technology](PrintSettingQuery_technology.md) | The case-insensitive technology specifies technology of the PrintSetting. |
| [url](PrintSettingQuery_url.md) | The URL specifies the location and folder to search for in the PrintSetting library. Setting the URL updates the location. |
| [vendor](PrintSettingQuery_vendor.md) | The case-insensitive vendor specifies vendor of the PrintSetting. Generic FFF PrintSetting doesnt have a vendor. |

## Accessed From

[PrintSettingLibrary.createQuery](PrintSettingLibrary_createQuery.md)

## Version

Introduced in version April 2023  

