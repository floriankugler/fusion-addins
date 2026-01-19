# DrawingExportOptions Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the different drawing export types. This class is never directly used in an export because you need the specific export type to specify the type of export to be performed.

## Methods

| Name | Description |
|----|----|
| [classType](DrawingExportOptions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [filename](DrawingExportOptions_filename.md) | Gets and sets the filename that the exported file will be written to. |
| [isValid](DrawingExportOptions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DrawingExportOptions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Derived Classes

[PDFExportOptions](PDFExportOptions.md)

## Version

Introduced in version December 2020  

