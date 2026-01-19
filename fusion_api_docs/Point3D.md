# Point3D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 3D point. A transient point is not displayed or saved in a document. Transient 3D points are used as a wrapper to work with raw 3D point information. They are created statically using the create method of the Point3D class.

## Methods

| Name | Description |
|----|----|
| [asArray](Point3D_asArray.md) | Get coordinate data of the point. |
| [asVector](Point3D_asVector.md) | Defines a vector using the coordinates of the point. |
| [classType](Point3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Point3D_copy.md) | Creates and returns a copy of this point object. |
| [create](Point3D_create.md) | Creates a transient 3D point object. |
| [distanceTo](Point3D_distanceTo.md) | Returns the distance from this point to another point. |
| [getData](Point3D_getData.md) | Gets the data defining the point. |
| [isEqualTo](Point3D_isEqualTo.md) | Checks to see if this point and another point are equal (have identical coordinates). The comparison is done within the modeling tolerance which can be found with the Application.pointTolerance property. If you want to compare two points with any other tolerance you can use the isEqualToByTolerance method. |
| [isEqualToByTolerance](Point3D_isEqualToByTolerance.md) | Checks to see if this point and another point are equal within the specified tolerance. |
| [set](Point3D_set.md) | Sets the data defining the point. |
| [setWithArray](Point3D_setWithArray.md) | Sets the coordinates of the point using an array as input. |
| [transformBy](Point3D_transformBy.md) | Transforms the point using the provided matrix. |
| [translateBy](Point3D_translateBy.md) | Translates the point using the provided vector. |
| [vectorTo](Point3D_vectorTo.md) | Returns a vector from this point to another point. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Point3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Point3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [x](Point3D_x.md) | Gets and sets the X coordinate of the point. |
| [y](Point3D_y.md) | Gets and sets the Y coordinate of the point. |
| [z](Point3D_z.md) | Gets and sets the Z coordinate of the point. |

## Accessed From

