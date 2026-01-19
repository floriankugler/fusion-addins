# Documents Object

Derived from: [Base](Base.md) Object  

## Description

The Documents object provides access to all of the currently open documents and provides methods to create and open documents.

## Methods

| Name | Description |
|----|----|
| [add](Documents_add.md) | Creates and opens a new document of the specified type. |
| [classType](Documents_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Documents_item.md) | Function that returns the specified document using an index into the collection. |
| [open](Documents_open.md) | Opens an item that has previously been saved. |

## Properties

| Name | Description |
| --- | --- |
| [count](Documents_count.md) | Returns the number of currently open documents. This includes documents that are visible and invisible. |
| [isValid](Documents_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Documents_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Application.documents](Application_documents.md)

## Samples

| Name | Description |
|----|----|
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

