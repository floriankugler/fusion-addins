
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

This class defines the methods and properties that pertain to the definition of a corner closure feature.

## Methods

| Name | Description |
|----|----|
| [classType](CornerClosureFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setThreeBendCornerClosure](CornerClosureFeatureInput_setThreeBendCornerClosure.md) | Sets the corner closure input with the values to be used to create a three-bend corner closure feature. Before using this method, the definitionType property should be examined to determine whether the corner is two-bend or three-bend, as this method is only applicable for three-bend corner closures. |
| [setTwoBendCornerClosure](CornerClosureFeatureInput_setTwoBendCornerClosure.md) | Sets the corner closure input with the values to be used to create a two-bend corner closure feature. Before using this method, the definitionType property should be examined to determine whether the corner is two-bend or three-bend, as this method is only applicable for two-bend corner closures. |

## Properties

| Name | Description |
| --- | --- |
| [definitionType](CornerClosureFeatureInput_definitionType.md) | Gets the type of corner closure defined. |
| [dominantEdge](CornerClosureFeatureInput_dominantEdge.md) | Gets and sets the dominant edge for the corner closure After setting the edge, the definitionType property should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |
| [isValid](CornerClosureFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CornerClosureFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [submissiveEdge](CornerClosureFeatureInput_submissiveEdge.md) | Gets and sets the submissive edge for the corner closure After setting the edge, the definitionType property should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |

## Accessed From

[CornerClosureFeatures.createInput](CornerClosureFeatures_createInput.md)

## Version

Introduced in version January 2026  

