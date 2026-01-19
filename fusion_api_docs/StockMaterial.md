
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Represents a StockMaterial.

## Methods

| Name | Description |
|----|----|
| [classType](StockMaterial_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFromJson](StockMaterial_createFromJson.md) | Creates a StockMaterial object from given JSON string. |
| [toJson](StockMaterial_toJson.md) | Generates and returns a JSON string that contains a description of this StockMaterial. |

## Properties

| Name | Description |
| --- | --- |
| [category](StockMaterial_category.md) | Gets and sets the category of the stock material. |
| [designators](StockMaterial_designators.md) | Gets a list of designators of the stock material. |
| [hardness](StockMaterial_hardness.md) | Get and sets the hardness of the stock materials. NOTE: the hardness can be NaN if not set. and user can set the hardness to NaN. |
| [isValid](StockMaterial_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](StockMaterial_name.md) | Gets and sets the name of the stock material. |
| [objectType](StockMaterial_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[DocumentStockMaterialLibrary.item](DocumentStockMaterialLibrary_item.md), [Setup.stockMaterial](Setup_stockMaterial.md), [StockMaterial.createFromJson](StockMaterial_createFromJson.md), [StockMaterialLibrary.childStockMaterials](StockMaterialLibrary_childStockMaterials.md), [StockMaterialLibrary.stockMaterialAtURL](StockMaterialLibrary_stockMaterialAtURL.md)

## Version

Introduced in version September 2024  

