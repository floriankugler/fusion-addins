# ConfigurationJointSnapCell Object

Derived from: [ConfigurationCell](ConfigurationCell.md) Object  

## Description

This object represents a joint snap that has been defined for a ConfigurationJointSnapColumn. Joint snaps are defined on the parent column, and the cell specifies which of the defined snaps will be used when the parent row of the cell is active.

## Methods

| Name | Description |
|----|----|
| [classType](ConfigurationJointSnapCell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ConfigurationJointSnapCell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConfigurationJointSnapCell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentColumn](ConfigurationJointSnapCell_parentColumn.md) | Returns the column this cell is in. |
| [parentRow](ConfigurationJointSnapCell_parentRow.md) | Returns the row this cell is in. |
| [snap](ConfigurationJointSnapCell_snap.md) | Gets and sets which snap will be used when the row this cell is in is active. When setting this property, only snaps defined for the parent column of this cell can be used. |

## Version

Introduced in version September 2024  

