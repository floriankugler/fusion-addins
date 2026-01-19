# RectangularPatternFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a rectangular pattern feature.

## Methods

| Name | Description |
|----|----|
| [classType](RectangularPatternFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setDirectionTwo](RectangularPatternFeatureInput_setDirectionTwo.md) | Sets all of the input required to define the pattern in the second direction. |

## Properties

| Name | Description |
| --- | --- |
| [directionOne](RectangularPatternFeatureInput_directionOne.md) | Returns a Vector3D indicating the positive direction of direction one. |
| [directionOneEntity](RectangularPatternFeatureInput_directionOneEntity.md) | Gets and sets the first direction entity. This can be a linear edge, construction axis, sketch line or rectangular pattern feature. If a rectangular pattern feature is set, the directionOneEntity and directionTwoEntity properties return the same rectangular pattern feature. |
| [directionTwo](RectangularPatternFeatureInput_directionTwo.md) | Returns a Vector3D indicating the positive direction of direction two. |
| [directionTwoEntity](RectangularPatternFeatureInput_directionTwoEntity.md) | Gets and sets the second direction entity. This can be a linear edge, construction axis, sketch line or rectangular pattern feature. If a rectangular pattern feature is set, the directionOneEntity and directionTwoEntity properties return the same rectangular pattern feature. |
| [distanceOne](RectangularPatternFeatureInput_distanceOne.md) | Gets and sets the distance in the first direction. |
| [distanceTwo](RectangularPatternFeatureInput_distanceTwo.md) | Gets and sets the distance in the second direction. |
| [inputEntities](RectangularPatternFeatureInput_inputEntities.md) | Gets and sets the input entities. The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. |
| [isSymmetricInDirectionOne](RectangularPatternFeatureInput_isSymmetricInDirectionOne.md) | Gets and sets if the pattern in direction one is in one direction or symmetric. |
| [isSymmetricInDirectionTwo](RectangularPatternFeatureInput_isSymmetricInDirectionTwo.md) | Gets and sets if the pattern in direction two is in one direction or symmetric. |
| [isValid](RectangularPatternFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RectangularPatternFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [patternComputeOption](RectangularPatternFeatureInput_patternComputeOption.md) | Gets and sets the compute option when patterning features. The default value for this is AdjustPatternCompute. This property only applies when patterning features and is ignored in the direct modeling environment. |
| [patternDistanceType](RectangularPatternFeatureInput_patternDistanceType.md) | Gets and sets how the distance between elements is computed. |
| [quantityOne](RectangularPatternFeatureInput_quantityOne.md) | Gets and sets the number of instances in the first direction. |
| [quantityTwo](RectangularPatternFeatureInput_quantityTwo.md) | Gets and sets the number of instances in the second direction. |
| [targetBaseFeature](RectangularPatternFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |

## Accessed From

[RectangularPatternFeatures.createInput](RectangularPatternFeatures_createInput.md)

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [RectangularPattern Feature](RectangularPatternFeatureSample_Sample.md) | Demonstrates creating a new rectangular pattern feature. |

## Version

Introduced in version November 2014  

