# BoundingBox3D Object

Derived from: [Base](Base.md) Object  

## Description

Transient object that represents a 3D bounding box. It defines a rectangular box whose sides are parallel to the model space x, y, and z planes. Because of the fixed orientation of the box it can be fully defined by two points at opposing corners; the min and max points. This object is usually used to provide a rough approximation of the volume in space that an entity occupies. It also provides some convenience function when working with the bounding box data. They are created statically using the create method of the BoundingBox3D class.

## Methods

| Name | Description |
|----|----|
| [classType](BoundingBox3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [combine](BoundingBox3D_combine.md) | Combines this bounding box with the input bounding box. If the input bounding box extends outside this bounding box then this bounding box will be extended to encompass both of the original bounding boxes. |
| [contains](BoundingBox3D_contains.md) | Determines if the specified point is within the bound box. |
| [copy](BoundingBox3D_copy.md) | Creates an independent copy of this bounding box. |
| [create](BoundingBox3D_create.md) | Creates a transient bounding box object. This object is created statically using the BoundingBox3D.create method. |
| [expand](BoundingBox3D_expand.md) | Expands the size of bounding box to include the specified point. |
| [intersects](BoundingBox3D_intersects.md) | Determines if the two bounding boxes intersect. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](BoundingBox3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxPoint](BoundingBox3D_maxPoint.md) | Gets and sets the maximum point corner of the box. |
| [minPoint](BoundingBox3D_minPoint.md) | Gets and sets the minimum point corner of the box. |
| [objectType](BoundingBox3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Arrange3DResultEnvelope.boundingBox](Arrange3DResultEnvelope_boundingBox.md), [BoundingBox3D.copy](BoundingBox3D_copy.md), [BoundingBox3D.create](BoundingBox3D_create.md), [BRepBody.boundingBox](BRepBody_boundingBox.md), [BRepBody.preciseBoundingBox](BRepBody_preciseBoundingBox.md), [BRepEdge.boundingBox](BRepEdge_boundingBox.md), [BRepFace.boundingBox](BRepFace_boundingBox.md), [BRepLoop.boundingBox](BRepLoop_boundingBox.md), [BRepLump.boundingBox](BRepLump_boundingBox.md), [BRepShell.boundingBox](BRepShell_boundingBox.md), [Component.boundingBox](Component_boundingBox.md), [Component.boundingBox2](Component_boundingBox2.md), [Component.preciseBoundingBox](Component_preciseBoundingBox.md), [CustomGraphicsBRepBody.boundingBox](CustomGraphicsBRepBody_boundingBox.md), [CustomGraphicsCurve.boundingBox](CustomGraphicsCurve_boundingBox.md), [CustomGraphicsEntity.boundingBox](CustomGraphicsEntity_boundingBox.md), [CustomGraphicsGroup.boundingBox](CustomGraphicsGroup_boundingBox.md), [CustomGraphicsLines.boundingBox](CustomGraphicsLines_boundingBox.md), [CustomGraphicsMesh.boundingBox](CustomGraphicsMesh_boundingBox.md), [CustomGraphicsPointSet.boundingBox](CustomGraphicsPointSet_boundingBox.md), [CustomGraphicsText.boundingBox](CustomGraphicsText_boundingBox.md), [FaceGroup.boundingBox](FaceGroup_boundingBox.md), [FlatPatternComponent.boundingBox](FlatPatternComponent_boundingBox.md), [FlatPatternComponent.boundingBox2](FlatPatternComponent_boundingBox2.md), [FlatPatternComponent.preciseBoundingBox](FlatPatternComponent_preciseBoundingBox.md), [MeshBody.boundingBox](MeshBody_boundingBox.md), [Occurrence.boundingBox](Occurrence_boundingBox.md), [Occurrence.boundingBox2](Occurrence_boundingBox2.md), [Occurrence.preciseBoundingBox](Occurrence_preciseBoundingBox.md), [Profile.boundingBox](Profile_boundingBox.md), [ProfileCurve.boundingBox](ProfileCurve_boundingBox.md), [Sketch.boundingBox](Sketch_boundingBox.md), [SketchArc.boundingBox](SketchArc_boundingBox.md), [SketchCircle.boundingBox](SketchCircle_boundingBox.md), [SketchConicCurve.boundingBox](SketchConicCurve_boundingBox.md), [SketchControlPointSpline.boundingBox](SketchControlPointSpline_boundingBox.md), [SketchCurve.boundingBox](SketchCurve_boundingBox.md), [SketchEllipse.boundingBox](SketchEllipse_boundingBox.md), [SketchEllipticalArc.boundingBox](SketchEllipticalArc_boundingBox.md), [SketchEntity.boundingBox](SketchEntity_boundingBox.md), [SketchFittedSpline.boundingBox](SketchFittedSpline_boundingBox.md), [SketchFixedSpline.boundingBox](SketchFixedSpline_boundingBox.md), [SketchLine.boundingBox](SketchLine_boundingBox.md), [SketchPoint.boundingBox](SketchPoint_boundingBox.md), [SketchText.boundingBox](SketchText_boundingBox.md)

## Samples

| Name | Description |
| --- | --- |
| [Rendering Sample](RenderSample_Sample.md) | Demonstrates using the Rendering capabilities in the API. This starts a series of local renderings to generate a series of frames, where the camera is repositioned and a parameter is modified for each frame to create a dynamic animation. To use the sample, have a design open that contains a parameter named "Length". It can be a user or model parameter. The sample will modify this parameter from a value of 0.1 cm to 15 cm, but you can change these values by editing the values of the paramStartVal and paramEndVal variables on lines 90 and 91 of the sample. It expects a folder named "C:\Temp\RenderSample" to exist, and will fail if it doesn't. The rendered frames will be written to that folder. An example rendering is shown below where [this file](../ExtraFiles/RenderSample.f3d) was used. The parameter is modifying a move feature which results in changing the shape of an extrusion. The parameter could be driving anything and you could modify the code to edit more than one parameter. The result of this sample is a folder containing all of the rendered frames. You can process these to create an animation. The sample animation was created using GIMP. |

## Version

Introduced in version August 2014  

