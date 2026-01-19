# ConstructionPoint Object

Derived from: [Base](Base.md) Object  

## Description

ConstructionPoint Object

## Methods

| Name | Description |
|----|----|
| [classType](ConstructionPoint_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](ConstructionPoint_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](ConstructionPoint_deleteMe.md) | Deletes the construction point. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](ConstructionPoint_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](ConstructionPoint_attributes.md) | Returns the collection of attributes associated with this construction point. |
| [baseFeature](ConstructionPoint_baseFeature.md) | If this construction point is associated with a base feature, this property will return that base feature. If it's not associated with a base feature, this property will return null. |
| [component](ConstructionPoint_component.md) | Returns the component this construction point belongs to. |
| [definition](ConstructionPoint_definition.md) | Returns the construction point definition object which provides access to the information defining the construction point. |
| [deriveFeature](ConstructionPoint_deriveFeature.md) | Returns the DeriveFeature if this construction point is derived from another design. This property returns null if the construction point is not derived from another design (i.e. isDerived property returns false). |
| [entityToken](ConstructionPoint_entityToken.md) | Returns a token for the ConstructionPoint object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same construction point. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](ConstructionPoint_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [geometry](ConstructionPoint_geometry.md) | Returns a Point3D object that represents the position of the construction point. The returned geometry is in the AssemblyContext of this ConstructionPoint. |
| [healthState](ConstructionPoint_healthState.md) | Returns the current health state of this construction point. |
| [isDeletable](ConstructionPoint_isDeletable.md) | Indicates if this construction point can be deleted. The base construction point cannot be deleted. |
| [isDerived](ConstructionPoint_isDerived.md) | Returns if this construction point is derived from another design. If true, the construction point cannot be deleted. You should not attempt to make any edits to the derived construction point. Any edits made to this derived construction point will be lost when the derive updates. |
| [isLightBulbOn](ConstructionPoint_isLightBulbOn.md) | Indicates if the light bulb (as displayed in the browser) is on. A construction point will only be visible if it's light bulb, and that of it's containing folder and parent component/s are also on. |
| [isParametric](ConstructionPoint_isParametric.md) | Indicates if the construction point is parametric. |
| [isValid](ConstructionPoint_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ConstructionPoint_isVisible.md) | Gets if the construction point is visible. This property is affected by the AssemblyContext of the construction point. |
| [name](ConstructionPoint_name.md) | The name of the construction point as it is displayed in the browser. |
| [nativeObject](ConstructionPoint_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](ConstructionPoint_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](ConstructionPoint_parent.md) | Returns the parent component or base feature. If both the design and the construction point are parametric, the parent will be a component. If the design is parametric and the construction point is not, the parent will be a base feature. If the design is not parametric the parent will be a component. |
| [timelineObject](ConstructionPoint_timelineObject.md) | Returns the timeline object associated with this construction point. |

## Accessed From

[BaseFeature.constructionPoints](BaseFeature_constructionPoints.md), [Component.originConstructionPoint](Component_originConstructionPoint.md), [ConstructionPoint.createForAssemblyContext](ConstructionPoint_createForAssemblyContext.md), [ConstructionPoint.nativeObject](ConstructionPoint_nativeObject.md), [ConstructionPointCenterDefinition.parentConstructionPoint](ConstructionPointCenterDefinition_parentConstructionPoint.md), [ConstructionPointDefinition.parentConstructionPoint](ConstructionPointDefinition_parentConstructionPoint.md), [ConstructionPointEdgePlaneDefinition.parentConstructionPoint](ConstructionPointEdgePlaneDefinition_parentConstructionPoint.md), [ConstructionPointPointDefinition.parentConstructionPoint](ConstructionPointPointDefinition_parentConstructionPoint.md), [ConstructionPoints.add](ConstructionPoints_add.md), [ConstructionPoints.item](ConstructionPoints_item.md), [ConstructionPoints.itemByName](ConstructionPoints_itemByName.md), [ConstructionPointThreePlanesDefinition.parentConstructionPoint](ConstructionPointThreePlanesDefinition_parentConstructionPoint.md), [ConstructionPointTwoEdgesDefinition.parentConstructionPoint](ConstructionPointTwoEdgesDefinition_parentConstructionPoint.md), [FlatPatternComponent.originConstructionPoint](FlatPatternComponent_originConstructionPoint.md)

## Samples

| Name | Description |
| --- | --- |
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version August 2014  

