# ConstructionAxisInput Object

Derived from: [Base](Base.md) Object  

## Description

A ConstructionAxisInput is a throwaway object used to create a ConstructionAxis The usage pattern is: a. create a ConstructionAxisInput (ConstructionAxes.CreateInput) b. call one of the member functions to specify how the ConstructionAxis is created c. create the ConstructionAxis (call ConstructionAxes.Add) d. stop referencing the ConstructionAxisInput (so it gets deleted).

## Methods

| Name | Description |
| --- | --- |
| [classType](ConstructionAxisInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setByCircularFace](ConstructionAxisInput_setByCircularFace.md) | This input method is for creating an axis coincident with the axis of a cylindrical, conical or torus face. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component. |
| [setByEdge](ConstructionAxisInput_setByEdge.md) | This input method is for creating a construction axis from a specified linear/circular edge or sketch curve. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component. |
| [setByLine](ConstructionAxisInput_setByLine.md) | This input method is for creating a non-parametric construction axis whose position in space is defined by an InfiniteLine3D object. This method of defining a construction axis is only valid when working in the direct modeling mode. This is not valid when working in the parametric modeling mode and will fail. |
| [setByNormalToFaceAtPoint](ConstructionAxisInput_setByNormalToFaceAtPoint.md) | This input method if for creating a construction axis normal to a specified face or sketch profile and that passes through a specified point. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component. |
| [setByPerpendicularAtPoint](ConstructionAxisInput_setByPerpendicularAtPoint.md) | This input method is for creating an axis that is normal to a face at a specified point. |
| [setByTwoPlanes](ConstructionAxisInput_setByTwoPlanes.md) | This input method is for creating a construction axis coincident with the intersection of two planes or planar faces. This will fail if the two planes are parallel. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component. |
| [setByTwoPoints](ConstructionAxisInput_setByTwoPoints.md) | This input method is for creating a construction axis that passes through the two points (work points, sketch points or vertices). This will fail if the two points are coincident. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component. |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](ConstructionAxisInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the ConstructionAxis is created based on geometry (e.g. a straight edge) in another component AND (the ConstructionAxis) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [isValid](ConstructionAxisInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ConstructionAxisInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseOrFormFeature](ConstructionAxisInput_targetBaseOrFormFeature.md) | When creating a construction axis that is owned by a base or form feature, set this property to the base or form feature you want to associate the new construction plane with. By default, this is null, meaning it will not be associated with a base or form feature. Because of a current limitation, if you want to create a construction axis associated with a base or form feature, you must set this property AND call the startEdit method of the base or form feature, create the feature, and then call the finishEdit method of the base or form feature. The base or form feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[ConstructionAxes.createInput](ConstructionAxes_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

