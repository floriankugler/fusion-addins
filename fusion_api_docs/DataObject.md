# DataObject Object

Derived from: [Base](Base.md) Object  

## Description

The DataObject provides access to the raw data that represents a logical entity. Typically, it is the bytes of a stored file, but it can also be something like the image data that could be stored within another file.

## Methods

| Name | Description |
|----|----|
| [asString](DataObject_asString.md) | Gets the file as a string (UTF-8). This is convenient when the saved file contains string data. For example, if the file contains JSON data. This eliminates the need to convert the Base64 string into a standard string. |
| [classType](DataObject_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getAsBase64String](DataObject_getAsBase64String.md) | Gets the binary data represented by the DataObject as a Base64 encoded string. |
| [saveToFile](DataObject_saveToFile.md) | Saves the data represented by the DataObject to a file. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](DataObject_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataObject_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.createThumbnail](Component_createThumbnail.md), [DataObjectFuture.dataObject](DataObjectFuture_dataObject.md), [FlatPatternComponent.createThumbnail](FlatPatternComponent_createThumbnail.md)

## Version

Introduced in version September 2024  

