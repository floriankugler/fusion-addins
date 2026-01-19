# PlaneAndOffsetsHolePositionDefinition Object

Derived from: [HolePositionDefinition](HolePositionDefinition.md) Object  

## Description

Provides positioning information for a hole that is positioned on a plane and at a distance from one or two edges.

## Methods

| Name | Description |
|----|----|
| [classType](PlaneAndOffsetsHolePositionDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [edgeOne](PlaneAndOffsetsHolePositionDefinition_edgeOne.md) | The first of 2 edges the hole position is measured from. OffsetOne provides access to the model parameter controlling the offset distance. |
| [edgeTwo](PlaneAndOffsetsHolePositionDefinition_edgeTwo.md) | The second of two edges the hole position is measured from. OffsetTwo provides access to the model parameter controlling the offset distance. This property can return null in the case where only one edge is used. |
| [isValid](PlaneAndOffsetsHolePositionDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PlaneAndOffsetsHolePositionDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offsetOne](PlaneAndOffsetsHolePositionDefinition_offsetOne.md) | Returns the model parameter controlling the distance from the center of the hole to EdgeOne. |
| [offsetTwo](PlaneAndOffsetsHolePositionDefinition_offsetTwo.md) | Returns the model parameter controlling the distance from the center of the hole to EdgeTwo. This property returns null in the case where only one edge is used. |
| [planarEntity](PlaneAndOffsetsHolePositionDefinition_planarEntity.md) | Returns the plane that defines the orientation and start of the hole. |

## Version

Introduced in version August 2014  

