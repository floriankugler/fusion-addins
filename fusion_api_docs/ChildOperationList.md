# ChildOperationList Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the collection of child operations, folders and patterns of an existing setup.

## Methods

| Name | Description |
|----|----|
| [classType](ChildOperationList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ChildOperationList_item.md) | Returns the specified item using an index into the collection. |
| [itemByName](ChildOperationList_itemByName.md) | Returns the operation, folder or pattern with the specified name (the name seen in the browser). |
| [itemByOperationId](ChildOperationList_itemByOperationId.md) | Returns the operation, folder or pattern with the specified operation id. |

## Properties

| Name | Description |
| --- | --- |
| [count](ChildOperationList_count.md) | Gets the number of objects in the collection. |
| [isValid](ChildOperationList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ChildOperationList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMFolder.children](CAMFolder_children.md), [CAMHoleRecognition.children](CAMHoleRecognition_children.md), [CAMPattern.children](CAMPattern_children.md), [Setup.children](Setup_children.md)

## Version

Introduced in version January 2016  

