# ConfigurationMaterialCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a ConfigurationMaterialTable table that controls which material is assigned to a component or body.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationMaterialCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationMaterialCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [material](ConfigurationMaterialCell_material.md) | Gets and sets the material associated with this cell. When setting this property, the material used must exist in the design. |
| [objectType](ConfigurationMaterialCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationMaterialCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationMaterialCell_parentRow.md) | Returns the row this cell is in. |

## Accessed From

[ConfigurationMaterialColumn.getCell](ConfigurationMaterialColumn_getCell.md), [ConfigurationMaterialColumn.getCellByRowId](ConfigurationMaterialColumn_getCellByRowId.md), [ConfigurationMaterialColumn.getCellByRowName](ConfigurationMaterialColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