[AdditiveFFFLimitsMachineElement.homePosition](AdditiveFFFLimitsMachineElement_homePosition.md), [AdditiveFFFLimitsMachineElement.parkPosition](AdditiveFFFLimitsMachineElement_parkPosition.md), [AdditivePlatformMachineElement.origin](AdditivePlatformMachineElement_origin.md), [AdditivePlatformMachineElement.size](AdditivePlatformMachineElement_size.md), [AngleValueCommandInput.manipulatorOrigin](AngleValueCommandInput_manipulatorOrigin.md), [Arc3D.center](Arc3D_center.md), [Arc3D.endPoint](Arc3D_endPoint.md), [Arc3D.getData](Arc3D_getData.md), [Arc3D.startPoint](Arc3D_startPoint.md), [AreaProperties.centroid](AreaProperties_centroid.md), [BeamNetwork.vertices](BeamNetwork_vertices.md), [BoundingBox3D.maxPoint](BoundingBox3D_maxPoint.md), [BoundingBox3D.minPoint](BoundingBox3D_minPoint.md), [BRepEdge.pointOnEdge](BRepEdge_pointOnEdge.md), [BRepFace.centroid](BRepFace_centroid.md), [BRepFace.pointOnFace](BRepFace_pointOnFace.md), [BRepVertex.geometry](BRepVertex_geometry.md), [BRepVertexDefinition.position](BRepVertexDefinition_position.md), [Camera.eye](Camera_eye.md), [Camera.target](Camera_target.md), [Circle3D.center](Circle3D_center.md), [Circle3D.getData](Circle3D_getData.md), [Cone.getData](Cone_getData.md), [Cone.origin](Cone_origin.md), [ConstructionPoint.geometry](ConstructionPoint_geometry.md), [CurveEvaluator3D.getEndPoints](CurveEvaluator3D_getEndPoints.md), [CurveEvaluator3D.getPointAtParameter](CurveEvaluator3D_getPointAtParameter.md), [CustomGraphicsBillBoard.anchorPoint](CustomGraphicsBillBoard_anchorPoint.md), [CustomGraphicsCoordinates.getCoordinate](CustomGraphicsCoordinates_getCoordinate.md), [CustomGraphicsViewPlacement.anchorPoint](CustomGraphicsViewPlacement_anchorPoint.md), [CustomGraphicsViewScale.anchorPoint](CustomGraphicsViewScale_anchorPoint.md), [Cylinder.getData](Cylinder_getData.md), [Cylinder.origin](Cylinder_origin.md), [DirectionCommandInput.manipulatorOrigin](DirectionCommandInput_manipulatorOrigin.md), [DistanceValueCommandInput.manipulatorOrigin](DistanceValueCommandInput_manipulatorOrigin.md), [Ellipse3D.center](Ellipse3D_center.md), [Ellipse3D.getData](Ellipse3D_getData.md), [EllipticalArc3D.center](EllipticalArc3D_center.md), [EllipticalArc3D.getData](EllipticalArc3D_getData.md), [EllipticalCone.getData](EllipticalCone_getData.md), [EllipticalCone.origin](EllipticalCone_origin.md), [EllipticalCylinder.getData](EllipticalCylinder_getData.md), [EllipticalCylinder.origin](EllipticalCylinder_origin.md), [FaceGroup.centroid](FaceGroup_centroid.md), [HoleFeature.position](HoleFeature_position.md), [InfiniteLine3D.getData](InfiniteLine3D_getData.md), [InfiniteLine3D.origin](InfiniteLine3D_origin.md), [JointGeometry.origin](JointGeometry_origin.md), [Line3D.endPoint](Line3D_endPoint.md), [Line3D.getData](Line3D_getData.md), [Line3D.startPoint](Line3D_startPoint.md), [Matrix3D.getAsCoordinateSystem](Matrix3D_getAsCoordinateSystem.md), [MeasureResults.positionOne](MeasureResults_positionOne.md), [MeasureResults.positionThree](MeasureResults_positionThree.md), [MeasureResults.positionTwo](MeasureResults_positionTwo.md), [NurbsCurve3D.controlPoints](NurbsCurve3D_controlPoints.md), [NurbsSurface.controlPoints](NurbsSurface_controlPoints.md), [OffsetConstraintInput.dimensionPoint](OffsetConstraintInput_dimensionPoint.md), [OrientedBoundingBox3D.centerPoint](OrientedBoundingBox3D_centerPoint.md), [PhysicalProperties.centerOfMass](PhysicalProperties_centerOfMass.md), [Plane.intersectWithLine](Plane_intersectWithLine.md), [Plane.origin](Plane_origin.md), [Point3D.copy](Point3D_copy.md), [Point3D.create](Point3D_create.md), [PolygonMesh.nodeCoordinates](PolygonMesh_nodeCoordinates.md), [Polyline3D.points](Polyline3D_points.md), [RecognizedHole.bottom](RecognizedHole_bottom.md), [RecognizedHole.top](RecognizedHole_top.md), [SceneSettings.centerOfFocus](SceneSettings_centerOfFocus.md), [SceneSettings.groundPosition](SceneSettings_groundPosition.md), [Selection.point](Selection_point.md), [Sketch.modelToSketchSpace](Sketch_modelToSketchSpace.md), [Sketch.origin](Sketch_origin.md), [Sketch.sketchToModelSpace](Sketch_sketchToModelSpace.md), [SketchAngularDimension.textPosition](SketchAngularDimension_textPosition.md), [SketchConcentricCircleDimension.textPosition](SketchConcentricCircleDimension_textPosition.md), [SketchDiameterDimension.textPosition](SketchDiameterDimension_textPosition.md), [SketchDimension.textPosition](SketchDimension_textPosition.md), [SketchDistanceBetweenLineAndPlanarSurfaceDimension.textPosition](SketchDistanceBetweenLineAndPlanarSurfaceDimension_textPosition.md), [SketchDistanceBetweenPointAndSurfaceDimension.textPosition](SketchDistanceBetweenPointAndSurfaceDimension_textPosition.md), [SketchEllipseMajorRadiusDimension.textPosition](SketchEllipseMajorRadiusDimension_textPosition.md), [SketchEllipseMinorRadiusDimension.textPosition](SketchEllipseMinorRadiusDimension_textPosition.md), [SketchLinearDiameterDimension.textPosition](SketchLinearDiameterDimension_textPosition.md), [SketchLinearDimension.textPosition](SketchLinearDimension_textPosition.md), [SketchOffsetCurvesDimension.textPosition](SketchOffsetCurvesDimension_textPosition.md), [SketchOffsetDimension.textPosition](SketchOffsetDimension_textPosition.md), [SketchPoint.geometry](SketchPoint_geometry.md), [SketchPoint.worldGeometry](SketchPoint_worldGeometry.md), [SketchRadialDimension.textPosition](SketchRadialDimension_textPosition.md), [SketchTangentDistanceDimension.textPosition](SketchTangentDistanceDimension_textPosition.md), [SketchText.position](SketchText_position.md), [SketchTextInput.position](SketchTextInput_position.md), [Sphere.getData](Sphere_getData.md), [Sphere.origin](Sphere_origin.md), [SurfaceEvaluator.getPointAtParameter](SurfaceEvaluator_getPointAtParameter.md), [Torus.getData](Torus_getData.md), [Torus.origin](Torus_origin.md), [TriangleMesh.nodeCoordinates](TriangleMesh_nodeCoordinates.md), [Vector3D.asPoint](Vector3D_asPoint.md), [Viewport.viewToModelSpace](Viewport_viewToModelSpace.md), [VolumetricColorSample.point](VolumetricColorSample_point.md), [VolumetricSample.point](VolumetricSample_point.md), [VolumetricScalarSample.point](VolumetricScalarSample_point.md), [VolumetricVectorSample.point](VolumetricVectorSample_point.md)

## Samples

| Name | Description |
|----|----|
| [SketchArcs.addByCenterStartSweep](SketchArcs_addByCenterStartaSweep_Sample.md) | Demonstrates the SketchArcs.addByCenterStartSweep method. |
| [SketchArcs.addByThreePoints](SketchArcs_addByThreePoints_Sample.md) | Demonstrates the SketchArcs.addByThreePoints method. |
| [SketchArcs.addFillet](SketchArcs_addFillet_Sample.md) | Demonstrates the SketchArcs.addFillet method. |

## Version

Introduced in version August 2014  

