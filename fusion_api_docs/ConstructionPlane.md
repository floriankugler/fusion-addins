# ConstructionPlane Object

Derived from: [Base](Base.md) Object  

## Description

ConstructionPlane Object

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPlane_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](ConstructionPlane_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](ConstructionPlane_deleteMe.md) | Deletes the construction plane. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](ConstructionPlane_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](ConstructionPlane_attributes.md) | Returns the collection of attributes associated with this construction plane. |
| [baseFeature](ConstructionPlane_baseFeature.md) | If this construction plane is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [component](ConstructionPlane_component.md) | Returns the component this construction plane belongs to. |
| [definition](ConstructionPlane_definition.md) | Returns the ConstructionPlaneDefinition object which provides access to the information defining this ConstructionPlane. |
| [deriveFeature](ConstructionPlane_deriveFeature.md) | Returns the DeriveFeature if this construction plane is derived from another design. This property returns null if the construction plane is not derived from another design (i.e. isDerived property returns false). |
| [displayBounds](ConstructionPlane_displayBounds.md) | Gets and sets the display size of the construction plane. The bounding box defines the min and max corners of the plane as defined in the 2D space of the construction plane. |
| [entityToken](ConstructionPlane_entityToken.md) | Returns a token for the ConstructionPlane object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same construction plane. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](ConstructionPlane_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [geometry](ConstructionPlane_geometry.md) | Returns a plane that represents the position and orientation of the construction plane. This geometry is defined in the AssemblyContext of this ConstructionPlane. |
| [healthState](ConstructionPlane_healthState.md) | Returns the current health state of this construction plane. |
| [isDeletable](ConstructionPlane_isDeletable.md) | Indicates if this construction plane can be deleted. Base construction planes can not be deleted. |
| [isDerived](ConstructionPlane_isDerived.md) | Returns if this construction plane is derived from another design. If true, the construction plane cannot be deleted. You should not attempt to make any edits to the derived construction plane. Any edits made to this derived construction plane will be lost when the derive updates. |
| [isLightBulbOn](ConstructionPlane_isLightBulbOn.md) | Indicates if the light bulb (as displayed in the browser) is on. A construction plane will only be visible if it's light bulb, and that of it's containing folder and parent component/s are also on. |
| [isParametric](ConstructionPlane_isParametric.md) | Indicates if this construction plane is parametric or not. |
| [isValid](ConstructionPlane_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ConstructionPlane_isVisible.md) | Indicates if the construction plane is visible. This property is affected by the AssemblyContext of the construction plane. |
| [name](ConstructionPlane_name.md) | Returns the name of the construction plane as it is shown in the browser. |
| [nativeObject](ConstructionPlane_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](ConstructionPlane_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](ConstructionPlane_parent.md) | Returns the parent component or base feature. If both the design and the construction plane are parametric, the parent will be a component. If the design is parametric and the construction plane is not, the parent will be a base feature. If the design is not parametric the parent will be a component. |
| [timelineObject](ConstructionPlane_timelineObject.md) | Returns the timeline object associated with this construction plane. |
| [transform](ConstructionPlane_transform.md) | Returns the current position and orientation of the construction plane as a matrix. For a parametric construction plane, this property is read-only. For a construction plane in a direct modeling model or in a base feature, this is read-write and can be used to reposition the constructions plane. |

## Accessed From

[Arrange2DPlaneEnvelopeInput.plane](Arrange2DPlaneEnvelopeInput_plane.md), [Arrange3DEnvelopeDefinition.plane](Arrange3DEnvelopeDefinition_plane.md), [Arrange3DEnvelopeInput.plane](Arrange3DEnvelopeInput_plane.md), [ArrangePlaneEnvelopeDefinition.plane](ArrangePlaneEnvelopeDefinition_plane.md), [BaseFeature.constructionPlanes](BaseFeature_constructionPlanes.md), [Component.xYConstructionPlane](Component_xYConstructionPlane.md), [Component.xZConstructionPlane](Component_xZConstructionPlane.md), [Component.yZConstructionPlane](Component_yZConstructionPlane.md), [ConstructionPlane.createForAssemblyContext](ConstructionPlane_createForAssemblyContext.md), [ConstructionPlane.nativeObject](ConstructionPlane_nativeObject.md), [ConstructionPlaneAtAngleDefinition.parentConstructionPlane](ConstructionPlaneAtAngleDefinition_parentConstructionPlane.md), [ConstructionPlaneByPlaneDefinition.parentConstructionPlane](ConstructionPlaneByPlaneDefinition_parentConstructionPlane.md), [ConstructionPlaneDefinition.parentConstructionPlane](ConstructionPlaneDefinition_parentConstructionPlane.md), [ConstructionPlaneDistanceOnPathDefinition.parentConstructionPlane](ConstructionPlaneDistanceOnPathDefinition_parentConstructionPlane.md), [ConstructionPlaneMidplaneDefinition.parentConstructionPlane](ConstructionPlaneMidplaneDefinition_parentConstructionPlane.md), [ConstructionPlaneOffsetDefinition.parentConstructionPlane](ConstructionPlaneOffsetDefinition_parentConstructionPlane.md), [ConstructionPlaneOffsetThroughPointDefinition.parentConstructionPlane](ConstructionPlaneOffsetThroughPointDefinition_parentConstructionPlane.md), [ConstructionPlanes.add](ConstructionPlanes_add.md), [ConstructionPlanes.item](ConstructionPlanes_item.md), [ConstructionPlanes.itemByName](ConstructionPlanes_itemByName.md), [ConstructionPlaneTangentAtPointDefinition.parentConstructionPlane](ConstructionPlaneTangentAtPointDefinition_parentConstructionPlane.md), [ConstructionPlaneTangentDefinition.parentConstructionPlane](ConstructionPlaneTangentDefinition_parentConstructionPlane.md), [ConstructionPlaneThreePointsDefinition.parentConstructionPlane](ConstructionPlaneThreePointsDefinition_parentConstructionPlane.md), [ConstructionPlaneTwoEdgesDefinition.parentConstructionPlane](ConstructionPlaneTwoEdgesDefinition_parentConstructionPlane.md), [FlatPatternComponent.xYConstructionPlane](FlatPatternComponent_xYConstructionPlane.md), [FlatPatternComponent.xZConstructionPlane](FlatPatternComponent_xZConstructionPlane.md), [FlatPatternComponent.yZConstructionPlane](FlatPatternComponent_yZConstructionPlane.md)

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

