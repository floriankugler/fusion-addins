
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The VolumetricSampler object which is used for controled sampling of the volumetric model.

## Methods

| Name | Description |
|----|----|
| [addSamplePoints](VolumetricSampler_addSamplePoints.md) | Appends sample points to the existing sample points to be used for sampling the volumetric model. |
| [classType](VolumetricSampler_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clearSamplePoints](VolumetricSampler_clearSamplePoints.md) | Clears the sample points that have been set for sampling the volumetric model. |
| [evaluate](VolumetricSampler_evaluate.md) | Evaluates the volumetric model at the previously set sample points for the given node and returns the results. |
| [evaluateColor](VolumetricSampler_evaluateColor.md) | Evaluates the color of the model at the previously set sample points and returns the results. |
| [evaluateDensity](VolumetricSampler_evaluateDensity.md) | Evaluates the density of the model at the previously set sample points and returns the results. This value is what is used to determine the level set of the model. |
| [evaluateLevelSet](VolumetricSampler_evaluateLevelSet.md) | Evaluates the level set function of the model at the previously set sample points and returns the results. |
| [samplePointCount](VolumetricSampler_samplePointCount.md) | Gets the number of sample points that will be used for sampling the volumetric model. |
| [setBoundingBoxSampling](VolumetricSampler_setBoundingBoxSampling.md) | Calculates and sets the sample points to be used for sampling the volumetric model for a given resolution throughout the bounding box provided. This will override any previously set sample points. |
| [setPlaneSampling](VolumetricSampler_setPlaneSampling.md) | Calculates and sets the sample points to be used for sampling the volumetric model for a given resolution, plane and primary axis. The points will be distributed in a grid pattern on the plane, starting at the plane origin and extend in the primary axis and secodary axis for the axis size arguments. The secondary axis is calculated from the cross product of the plane normal and the primary axis. This will override any previously set sample points. |
| [setSamplePoints](VolumetricSampler_setSamplePoints.md) | Sets sample points to be used for sampling the volumetric model. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](VolumetricSampler_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](VolumetricSampler_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[VolumetricModel.createSampler](VolumetricModel_createSampler.md)

## Version

Introduced in version May 2025  

