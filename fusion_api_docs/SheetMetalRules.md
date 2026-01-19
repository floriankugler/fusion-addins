# SheetMetalRules Object

Derived from: [Base](Base.md) Object  

## Description

A collection of sheet metal rules.

## Methods

| Name | Description |
|----|----|
| [addByCopy](SheetMetalRules_addByCopy.md) | Creates a new sheet metal rule by copying an existing rule. The new rule can then be edited to define the rule characteristics you want. |
| [classType](SheetMetalRules_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SheetMetalRules_item.md) | Function that returns the specified sheet metal rule using an index into the collection. |
| [itemByName](SheetMetalRules_itemByName.md) | Function that returns the specified sheet metal rule using the name of the rule. |

## Properties

| Name | Description |
| --- | --- |
| [count](SheetMetalRules_count.md) | The number of sheet metal rules in the collection. |
| [isValid](SheetMetalRules_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SheetMetalRules_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.designSheetMetalRules](Design_designSheetMetalRules.md), [Design.librarySheetMetalRules](Design_librarySheetMetalRules.md), [FlatPatternProduct.designSheetMetalRules](FlatPatternProduct_designSheetMetalRules.md), [FlatPatternProduct.librarySheetMetalRules](FlatPatternProduct_librarySheetMetalRules.md), [WorkingModel.designSheetMetalRules](WorkingModel_designSheetMetalRules.md), [WorkingModel.librarySheetMetalRules](WorkingModel_librarySheetMetalRules.md)

## Samples

| Name | Description |
|----|----|
| [Sheet Metal Rules Sample](Sheet%20Metal%20Rules%20Sample_Sample.htm) | Demonstrates creating adding a sheet metal rule. |

## Version

Introduced in version November 2022  

