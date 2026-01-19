# DocumentReference Object

Derived from: [Base](Base.md) Object  

## Description

Represents a reference to a document from another document.

## Methods

| Name | Description |
|----|----|
| [classType](DocumentReference_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getLatestVersion](DocumentReference_getLatestVersion.md) | Updates the reference to use the latest version. This is only useful when the isOutOfDate property is true. |

## Properties

| Name | Description |
| --- | --- |
| [dataFile](DocumentReference_dataFile.md) | The dataFile on A360 that this object references. |
| [isOutOfDate](DocumentReference_isOutOfDate.md) | Indicates if this reference is out of date, meaning that the reference is not referencing the latest version. |
| [isValid](DocumentReference_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DocumentReference_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentDocument](DocumentReference_parentDocument.md) | The document that is doing the referencing and owns this reference. |
| [referencedDocument](DocumentReference_referencedDocument.md) | The document currently open in Fusion that this object references. |
| [version](DocumentReference_version.md) | Gets and sets the version of the dataFile on A360 that this document currently represents. Setting this property will cause all occurrences referencing this document to update to that version. |

## Accessed From

[DeriveFeature.documentReference](DeriveFeature_documentReference.md), [DocumentReferences.item](DocumentReferences_item.md), [Occurrence.documentReference](Occurrence_documentReference.md)

## Version

Introduced in version June 2017  

