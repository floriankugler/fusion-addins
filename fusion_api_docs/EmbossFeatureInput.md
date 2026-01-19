
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This class defines the methods and properties that pertain to the definition of an emboss feature.

## Methods

| Name | Description |
|----|----|
| [classType](EmbossFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [creationOccurrence](EmbossFeatureInput_creationOccurrence.md) | In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the emboss feature is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the emboss feature) is not in the root component. The creationOccurrence is analogous to the active occurrence in the UI |
| [depth](EmbossFeatureInput_depth.md) | Gets and sets the ValueInput object that defines the depth of the emboss. A positive value results in the emboss protruding out of the body and the negative value results in the emboss going into the body. |
| [horizontalDistance](EmbossFeatureInput_horizontalDistance.md) | Gets and sets the horizontal offset distance. This defaults to zero. |
| [inputFaces](EmbossFeatureInput_inputFaces.md) | Gets and sets an array of BRepFace objects that define the faces the emboss will be performed on. By default, faces that are tangent to any of the input faces are also used. Use the isTangentChain property of the EmbossFeatureInput object to disable the use of tangent faces. If multiple inputFaces are provided, they must all be on the same body. |
| [isTangentChain](EmbossFeatureInput_isTangentChain.md) | Gets and sets whether any faces that are tangentially connected to any of the input faces will also be used. By default this property is true. |
| [isValid](EmbossFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](EmbossFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [profiles](EmbossFeatureInput_profiles.md) | Gets and sets an array of Profile objects that define the shape of the emboss. The profile argument can be Profile and SketchText objects. When multiple objects are used, all profiles and sketch texts must be co-planar. |
| [rotationAngle](EmbossFeatureInput_rotationAngle.md) | Gets and sets the rotation angle. This defaults to zero. |
| [targetBaseFeature](EmbossFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [verticalDistance](EmbossFeatureInput_verticalDistance.md) | Gets and sets the vertical offset distance. This defaults to zero. |

## Accessed From

[EmbossFeatures.createInput](EmbossFeatures_createInput.md)

## Version

Introduced in version September 2025  

