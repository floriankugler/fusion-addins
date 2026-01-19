# Milestone Object

Derived from: [Base](Base.md) Object  

## Description

An object that represents a milestone.

## Methods

| Name | Description |
|----|----|
| [classType](Milestone_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Milestone_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](Milestone_name.md) | Gets and sets the name of the milestone. |
| [objectType](Milestone_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [version](Milestone_version.md) | Returns the file version associated with this milestone. |

## Accessed From

[DataFile.createMilestone](DataFile_createMilestone.md), [DataFile.milestone](DataFile_milestone.md), [DesignDataFile.createMilestone](DesignDataFile_createMilestone.htm), [DesignDataFile.milestone](DesignDataFile_milestone.htm), [Milestones.asArray](Milestones_asArray.md), [Milestones.item](Milestones_item.md), [Milestones.itemByName](Milestones_itemByName.md)

## Version

Introduced in version March 2024  

