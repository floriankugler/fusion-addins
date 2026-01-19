# ContactSet Object

Derived from: [Base](Base.md) Object  

## Description

Represents a contact set in a design.

## Methods

| Name | Description |
|----|----|
| [classType](ContactSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ContactSet_deleteMe.md) | Deletes this contact set from the design. |

## Properties

| Name | Description |
| --- | --- |
| [isSuppressed](ContactSet_isSuppressed.md) | Gets and sets if this contact set is currently suppressed. |
| [isValid](ContactSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ContactSet_name.md) | Gets and sets the name of the contact set. |
| [objectType](ContactSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurencesAndBodies](ContactSet_occurencesAndBodies.md) | Gets and sets the group of Occurrence and/or BRepBody objects that are part of this contact set. |

## Accessed From

[ContactSets.add](ContactSets_add.md), [ContactSets.item](ContactSets_item.md), [ContactSets.itemByName](ContactSets_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version September 2016  

