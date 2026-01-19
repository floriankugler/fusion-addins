# PathPatternFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a path pattern feature.

## Methods

| Name | Description |
|----|----|
| [classType](PathPatternFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [distance](PathPatternFeatureInput_distance.md) | Gets and sets the distance. |
| [inputEntities](PathPatternFeatureInput_inputEntities.md) | Gets and sets the input entities. The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. |
| [isFlipDirection](PathPatternFeatureInput_isFlipDirection.md) | Gets and sets if flip the direction from start point. |
| [isOrientationAlongPath](PathPatternFeatureInput_isOrientationAlongPath.md) | Gets and sets if the orientation is along path. If false, the orientation is identical. |
| [isSymmetric](PathPatternFeatureInput_isSymmetric.md) | Gets and sets if the pattern is in one direction or symmetric. |
| [isValid](PathPatternFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PathPatternFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [path](PathPatternFeatureInput_path.md) | Gets and sets the path to create the pattern on path. |
| [patternComputeOption](PathPatternFeatureInput_patternComputeOption.md) | Gets and sets the compute option when patterning features. The default value for this is AdjustPatternCompute. This property only applies when patterning features and is ignored in the direct modeling environment. |
| [patternDistanceType](PathPatternFeatureInput_patternDistanceType.md) | Gets and sets how the distance between elements is computed. |
| [quantity](PathPatternFeatureInput_quantity.md) | Gets and sets quantity of the elements. |
| [startPoint](PathPatternFeatureInput_startPoint.md) | Gets and sets the start point on the path to count the distance. It's between 0 and 1. 0 means start point of the path, 1 means end point of the path. |
| [targetBaseFeature](PathPatternFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[PathPatternFeatures.createInput](PathPatternFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Path Pattern Feature API Sample](PathPatternFeatureSample_Sample.md) | Demonstrates creating a new path pattern feature. |

## Version

Introduced in version November 2014  

