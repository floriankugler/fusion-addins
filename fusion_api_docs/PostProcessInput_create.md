# PostProcessInput.create Method

Parent Object: [PostProcessInput](PostProcessInput.md)  

## Description

Creates a new PostProcessInput object to be used as an input argument by the postProcess() and postProcessAll() methods on the CAM class for posting toolpaths and generating CNC files.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.PostProcessInput.create(programName, postConfiguration, outputFolder, outputUnits)
```

## Return Value

| Type | Description |
|----|----|
| [PostProcessInput](PostProcessInput.md) | Returns the newly created PostProcessInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| programName | string | The program name or number. If the post configuration specifies the parameter programNameIsInteger = true, then the program name must be a number. |
| postConfiguration | string | The full filename (including the path) to the post configuration file (.cps) The post config file can be stored in any path but for convenience you can use the genericPostFolder or the personalPostFolder property on the CAM class to specify the path if your .cps file is stored in either of those locations. You must add a forward slash (this works for Mac or Windows) to the path defined by these folder properties before the filename (e.g. postConfiguration = cam.genericPostFolder + '/' + 'fanuc.cps') |
| outputFolder | string | The path for the existing output folder where the .cnc files will be located. This method will create the specified output folder if it does not already exist. It is not necessary to add a slash to the end of the outputFolder path. You should use forward slashes in your path definition if you want your script to run on both Mac and Windows. |
| outputUnits | [PostOutputUnitOptions](PostOutputUnitOptions.md) | The units option for the CNC output. Valid options are DocumentUnitsOutput, InchesOutput or MillimetersOutput |

## Samples

| Name | Description |
|----|----|
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  

