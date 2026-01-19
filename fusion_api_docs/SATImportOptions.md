# SATImportOptions Object

Derived from: [ImportOptions](ImportOptions.md) Object  

## Description

Defines that a SAT import is to be done and specifies the various options.

## Methods

| Name | Description |
|----|----|
| [classType](SATImportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [filename](SATImportOptions_filename.md) | Gets and sets the filename or URL of the file to be imported. |
| [isValid](SATImportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isViewFit](SATImportOptions_isViewFit.md) | Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry. |
| [objectType](SATImportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ImportManager.createSATImportOptions](ImportManager_createSATImportOptions.md)

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

