# PostProcessInput Object

Derived from: [Base](Base.md) Object  

## Description

This object is retired. See more information in the 'Remarks' section below.  

This class defines the properties that pertain to the settings and options required for posting a toolpath to generate a CNC file. A PostProcessInput object is a required parameter for the postProcessAll() and postProcess() methods on the CAM class.

## Methods

| Name | Description |
|----|----|
| [classType](PostProcessInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](PostProcessInput_create.md) | Creates a new PostProcessInput object to be used as an input argument by the postProcess() and postProcessAll() methods on the CAM class for posting toolpaths and generating CNC files. |

## Properties

| Name | Description |
| --- | --- |
| [areToolChangesMinimized](PostProcessInput_areToolChangesMinimized.md) | Gets and sets that operations may be reordered between setups to minimize the number of tool changes. Operations within each setup will still be executed in the programmed order. This is commonly used for tombstone machining where you have multiple setups. The default value for this property is false. |
| [isOpenInEditor](PostProcessInput_isOpenInEditor.md) | Gets and sets the option if opening the CNC file with the editor after it is created. The default value for this property is true. |
| [isValid](PostProcessInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PostProcessInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [outputFolder](PostProcessInput_outputFolder.md) | Gets and sets the path for the output folder where the .cnc files will be located. |
| [outputUnits](PostProcessInput_outputUnits.md) | Gets and sets the units option for the CNC output. Valid options are DocumentUnitsOutput, InchesOutput or MillimetersOutput |
| [postConfiguration](PostProcessInput_postConfiguration.md) | Gets and sets the full filename (including the path) for the post configuration file (.cps) |
| [postProperties](PostProcessInput_postProperties.md) | Gets and sets the list of post properties. Each property has a string name and a ValueInput object. The default value for this is an empty NamedValues. |
| [programComment](PostProcessInput_programComment.md) | Gets and sets the program comment. The default value for this property is an empty string (""). |
| [programName](PostProcessInput_programName.md) | Gets and sets the program name or number. If the post configuration specifies the parameter programNameIsInteger = true, then the program name must be a number. |

## Accessed From

[PostProcessInput.create](PostProcessInput_create.md)

## Samples

| Name | Description |
|----|----|
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  

