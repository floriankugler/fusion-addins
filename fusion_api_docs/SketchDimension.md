# SketchDimension Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the all sketch dimensions.

## Methods

| Name | Description |
|----|----|
| [classType](SketchDimension_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](SketchDimension_deleteMe.md) | Deletes this dimension. The IsDeletable property indicates if this dimension can be deleted. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](SketchDimension_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](SketchDimension_attributes.md) | Returns the collection of attributes associated with this sketch dimension. |
| [entityToken](SketchDimension_entityToken.md) | Returns a token for the SketchDimension object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same sketch dimension. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [isDeletable](SketchDimension_isDeletable.md) | Indicates if this dimension is deletable. |
| [isDriving](SketchDimension_isDriving.md) | Gets and sets if the dimension is Driving or is Driven. Setting this property to true for a given dimension may fail if the result would over constrain the sketch. Fusion does not allow over-constrained sketches. |
| [isValid](SketchDimension_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchDimension_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parameter](SketchDimension_parameter.md) | Returns the associated parameter or null if there is no associated parameter. |
| [parentSketch](SketchDimension_parentSketch.md) | Returns the parent sketch object. |
| [textPosition](SketchDimension_textPosition.md) | Gets and sets position of the dimension text. |
| [value](SketchDimension_value.md) | Gets and sets the current value of the sketch dimension. In a parametric modeling design and the isDriving property is True, this is exactly equivalent to getting the parameter associated with the dimension and editing its value. Editing this property will result in the parameter value being changed. If isDriving is False, this acts as a read-only property and attempting to set it will fail. In a direct modeling design the parameter property will return null and this property can be used to get and set the value of the dimension because in this case, there isn't an associated parameter. The value is always in internal units which means that for dimensions that represent a distance, the value is in Centimeters and for dimensions representing an angle the value is in Radians. |

## Accessed From

[AutoConstrainResult.addedDimensions](AutoConstrainResult_addedDimensions.md), [OffsetConstraint.dimension](OffsetConstraint_dimension.md), [SketchDimensionList.item](SketchDimensionList_item.md), [SketchDimensions.item](SketchDimensions_item.md)

## Derived Classes

[SketchAngularDimension](SketchAngularDimension.md), [SketchConcentricCircleDimension](SketchConcentricCircleDimension.md), [SketchDiameterDimension](SketchDiameterDimension.md), [SketchDistanceBetweenLineAndPlanarSurfaceDimension](SketchDistanceBetweenLineAndPlanarSurfaceDimension.md), [SketchDistanceBetweenPointAndSurfaceDimension](SketchDistanceBetweenPointAndSurfaceDimension.md), [SketchEllipseMajorRadiusDimension](SketchEllipseMajorRadiusDimension.md), [SketchEllipseMinorRadiusDimension](SketchEllipseMinorRadiusDimension.md), [SketchLinearDiameterDimension](SketchLinearDiameterDimension.md), [SketchLinearDimension](SketchLinearDimension.md), [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md), [SketchOffsetDimension](SketchOffsetDimension.md), [SketchRadialDimension](SketchRadialDimension.md), [SketchTangentDistanceDimension](SketchTangentDistanceDimension.md)

## Version

Introduced in version August 2014  

