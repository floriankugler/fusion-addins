# DocumentReferences Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the list of documents referenced from a document.

## Methods

| Name | Description |
|----|----|
| [classType](DocumentReferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](DocumentReferences_item.md) | Returns the specified DocumentReference. |

## Properties

| Name | Description |
| --- | --- |
| [count](DocumentReferences_count.md) | The number of DocumentReference objects in this collection. |
| [isValid](DocumentReferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DocumentReferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Document.allDocumentReferences](Document_allDocumentReferences.md), [Document.documentReferences](Document_documentReferences.md), [DrawingDocument.allDocumentReferences](DrawingDocument_allDocumentReferences.md), [DrawingDocument.documentReferences](DrawingDocument_documentReferences.md), [FusionDocument.allDocumentReferences](FusionDocument_allDocumentReferences.md), [FusionDocument.documentReferences](FusionDocument_documentReferences.md)

## Version

Introduced in version June 2017  

