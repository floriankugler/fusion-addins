
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The AutoConstrainInput object is used to define the various options when adding dimension and geometric constraints to help constrain a sketch.

## Methods

| Name | Description |
|----|----|
| [classType](AutoConstrainInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [datumPoint](AutoConstrainInput_datumPoint.md) | Gets and sets an optional datum point that the dimensions will be based on. This defaults to null, which indicates there is no datum point specified. When no datum point is provided, AutoConstrain will automatically select an appropriate datum based on the sketch content and geometry. |
| [isValid](AutoConstrainInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AutoConstrainInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSketch](AutoConstrainInput_parentSketch.md) | Returns the Sketch this object is associated with and where the dimension and geometric constraints will be added when the autoConstrain method is called. This property is read-only and is set when the input object is created by the sketch's createAutoConstrainInput method. |

## Accessed From

[Sketch.createAutoConstrainInput](Sketch_createAutoConstrainInput.md)

## Version

Introduced in version January 2026  

