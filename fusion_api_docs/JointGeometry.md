# JointGeometry Object

Derived from: [Base](Base.md) Object  

## Description

A transient object used to define and query the geometric input of a joint and the resulting coordinate system it defines. New JointGeometry objects are created using its various static create methods and are then used as input to the Joints.createInput method.

## Methods

| Name | Description |
|----|----|
| [classType](JointGeometry_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createByBetweenTwoPlanes](JointGeometry_createByBetweenTwoPlanes.md) | Creates a new transient JointGeometry object based on a plane bisecting the two input planes. |
| [createByCurve](JointGeometry_createByCurve.md) | Creates a new transient JointGeometry object using a BRepEdge or SketchCurve as input. A JointGeometry object can be used to create a joint or joint origin. |
| [createByCylinderOrConeFace](JointGeometry_createByCylinderOrConeFace.md) | Creates a new transient JointGeometry object based on a cylinder or cone BRepFace object. |
| [createByNonPlanarFace](JointGeometry_createByNonPlanarFace.md) | Creates a new transient JointGeometry object based on a non-planar analytical BRepFace object. This is limited to cylinders, cones, spheres, and tori. A JointGeometry object can be used to create a joint or joint origin. |
| [createByPlanarFace](JointGeometry_createByPlanarFace.md) | Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry object can be used to create a joint or joint origin. |
| [createByPoint](JointGeometry_createByPoint.md) | Creates a new transient JointGeometry object using a ConstructionPoint, SketchPoint or BRepVertex as input. A JointGeometry object can be used to create a joint or joint origin. |
| [createByProfile](JointGeometry_createByProfile.md) | Creates a new transient JointGeometry object based on a planar BRepFace object. A JointGeometry object can be used to create a joint or joint origin. |
| [createBySphereFace](JointGeometry_createBySphereFace.md) | Creates a new transient JointGeometry object based on a sphere BRepFace object. |
| [createBySplineFace](JointGeometry_createBySplineFace.md) | Creates a new transient JointGeometry object based on a spline BRepFace object. |
| [createByTangentFaceEdge](JointGeometry_createByTangentFaceEdge.md) | Creates a new transient JointGeometry object based on a BRepFace object as well as a BRepEdge object which is on the BRepFace. |
| [createByTorusFace](JointGeometry_createByTorusFace.md) | Creates a new transient JointGeometry object based on a torus BRepFace object. |
| [createByTwoEdgeIntersection](JointGeometry_createByTwoEdgeIntersection.md) | Creates a new transient JointGeometry object that is positioned at the intersection of the two input linear BRepEdge objects. |

## Properties

| Name | Description |
| --- | --- |
| [entityOne](JointGeometry_entityOne.md) | The first entity that's defining this joint geometry. This can be various types of geometry depending on how this joint geometry is defined. The geometryType property indicates how this joint geometry is defined a provides a clue about the type of geometry to expect back from this property. |
| [entityTwo](JointGeometry_entityTwo.md) | This is the second entity that defines this joint geometry. This isn't used for all joint geometry types and will return null in the cases where it's not used. A second geometry is used in the case where the geometryType property returns JointProfileGeometry, JointPlanarBRepFaceGeometry, JointBetweenTwoFacesGeometry or JointByTwoEdgeIntersectionGeometry. |
| [geometryType](JointGeometry_geometryType.md) | Returns the type of geometry this JointGeometry object represents. |
| [isValid](JointGeometry_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [keyPointType](JointGeometry_keyPointType.md) | Returns the keypoint type this JointGeometry is using. |
| [objectType](JointGeometry_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](JointGeometry_origin.md) | Returns the origin point that's been calculated for this joint geometry. |
| [planeOne](JointGeometry_planeOne.md) | Returns the first plane for joint geometry that is defined between two planes. Returns null in all other cases. |
| [planeTwo](JointGeometry_planeTwo.md) | Returns the second plane for joint geometry that is defined between two planes. Returns null in all other cases. |
| [primaryAxisVector](JointGeometry_primaryAxisVector.md) | Returns the direction of the primary axis that's been calculated for this joint geometry. Conceptually, this is the Z-axis of the computed coordinate system. |
| [secondaryAxisVector](JointGeometry_secondaryAxisVector.md) | Returns the direction of the secondary axis that's been calculated for this joint geometry. Conceptually, this is the X-axis of the computed coordinate system. |
| [tangentFaceParamOne](JointGeometry_tangentFaceParamOne.md) | Returns the first tangent face parameter. |
| [tangentFaceParamTwo](JointGeometry_tangentFaceParamTwo.md) | Returns the second tangent face parameter. |
| [tangentFaceType](JointGeometry_tangentFaceType.md) | Returns the tangent face type this JointGeometry is using. |
| [thirdAxisVector](JointGeometry_thirdAxisVector.md) | Returns the direction of the third axis that's been calculated for this joint geometry. Conceptually, this is the Y-axis of the computed coordinate system. |

## Accessed From

[AsBuiltJoint.geometry](AsBuiltJoint_geometry.md), [AsBuiltJointInput.geometry](AsBuiltJointInput_geometry.md), [JointGeometry.createByBetweenTwoPlanes](JointGeometry_createByBetweenTwoPlanes.md), [JointGeometry.createByCurve](JointGeometry_createByCurve.md), [JointGeometry.createByCylinderOrConeFace](JointGeometry_createByCylinderOrConeFace.md), [JointGeometry.createByNonPlanarFace](JointGeometry_createByNonPlanarFace.md), [JointGeometry.createByPlanarFace](JointGeometry_createByPlanarFace.md), [JointGeometry.createByPoint](JointGeometry_createByPoint.md), [JointGeometry.createByProfile](JointGeometry_createByProfile.md), [JointGeometry.createBySphereFace](JointGeometry_createBySphereFace.md), [JointGeometry.createBySplineFace](JointGeometry_createBySplineFace.md), [JointGeometry.createByTangentFaceEdge](JointGeometry_createByTangentFaceEdge.md), [JointGeometry.createByTorusFace](JointGeometry_createByTorusFace.md), [JointGeometry.createByTwoEdgeIntersection](JointGeometry_createByTwoEdgeIntersection.md), [JointOrigin.geometry](JointOrigin_geometry.md), [JointOriginInput.geometry](JointOriginInput_geometry.md)

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Joint Origin Between Two Faces Sample](JointOrigin2Planes_Sample.md) | Demonstrates creating a new Joint Origin between two planes. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

