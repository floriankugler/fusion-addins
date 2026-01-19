# SplitFaceFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a split face feature.

## Methods

| Name | Description |
|----|----|
| [classType](SplitFaceFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAlongVectorSplitType](SplitFaceFeatureInput_setAlongVectorSplitType.md) | Sets the split type to project the splitting tool along the direction defined by the specified entity. |
| [setClosestPointSplitType](SplitFaceFeatureInput_setClosestPointSplitType.md) | Sets the split type to be a curve that defined by projecting the splitting curve to the closest point on the surface. |
| [setSurfaceIntersectionSplitType](SplitFaceFeatureInput_setSurfaceIntersectionSplitType.md) | Set the split type to be a surface to surface intersection. If the split tool is a curve it will be extruded into a surface to use in the split. If it's a surface, the surface will be used and optionally extended to fully intersect the faces to be split. |

## Properties

| Name | Description |
| --- | --- |
| [facesToSplit](SplitFaceFeatureInput_facesToSplit.md) | Gets and sets the faces to be split. The collection can contain one or more faces selected from solid and/or open bodies. |
| [isSplittingToolExtended](SplitFaceFeatureInput_isSplittingToolExtended.md) | Gets and sets whether or not the splittingTool is to be automatically extended (if possible) so as to completely intersect the facesToSplit. |
| [isValid](SplitFaceFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SplitFaceFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [splittingTool](SplitFaceFeatureInput_splittingTool.md) | Gets and sets the entity(s) that define the splitting tool(s). The splitting tool can be a single entity or an ObjectCollection containing solid and/or open bodies, construction planes, faces, or sketch curves that partially or fully intersect the faces that are being split. |
| [splitType](SplitFaceFeatureInput_splitType.md) | Returns the type of split type currently defined. |
| [targetBaseFeature](SplitFaceFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[SplitFaceFeatures.createInput](SplitFaceFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Split Face Feature API Sample](SplitFaceFeatureSample_Sample.md) | Demonstrates creating a new split face feature. |

## Version

Introduced in version June 2015  

