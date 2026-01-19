# Matrix3D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 3D 4x4 matrix. This object is a wrapper over 3D matrix data and is used as way to pass matrix data in and out of the API and as a convenience when operating on matrix data. They are created statically using the create method of the Matrix3D class.

## Methods

| Name | Description |
|----|----|
| [asArray](Matrix3D_asArray.md) | Returns the contents of the matrix as a 16 element array. |
| [classType](Matrix3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Matrix3D_copy.md) | Creates an independent copy of this matrix. |
| [create](Matrix3D_create.md) | Creates a transient 3d matrix object. It is initialized as an identity matrix and is created statically using the Matrix3D.create method. |
| [getAsCoordinateSystem](Matrix3D_getAsCoordinateSystem.md) | Gets the matrix data as the components that define a coordinate system. |
| [getCell](Matrix3D_getCell.md) | Gets the value of the specified cell in the 4x4 matrix. |
| [invert](Matrix3D_invert.md) | Inverts this matrix. |
| [isEqualTo](Matrix3D_isEqualTo.md) | Compares this matrix with another matrix and returns True if they're identical. |
| [setCell](Matrix3D_setCell.md) | Sets the specified cell in the 4x4 matrix to the specified value. |
| [setToAlignCoordinateSystems](Matrix3D_setToAlignCoordinateSystems.md) | Sets this matrix to be the matrix that maps from the 'from' coordinate system to the 'to' coordinate system. |
| [setToIdentity](Matrix3D_setToIdentity.md) | Resets this matrix to an identify matrix. |
| [setToRotateTo](Matrix3D_setToRotateTo.md) | Sets to the matrix of rotation that would align the 'from' vector with the 'to' vector. The optional axis argument may be used when the two vectors are perpendicular and in opposite directions to specify a specific solution, but is otherwise ignored |
| [setToRotation](Matrix3D_setToRotation.md) | Sets this matrix to the matrix of rotation by the specified angle, through the specified origin, around the specified axis |
| [setWithArray](Matrix3D_setWithArray.md) | Sets the contents of the array using a 16 element array. |
| [setWithCoordinateSystem](Matrix3D_setWithCoordinateSystem.md) | Sets the matrix based on the components of a coordinate system. |
| [transformBy](Matrix3D_transformBy.md) | Transforms this matrix using the input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [determinant](Matrix3D_determinant.md) | Returns the determinant of the matrix. |
| [isValid](Matrix3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Matrix3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [translation](Matrix3D_translation.md) | Gets and sets the translation component of the matrix. |

## Accessed From

[AsBuiltJoint.transform](AsBuiltJoint_transform.md), [ConstructionPlane.transform](ConstructionPlane_transform.md), [CustomGraphicsBRepBody.transform](CustomGraphicsBRepBody_transform.md), [CustomGraphicsCurve.transform](CustomGraphicsCurve_transform.md), [CustomGraphicsEntity.transform](CustomGraphicsEntity_transform.md), [CustomGraphicsGroup.transform](CustomGraphicsGroup_transform.md), [CustomGraphicsLines.transform](CustomGraphicsLines_transform.md), [CustomGraphicsMesh.transform](CustomGraphicsMesh_transform.md), [CustomGraphicsPointSet.transform](CustomGraphicsPointSet_transform.md), [CustomGraphicsText.transform](CustomGraphicsText_transform.md), [Decal.transform](Decal_transform.md), [DecalInput.transform](DecalInput_transform.md), [Joint.geometryOneTransform](Joint_geometryOneTransform.md), [Joint.geometryTwoTransform](Joint_geometryTwoTransform.md), [JointOrigin.transform](JointOrigin_transform.md), [Matrix3D.copy](Matrix3D_copy.md), [Matrix3D.create](Matrix3D_create.md), [Matrix3DGraphNodeProperty.value](Matrix3DGraphNodeProperty_value.md), [MoveFeature.transform](MoveFeature_transform.md), [MoveFeatureFreeMoveDefinition.transform](MoveFeatureFreeMoveDefinition_transform.md), [MoveFeatureInput.transform](MoveFeatureInput_transform.md), [Occurrence.initialTransform](Occurrence_initialTransform.md), [Occurrence.transform](Occurrence_transform.md), [Occurrence.transform2](Occurrence_transform2.md), [OptimizedOrientationResult.transformation](OptimizedOrientationResult_transformation.md), [PatternElement.transform](PatternElement_transform.md), [ProjectedTextureMapControl.transform](ProjectedTextureMapControl_transform.md), [SectionAnalysis.initialPosition](SectionAnalysis_initialPosition.md), [SectionAnalysis.transform](SectionAnalysis_transform.md), [SectionAnalysisInput.initialPosition](SectionAnalysisInput_initialPosition.md), [SectionAnalysisInput.transform](SectionAnalysisInput_transform.md), [Setup.workCoordinateSystem](Setup_workCoordinateSystem.md), [Sketch.transform](Sketch_transform.md), [SVGImportOptions.transform](SVGImportOptions_transform.md), [TextureMapControl3D.transform](TextureMapControl3D_transform.md), [TriadCommandInput.lastTransform](TriadCommandInput_lastTransform.md), [TriadCommandInput.positionTransform](TriadCommandInput_positionTransform.md), [TriadCommandInput.transform](TriadCommandInput_transform.md), [Viewport.modelToViewSpaceTransform](Viewport_modelToViewSpaceTransform.md)

## Samples

| Name | Description |
|----|----|
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |

## Version

Introduced in version August 2014  

