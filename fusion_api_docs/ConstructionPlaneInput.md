# ConstructionPlaneInput Object

Derived from: [Base](Base.md) Object  

## Description

A ConstructionPlaneInput is a throwaway object used to create a ConstructionPlane The usage pattern is: a. create a ConstructionPlaneInput (ConstructionPlanes.CreateInput) b. call one of the member functions to specify how the ConstructionPlane is created c. create the ConstructionPlane (call ConstructionPlanes.Add) d. stop referencing the ConstructionPlaneInput (so it gets deleted).

## Methods

| Name | Description |
| --- | --- |
| [classType](ConstructionPlaneInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setByAngle](ConstructionPlaneInput_setByAngle.md) | This input method is for creating a construction plane through an edge, axis or line at a specified angle. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByDistanceOnPath](ConstructionPlaneInput_setByDistanceOnPath.md) | This input method is for creating a construction plane normal to, and at specified distance along, a path defined by an edge or sketch profile. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByOffset](ConstructionPlaneInput_setByOffset.md) | This input method is for creating a construction plane that is offset from a planar face or construction plane at a specified distance. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByOffsetThroughPoint](ConstructionPlaneInput_setByOffsetThroughPoint.md) | Defines a construction plane that is offset from a planar face or construction plane and whose offset distance is defined by a vertex, sketch point, or construction point where the plane passes through the point. |
| [setByPlane](ConstructionPlaneInput_setByPlane.md) | This input method is for creating a non-parametric construction plane positioned in space as defined by the input Plane object. This method of defining a construction plane is only valid when working in the direct modeling mode. This is not valid when working in the parametric modeling mode and will fail. |
| [setByTangent](ConstructionPlaneInput_setByTangent.md) | This input method is for creating a construction plane tangent to a cylindrical or conical face at a specified point. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByTangentAtPoint](ConstructionPlaneInput_setByTangentAtPoint.md) | This input method is for creating a construction plane tangent to a face and aligned to a point. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByThreePoints](ConstructionPlaneInput_setByThreePoints.md) | This input method is for creating a construction plane through three points that define a triangle. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByTwoEdges](ConstructionPlaneInput_setByTwoEdges.md) | This input method is for creating a construction plane that passes through two coplanar linear entities or axes. Defines a plane by specifying two coplanar linear entities. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |
| [setByTwoPlanes](ConstructionPlaneInput_setByTwoPlanes.md) | This input method is for creating a construction plane at the midpoint between two planar faces or construction planes. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component. |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](ConstructionPlaneInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the ConstructionPlane is created based on geometry (e.g. a planarEntity) in another component AND (the ConstructionPlane) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [isValid](ConstructionPlaneInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionPlaneInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseOrFormFeature](ConstructionPlaneInput_targetBaseOrFormFeature.md) | When creating a construction plane that is owned by a base or form feature, set this property to the base or form feature you want to associate the new construction plane with. By default, this is null, meaning it will not be associated with a base or form feature. Because of a current limitation, if you want to create a construction plane associated with a base or form feature, you must set this property AND call the startEdit method of the base or form feature, create the feature, and then call the finishEdit method of the base or form feature. The base or form feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[ConstructionPlanes.createInput](ConstructionPlanes_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2014  

