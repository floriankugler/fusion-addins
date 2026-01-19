# ConfigurationFeatureAspectStringCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

Represents a cell from a column that defines a configuration feature aspect that is a String value.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationFeatureAspectStringCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationFeatureAspectStringCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationFeatureAspectStringCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationFeatureAspectStringCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationFeatureAspectStringCell_parentRow.md) | Returns the row this cell is in. |
| [value](ConfigurationFeatureAspectStringCell_value.md) | Gets and sets the value of the property associated with the parent column of this cell. |

## Version

Introduced in version September 2024  

