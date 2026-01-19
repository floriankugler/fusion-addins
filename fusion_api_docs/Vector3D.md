# Vector3D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 3D vector. This object is a wrapper over 3D vector data and is used as way to pass vector data in and out of the API and as a convenience when operating on vector data. They are created statically using the create method of the Vector3D class.

## Methods

| Name | Description |
|----|----|
| [add](Vector3D_add.md) | Adds a vector to this vector. |
| [angleTo](Vector3D_angleTo.md) | Determines the angle between this vector and the specified vector. |
| [asArray](Vector3D_asArray.md) | Returns the vector coordinates as an array \[x, y, z\]. |
| [asPoint](Vector3D_asPoint.md) | Returns a new point with the same coordinate values as this vector. |
| [classType](Vector3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Vector3D_copy.md) | Creates a copy of this vector. |
| [create](Vector3D_create.md) | Creates a 3D vector object. This object is created statically using the Vector3D.create method. |
| [crossProduct](Vector3D_crossProduct.md) | Returns the cross product between this vector and the specified vector. |
| [dotProduct](Vector3D_dotProduct.md) | Returns the dot product between this vector and the specified vector. |
| [isEqualTo](Vector3D_isEqualTo.md) | Determines if this vector is equal to the specified vector. |
| [isParallelTo](Vector3D_isParallelTo.md) | Determines if the input vector is parallel with this vector. |
| [isPerpendicularTo](Vector3D_isPerpendicularTo.md) | Determines if the input vector is perpendicular to this vector. |
| [normalize](Vector3D_normalize.md) | Makes this vector of unit length. This vector should not be zero length. |
| [scaleBy](Vector3D_scaleBy.md) | Scale this vector by the specified product. |
| [setWithArray](Vector3D_setWithArray.md) | Reset this vector with the coordinate values in an array \[x, y, z\]. |
| [subtract](Vector3D_subtract.md) | Subtract a vector from this vector. |
| [transformBy](Vector3D_transformBy.md) | Transform this vector by the specified matrix. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Vector3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [length](Vector3D_length.md) | Get the length of this vector. |
| [objectType](Vector3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [x](Vector3D_x.md) | The x value. |
| [y](Vector3D_y.md) | The y value. |
| [z](Vector3D_z.md) | The z value. |

## Accessed From

[AngleValueCommandInput.manipulatorXDirection](AngleValueCommandInput_manipulatorXDirection.md), [AngleValueCommandInput.manipulatorYDirection](AngleValueCommandInput_manipulatorYDirection.md), [Arc3D.getData](Arc3D_getData.md), [Arc3D.normal](Arc3D_normal.md), [Arc3D.referenceVector](Arc3D_referenceVector.md), [AreaProperties.getPrincipalAxes](AreaProperties_getPrincipalAxes.md), [ArrangeComponent.upDirection](ArrangeComponent_upDirection.md), [ArrangeComponent.zeroDirection](ArrangeComponent_zeroDirection.md), [BallJointMotion.pitchDirectionVector](BallJointMotion_pitchDirectionVector.md), [BallJointMotion.rollDirectionVector](BallJointMotion_rollDirectionVector.md), [BallJointMotion.yawDirectionVector](BallJointMotion_yawDirectionVector.md), [BossFeature.direction](BossFeature_direction.md), [Camera.upVector](Camera_upVector.md), [Circle3D.getData](Circle3D_getData.md), [Circle3D.normal](Circle3D_normal.md), [Cone.axis](Cone_axis.md), [Cone.getData](Cone_getData.md), [CurveEvaluator3D.getCurvature](CurveEvaluator3D_getCurvature.md), [CurveEvaluator3D.getFirstDerivative](CurveEvaluator3D_getFirstDerivative.md), [CurveEvaluator3D.getSecondDerivative](CurveEvaluator3D_getSecondDerivative.md), [CurveEvaluator3D.getTangent](CurveEvaluator3D_getTangent.md), [CurveEvaluator3D.getThirdDerivative](CurveEvaluator3D_getThirdDerivative.md), [CustomGraphicsBillBoard.axis](CustomGraphicsBillBoard_axis.md), [Cylinder.axis](Cylinder_axis.md), [Cylinder.getData](Cylinder_getData.md), [CylindricalJointMotion.rotationAxisVector](CylindricalJointMotion_rotationAxisVector.md), [DirectionCommandInput.manipulatorDirection](DirectionCommandInput_manipulatorDirection.md), [DistanceValueCommandInput.manipulatorDirection](DistanceValueCommandInput_manipulatorDirection.md), [Ellipse3D.getData](Ellipse3D_getData.md), [Ellipse3D.majorAxis](Ellipse3D_majorAxis.md), [Ellipse3D.normal](Ellipse3D_normal.md), [EllipticalArc3D.getData](EllipticalArc3D_getData.md), [EllipticalArc3D.majorAxis](EllipticalArc3D_majorAxis.md), [EllipticalArc3D.normal](EllipticalArc3D_normal.md), [EllipticalCone.getAxes](EllipticalCone_getAxes.md), [EllipticalCone.getData](EllipticalCone_getData.md), [EllipticalCylinder.axis](EllipticalCylinder_axis.md), [EllipticalCylinder.getData](EllipticalCylinder_getData.md), [EllipticalCylinder.majorAxis](EllipticalCylinder_majorAxis.md), [ExtruderMachineElement.offset](ExtruderMachineElement_offset.md), [HoleFeature.direction](HoleFeature_direction.md), [InfiniteLine3D.direction](InfiniteLine3D_direction.md), [InfiniteLine3D.getData](InfiniteLine3D_getData.md), [JointGeometry.primaryAxisVector](JointGeometry_primaryAxisVector.md), [JointGeometry.secondaryAxisVector](JointGeometry_secondaryAxisVector.md), [JointGeometry.thirdAxisVector](JointGeometry_thirdAxisVector.md), [JointOrigin.primaryAxisVector](JointOrigin_primaryAxisVector.md), [JointOrigin.secondaryAxisVector](JointOrigin_secondaryAxisVector.md), [JointOrigin.thirdAxisVector](JointOrigin_thirdAxisVector.md), [JointOriginInput.primaryAxisVector](JointOriginInput_primaryAxisVector.md), [JointOriginInput.secondaryAxisVector](JointOriginInput_secondaryAxisVector.md), [JointOriginInput.thirdAxisVector](JointOriginInput_thirdAxisVector.md), [LinearMachineAxis.direction](LinearMachineAxis_direction.md), [LinearMachineAxisInput.direction](LinearMachineAxisInput_direction.md), [Matrix3D.getAsCoordinateSystem](Matrix3D_getAsCoordinateSystem.md), [Matrix3D.translation](Matrix3D_translation.md), [MultiAxisRetractAndReconfigureSettings.stockExpansion](MultiAxisRetractAndReconfigureSettings_stockExpansion.md), [OrientedBoundingBox3D.heightDirection](OrientedBoundingBox3D_heightDirection.md), [OrientedBoundingBox3D.lengthDirection](OrientedBoundingBox3D_lengthDirection.md), [OrientedBoundingBox3D.widthDirection](OrientedBoundingBox3D_widthDirection.md), [PhysicalProperties.getPrincipalAxes](PhysicalProperties_getPrincipalAxes.md), [PinSlotJointMotion.rotationAxisVector](PinSlotJointMotion_rotationAxisVector.md), [PinSlotJointMotion.slideDirectionVector](PinSlotJointMotion_slideDirectionVector.md), [PlanarJointMotion.normalDirectionVector](PlanarJointMotion_normalDirectionVector.md), [PlanarJointMotion.primarySlideDirectionVector](PlanarJointMotion_primarySlideDirectionVector.md), [PlanarJointMotion.secondarySlideDirectionVector](PlanarJointMotion_secondarySlideDirectionVector.md), [Plane.normal](Plane_normal.md), [Plane.uDirection](Plane_uDirection.md), [Plane.vDirection](Plane_vDirection.md), [Point3D.asVector](Point3D_asVector.md), [Point3D.vectorTo](Point3D_vectorTo.md), [PolygonMesh.normalVectors](PolygonMesh_normalVectors.md), [RecognizedHole.axis](RecognizedHole_axis.md), [RecognizedHoleSegment.axis](RecognizedHoleSegment_axis.md), [RectangularPatternFeature.directionOne](RectangularPatternFeature_directionOne.md), [RectangularPatternFeature.directionTwo](RectangularPatternFeature_directionTwo.md), [RectangularPatternFeatureInput.directionOne](RectangularPatternFeatureInput_directionOne.md), [RectangularPatternFeatureInput.directionTwo](RectangularPatternFeatureInput_directionTwo.md), [RevoluteJointMotion.rotationAxisVector](RevoluteJointMotion_rotationAxisVector.md), [Sketch.xDirection](Sketch_xDirection.md), [Sketch.yDirection](Sketch_yDirection.md), [SketchEllipse.majorAxis](SketchEllipse_majorAxis.md), [SketchEllipticalArc.majorAxis](SketchEllipticalArc_majorAxis.md), [SliderJointMotion.slideDirectionVector](SliderJointMotion_slideDirectionVector.md), [SurfaceEvaluator.getCurvature](SurfaceEvaluator_getCurvature.md), [SurfaceEvaluator.getFirstDerivative](SurfaceEvaluator_getFirstDerivative.md), [SurfaceEvaluator.getNormalAtParameter](SurfaceEvaluator_getNormalAtParameter.md), [SurfaceEvaluator.getNormalAtPoint](SurfaceEvaluator_getNormalAtPoint.md), [SurfaceEvaluator.getSecondDerivative](SurfaceEvaluator_getSecondDerivative.md), [SurfaceEvaluator.getThirdDerivative](SurfaceEvaluator_getThirdDerivative.md), [ToEntityExtentDefinition.directionHint](ToEntityExtentDefinition_directionHint.md), [Torus.axis](Torus_axis.md), [Torus.getData](Torus_getData.md), [TriangleMesh.normalVectors](TriangleMesh_normalVectors.md), [Vector3D.copy](Vector3D_copy.md), [Vector3D.create](Vector3D_create.md), [Vector3D.crossProduct](Vector3D_crossProduct.md), [Vector3DGraphNodeProperty.value](Vector3DGraphNodeProperty_value.md), [Viewport.frontEyeDirection](Viewport_frontEyeDirection.md), [Viewport.frontUpDirection](Viewport_frontUpDirection.md), [VolumetricVectorSample.value](VolumetricVectorSample_value.md)

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |

## Version

Introduced in version August 2014  

