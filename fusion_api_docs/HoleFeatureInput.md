# HoleFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a hole feature.

## Methods

| Name | Description |
| --- | --- |
| [classType](HoleFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAllExtent](HoleFeatureInput_setAllExtent.md) | Defines the extent of the hole to be through-all. The direction can be either positive, negative. |
| [setDistanceExtent](HoleFeatureInput_setDistanceExtent.md) | Defines the depth of the hole using a specified distance. |
| [setLengthAndOffset](HoleFeatureInput_setLengthAndOffset.md) | Sets the length and offset of the thread of a tapped hole. This method is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise calling this method will fail. By default the isFullLength property is true which means the thread is the full length of the hole and there is no offset. Calling this method will have the side effect of setting the isFullLength property to false. |
| [setOneSideToExtent](HoleFeatureInput_setOneSideToExtent.md) | Sets the extent of the hole to be from the sketch plane to the specified "to" face. |
| [setPositionAtCenter](HoleFeatureInput_setPositionAtCenter.md) | Defines the position of the hole at the center of a circular or elliptical edge of the face. |
| [setPositionByPlaneAndOffsets](HoleFeatureInput_setPositionByPlaneAndOffsets.md) | Defines the orientation of the hole using a planar face or construction plane. The position of the hole is defined by the distance from one or two edges. |
| [setPositionByPoint](HoleFeatureInput_setPositionByPoint.md) | Defines the position of a the hole using a point. The point can be a vertex on the face or it can be a Point3D object to define any location on the face. If a Point3D object is provided it will be projected onto the plane along the planes normal. The orientation of the hole is defined by the planar face or construction plane. If a vertex is used, the position of the hole is associative to that vertex. If a Point3D object is used the position of the hole is not associative. |
| [setPositionBySketchPoint](HoleFeatureInput_setPositionBySketchPoint.md) | Defines the position and orientation of the hole using a sketch point. |
| [setPositionBySketchPoints](HoleFeatureInput_setPositionBySketchPoints.md) | Defines the position and orientation of the hole using a set of sketch points. |
| [setPositionOnEdge](HoleFeatureInput_setPositionOnEdge.md) | Defines the position and orientation of the hole to be on the start, end or center of an edge. |
| [setToClearanceHole](HoleFeatureInput_setToClearanceHole.md) | Sets the hole to be a clearance hole of the size specified by the ClearanceHoleInfo object. |
| [setToSimpleHole](HoleFeatureInput_setToSimpleHole.md) | This property sets the hole's tap to be "simple", which means that it will not have any tap and will be a simple hole. When a new input is created, it defaults to being a simple hole. |
| [setToTappedHole](HoleFeatureInput_setToTappedHole.md) | Sets the hole to be a straight or tapered tapped hole of the size specified by the ThreadInfo object. |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](HoleFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the Hole is created based on geometry (e.g. a face or point) in another component AND (the Hole) is not in the root component. The CreationOccurrence is analogous to the active occurrence in the UI A value of null indicates that everything is in the context of a single component. |
| [holeTapType](HoleFeatureInput_holeTapType.md) | Returns the current type of tap associated with this hole. When a new HoleFeatureInput is created, this will default to SimpleHoleTapType, which means the hole will not have any tap and will be a simple hole. You can set the tap type by using one of the methods to define the specific tap desired. |
| [isDefaultDirection](HoleFeatureInput_isDefaultDirection.md) | Gets or sets if the hole goes in the default direction or is reversed. |
| [isFullLength](HoleFeatureInput_isFullLength.md) | Gets and sets if this thread is the full length of the hole. It defaults to true. This property is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise this property is ignored. The property can only be set to True, which will cause the feature to ignore the values of the threadLength and threadOffset properties. Using the setLengthAndOffset method will have the side effect of setting this property to false. |
| [isModeled](HoleFeatureInput_isModeled.md) | Gets and sets if the thread is physical or cosmetic thread. A value of true indicates a physical thread. It defaults to false. This property is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise this property is ignored. |
| [isValid](HoleFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](HoleFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [participantBodies](HoleFeatureInput_participantBodies.md) | Gets and sets the list of bodies that will participate in the hole. If this property has not been set, the default behavior is that all bodies that are intersected by the hole will participate. This property can return null in the case where the feature has not been fully defined so that possible intersecting bodies can be computed. |
| [targetBaseFeature](HoleFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [threadLength](HoleFeatureInput_threadLength.md) | Gets the thread length when the isFullLength property is False. Returns null when the isFullLength property is true. |
| [threadOffset](HoleFeatureInput_threadOffset.md) | Gets the thread offset when the isFullLength property is False. Returns null when the isFullLength property is true. |
| [tipAngle](HoleFeatureInput_tipAngle.md) | Gets the ValueInput object that defines the angle of the tip of the hole. The default is "118.0 deg" but can be modified by setting it using another Value object. |

## Accessed From

[HoleFeatures.createCounterboreInput](HoleFeatures_createCounterboreInput.md), [HoleFeatures.createCountersinkInput](HoleFeatures_createCountersinkInput.md), [HoleFeatures.createSimpleInput](HoleFeatures_createSimpleInput.md)

## Samples

| Name | Description |
|----|----|
| [Hole Feature API Sample](HoleFeatureSample_Sample.md) | Demonstrates creating a new hole feature. |

## Version

Introduced in version August 2014  

