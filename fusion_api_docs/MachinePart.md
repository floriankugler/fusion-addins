# MachinePart Object

Derived from: [Base](Base.md) Object  

## Description

Object representing some part of a machine, such as the static base of the machine, an axis, or the attachment points for tools and fixtures.

## Methods

| Name | Description |
|----|----|
| [classType](MachinePart_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](MachinePart_deleteMe.md) | Delete this part and its children from the kinematics tree. |

## Properties

| Name | Description |
| --- | --- |
| [axis](MachinePart_axis.md) | Get the axis object for this part used to reference this part for other operations. Only valid when partType is Axis, otherwise returns null |
| [children](MachinePart_children.md) | Get the collection of child parts. |
| [id](MachinePart_id.md) | Get the internal ID of the part. This is unique with respect to other MachineParts in the Machine. |
| [isValid](MachinePart_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachinePart_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](MachinePart_parent.md) | Get or set the parent of this part. Returns null if this part is a root part. Setting the parent will add this part to the end of the parent's children collection. Setting the parent will throw an error if the new parent is this part or a child of this part. |
| [partType](MachinePart_partType.md) | Get the type of this part. |
| [spindle](MachinePart_spindle.md) | Get the spindle object for this part used to reference this part for other operations. Will return null if the part has no spindle assigned. |
| [toolStation](MachinePart_toolStation.md) | Get the tool station object for this part. Will return null if the part has no tool station assigned. |

## Accessed From

[MachineItem.part](MachineItem_part.md), [MachinePart.parent](MachinePart_parent.md), [MachineParts.add](MachineParts_add.md), [MachineParts.item](MachineParts_item.md), [MachineParts.itemById](MachineParts_itemById.md)

## Version

Introduced in version April 2023  

