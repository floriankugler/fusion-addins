# ConfigurationAppearanceCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a single cell within a ConfigurationAppearanceTable table that controls which appearance is assigned to a component or body.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationAppearanceCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [appearance](ConfigurationAppearanceCell_appearance.md) | Gets and sets the appearance associated with this cell. This property can return null indicating the appearance from the physical material assigned to the object is inherited. Setting the property to null will inherit the appearance from the physical material assigned to the object. |
| [isValid](ConfigurationAppearanceCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationAppearanceCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationAppearanceCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationAppearanceCell_parentRow.md) | Returns the row this cell is in. |

## Accessed From

[ConfigurationAppearanceColumn.getCell](ConfigurationAppearanceColumn_getCell.md), [ConfigurationAppearanceColumn.getCellByRowId](ConfigurationAppearanceColumn_getCellByRowId.md), [ConfigurationAppearanceColumn.getCellByRowName](ConfigurationAppearanceColumn_getCellByRowName.md)

## Version

Introduced in version January 2024  

