# SelectionSets Object

Derived from: [Base](Base.md) Object  

## Description

The SelectionSets object is used to create and access existing selection sets.  

In the user interface, selection sets are created by selecting geometry and then running the "Create Selection Set" command from the context menu. All existing selection sets are shown in a "Selection Sets" folder in the browser.

## Methods

| Name | Description |
|----|----|
| [add](SelectionSets_add.md) | Adds a new SelectionSet to the parent product. |
| [classType](SelectionSets_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SelectionSets_item.md) | Returns the specified SelectionSet object using an index into the collection. |
| [itemByName](SelectionSets_itemByName.md) | Returns the specified SelectionSet object using the name of the selection set. |

## Properties

| Name | Description |
| --- | --- |
| [count](SelectionSets_count.md) | Returns the number of SelectionSet objects in the collection. |
| [isValid](SelectionSets_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SelectionSets_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAM.selectionSets](CAM_selectionSets.md), [Design.selectionSets](Design_selectionSets.md), [Drawing.selectionSets](Drawing_selectionSets.md), [FlatPatternProduct.selectionSets](FlatPatternProduct_selectionSets.md), [Product.selectionSets](Product_selectionSets.md), [WorkingModel.selectionSets](WorkingModel_selectionSets.md)

## Version

Introduced in version May 2022  

