# SketchFittedSpline Object

Derived from: [SketchCurve](SketchCurve.md) Object  

## Description

A fitted spline in a sketch.

## Methods

| Name | Description |
| --- | --- |
| [activateCurvatureHandle](SketchFittedSpline_activateCurvatureHandle.md) | Activates the curvature handle for the specified fit point and returns the sketch arc that acts as the handle to control the curvature. You can use the getCurvatureHandle property to determine if the curvature handle has already been activated. If this method is called for a handle that already exists, nothing changes and the existing sketch arc that acts as the curvature handle is returned. The getCurvatureHandle method can be used to determine if the handle has already been activated. To deactivate a sketch handle you can delete the sketch arc. |
| [activateTangentHandle](SketchFittedSpline_activateTangentHandle.md) | Activates the tangent handle for the specified fit point and returns the sketch line that acts as the handle to control the tangency. You can use the getTangentHandle property to determine if the tangent handle has already been activated. If this method is called for a handle that already exists, nothing changes and the existing sketch line that acts as the tangent handle is returned. The getTangentHandle method can be used to determine if the handle has already been activated. To deactivate a sketch handle you can delete the sketch line. |
| [addFitPoint](SketchFittedSpline_addFitPoint.md) | Creates a new fit point at the specified parameter value. |
| [breakCurve](SketchFittedSpline_breakCurve.md) | Breaks a curve into two or three pieces by finding intersections of this curve with all other curves in the sketch and splitting this curve at the nearest intersections to a specified point on the curve. |
| [classType](SketchFittedSpline_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](SketchFittedSpline_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](SketchFittedSpline_deleteMe.md) | Deletes the entity from the sketch. |
| [extend](SketchFittedSpline_extend.md) | Extend a curve by specifying a point that determines the end of the curve to extend |
| [getCurvatureHandle](SketchFittedSpline_getCurvatureHandle.md) | Returns the sketch arc that acts as the handle to control the curvature at the specified fit point. Returns null in the case where the curvature handle has not been activated at that sketch point. Deleting the returned arc will deactivate the curvature handle. Use the activateCurvatureHandle method to activate the curvature handle. |
| [getTangentHandle](SketchFittedSpline_getTangentHandle.md) | Returns the sketch line that acts as the handle to control the tangency at the specified fit point. Returns null in the case where the tangent handle has not been activated at that sketch point. Deleting the returned line will deactivate the tangent handle. Use the activateTangentHandle method to activate the tangent handle. |
| [intersections](SketchFittedSpline_intersections.md) | Get the curves that intersect this curve along with the intersection points (Point3D) |
| [split](SketchFittedSpline_split.md) | Split a curve at a position specified along the curve |
| [trim](SketchFittedSpline_trim.md) | Trim a curve by specifying a point that determines the segment of the curve to trim away |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](SketchFittedSpline_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](SketchFittedSpline_attributes.md) | Returns the collection of attributes associated with this face. |
| [boundingBox](SketchFittedSpline_boundingBox.md) | Returns the bounding box of the entity in sketch space. |
| [endSketchPoint](SketchFittedSpline_endSketchPoint.md) | Returns the sketch point that defines the ending position of the spline. Editing the position of this sketch point will result in editing the spline. |
| [entityToken](SketchFittedSpline_entityToken.md) | Returns a token for the SketchEntity object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same sketch entity. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [fitPoints](SketchFittedSpline_fitPoints.md) | Returns the set of sketch points that the spline fits through. The points include the start and end points and are returned in the same order as the spline fits through them where the first point in the list is the start point and the last point is the end point. Editing the position of these sketch points will result in editing the spline. |
| [geometricConstraints](SketchFittedSpline_geometricConstraints.md) | Returns the sketch constraints that are attached to this curve. |
| [geometry](SketchFittedSpline_geometry.md) | Returns the transient geometry of the curve which provides geometric information about the curve. The returned geometry is always in sketch space. |
| [is2D](SketchFittedSpline_is2D.md) | Indicates if this curve lies entirely on the sketch x-y plane. |
| [isClosed](SketchFittedSpline_isClosed.md) | Gets and sets if this spline is closed. A closed spline is also periodic. This property can return false even in the case where the spline is physically closed. It's possible that the start and end points of a spline can be the same point but the curve is still not considered closed. This can happen when the start and end points of an open curve are merged. The curve is physically closed but is not periodic and can have a discontinuity at the joint. Setting it to closed will cause it to be periodic and to always remain closed even as fit points are deleted. |
| [isConstruction](SketchFittedSpline_isConstruction.md) | Gets and sets whether this curve is construction geometry. |
| [isDeletable](SketchFittedSpline_isDeletable.md) | Indicates if this sketch entity can be deleted. There are cases, especially with sketch points where another entity is dependent on an entity so deleting it is not allowed. For example, you can't delete the center point of circle by itself but deleting the circle will delete the point. The same is true for the end points of a line. |
| [isFixed](SketchFittedSpline_isFixed.md) | Indicates if this geometry is "fixed". |
| [isFullyConstrained](SketchFittedSpline_isFullyConstrained.md) | Indicates if this sketch entity is fully constrained. |
| [isLinked](SketchFittedSpline_isLinked.md) | Indicates if this sketch entity was created by a projection, inclusion, or driven by an API script. If this returns true, then the entity is presented to the user as not editable and with a 'break link' command available. |
| [isReference](SketchFittedSpline_isReference.md) | Indicates if this geometry is a reference. Changing this property from true to false removes the reference. This property can not be set to true if it is already false. |
| [isValid](SketchFittedSpline_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](SketchFittedSpline_isVisible.md) | When a sketch is created, geometry is sometimes automatically added to the sketch. For example a sketch point that references the origin point is always included and if a face was selected to create the sketch on, geometry from the face is also included. This automatically created geometry behaves in a special way in that it is invisible but is available for selection and it also participates in profile calculations. It's not possible to make them visible but they can be deleted and they can be used for any other standard sketch operation. |
| [length](SketchFittedSpline_length.md) | Returns the length of the curve in centimeters. |
| [nativeObject](SketchFittedSpline_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](SketchFittedSpline_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSketch](SketchFittedSpline_parentSketch.md) | Returns the parent sketch. |
| [referencedEntity](SketchFittedSpline_referencedEntity.md) | Returns the referenced entity in the case where IsReference is true. However, this property can also return null when IsReference is true in the case where the reference is not parametric. |
| [sketchDimensions](SketchFittedSpline_sketchDimensions.md) | Returns the sketch dimensions that are attached to this curve. |
| [startSketchPoint](SketchFittedSpline_startSketchPoint.md) | Returns the sketch point that defines the starting position of the spline. Editing the position of this sketch point will result in editing the spline. |
| [worldGeometry](SketchFittedSpline_worldGeometry.md) | Returns an NurbsCurve3D object which provides geometric information in world space. The returned geometry takes into account the assembly context and the position of the sketch in it's parent component, which means the geometry will be returned in the root component space. |

## Accessed From

[SketchFittedSpline.createForAssemblyContext](SketchFittedSpline_createForAssemblyContext.md), [SketchFittedSpline.nativeObject](SketchFittedSpline_nativeObject.md), [SketchFittedSplines.add](SketchFittedSplines_add.md), [SketchFittedSplines.addByNurbsCurve](SketchFittedSplines_addByNurbsCurve.md), [SketchFittedSplines.item](SketchFittedSplines_item.md)

## Samples

| Name | Description |
|----|----|
| [Sketch spline through points creation and relative functions API Sample](SketchSplineThroughPoints_Sample.md) | Create a sketch spline with points and use some operations for spline tangent handle & curvature handle. |

## Version

Introduced in version August 2014  

