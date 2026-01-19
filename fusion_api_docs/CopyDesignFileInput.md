
Derived from: [CopyFileInput](CopyFileInput.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Input object that defines the various settings that apply when copying a design file, including whether associated drawings and/or references external components are also copied.

## Methods

| Name | Description |
|----|----|
| [classType](CopyDesignFileInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isCopyDrawings](CopyDesignFileInput_isCopyDrawings.md) | Gets and sets if any drawings associated with the design should also be copied. |
| [isCopyReferencedExternalComponents](CopyDesignFileInput_isCopyReferencedExternalComponents.md) | Gets and sets if any external reference components associated with the design should also be copied. |
| [isValid](CopyDesignFileInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CopyDesignFileInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetFolder](CopyDesignFileInput_targetFolder.md) | Gets and sets the target DataFolder where the design will be copied to. |

## Accessed From

[DataFile.createCopyDesignFileInput](DataFile_createCopyDesignFileInput.md)

## Version

Introduced in version May 2024  

