# Components Object

Derived from: [Base](Base.md) Object  

## Description

The Components collection object provides access to existing components in a design.

## Methods

| Name | Description |
|----|----|
| [classType](Components_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Components_item.md) | Function that returns the specified component using an index into the collection. |
| [itemById](Components_itemById.md) | Returns the Component that has the specified ID. |
| [itemByName](Components_itemByName.md) | Function that returns the specified component by name. |

## Properties

| Name | Description |
| --- | --- |
| [count](Components_count.md) | The number of components in the collection. |
| [isValid](Components_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Components_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.allComponents](Design_allComponents.md), [FlatPatternProduct.allComponents](FlatPatternProduct_allComponents.md), [WorkingModel.allComponents](WorkingModel_allComponents.md)

## Samples

| Name | Description |
| --- | --- |
| [Library Item API Sample](LibraryItemSample_Sample.md) | Demonstrates how to examine library items using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the existing default code. The script will search for and record all components and library items in the current project. They are displayed in a dialog when the script has finished. |

## Version

Introduced in version August 2014  

