# PatchFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a patch feature.

## Methods

| Name | Description |
|----|----|
| [classType](PatchFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getContinuity](PatchFeatureInput_getContinuity.md) | Gets the continuity used for each edge in the boundary. |
| [setContinuity](PatchFeatureInput_setContinuity.md) | Sets the continuity to use for each edge in the boundary. The arrays for the arguments correspond to B-Rep edges in the boundary. You can use the getContinuity method to get the list of edges to know their order. This order applies to the arrays provided for the arguments. |

## Properties

| Name | Description |
| --- | --- |
| [boundaryCurve](PatchFeatureInput_boundaryCurve.md) | Gets and sets the input geometry that will be used to define the boundary. This can be a sketch profile, a single sketch curve, a single B-Rep edge, an ObjectCollection, or a Path object. If a single open sketch curve or B-Rep edge is input, Fusion will automatically find connected sketch curves or B-Rep edges to define a closed loop. If an ObjectCollection is used as input, it must be a set of curves that define a closed shape. If a Path is used as input, it must define a closed shape. |
| [continuity](PatchFeatureInput_continuity.md) | **RETIRED** Gets and sets the type of surface continuity to use when matching boundary edges to face edges. When a new PatchFeatureInput is created, this is initialized to ConnectedSurfaceContinuityType. This value is ignored when creating a patch for sketch curves. |
| [creationOccurrence](PatchFeatureInput_creationOccurrence.md) | For geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Patch feature is created based on geometry (e.g., a profile, edges, faces) in another component AND (the Patch feature) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI |
| [groupContinuity](PatchFeatureInput_groupContinuity.md) | Gets and sets the type of surface continuity to use for all edges when the isGroupEdges property is true. The continuity is used to determine how the patch connects to any B-Rep edges in the boundary. It is ignored for any sketch curves in the boundary. The property defaults to ConnectedSurfaceContinuityType. The value of this property is ignored if the isGroupEdges property is false. |
| [groupIsContinuityDirectionFlipped](PatchFeatureInput_groupIsContinuityDirectionFlipped.md) | Gets and sets the continuity direction for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to false. The value of this property is ignored if the isGroupEdges property is false. |
| [groupWeight](PatchFeatureInput_groupWeight.md) | Gets and sets the weight to use for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to 0.5. The value of this property is ignored if the isGroupEdges property is false. |
| [interiorRailsAndPoints](PatchFeatureInput_interiorRailsAndPoints.md) | Gets and sets any interior curves or points the patch should fit through. Valid entities include object collections of connected curves, paths, sketch curves, sketch points, B-Rep edges, and construction points. When getting this property, the returned ObjectCollection can contain individual edges, sketch curves, sketch points, construction points, vertices, and ObjectCollection objects that represent a group of the curves and points listed above. Can be set to null to remove any interior rails and points from the patch. |
| [isGroupEdges](PatchFeatureInput_isGroupEdges.md) | Gets and sets if the edges in the boundary curve are treated as a group, and they all use the same continuity. If this property is True (which is the default), the continuity property controls the continuity for all edges. If this property is false; the continuity is set for each edge using the setContinuity method. When this property is set to true, the continuity and weight of the first edge will be used for all edges. When set to false, each edge will initially have the same continuity and weight. This is typically set to false as a side-effect of calling the setContinuity method. |
| [isValid](PatchFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PatchFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [operation](PatchFeatureInput_operation.md) | Gets and sets the type of operation performed by the patch feature. Only 'NewBodyFeatureOperation' and 'NewComponentFeatureOperation' are valid operations for patch features. |
| [targetBaseFeature](PatchFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[PatchFeatures.createInput](PatchFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version July 2016  

