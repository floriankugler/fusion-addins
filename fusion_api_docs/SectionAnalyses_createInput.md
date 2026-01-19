# SectionAnalyses.createInput Method

Parent Object: [SectionAnalyses](SectionAnalyses.md)  

## Description

Creates a new SectionAnalysisInput object to use when creating a new Section Analysis. A SectionAnalysisInput object is the API equivalent of the command dialog that contains the inputs to create a section analysis. Use this object to define the settings you need and then pass this into the add method to create the section analysis.

## Syntax

"sectionAnalyses_var" is a variable referencing a [SectionAnalyses](SectionAnalyses.md) object.

```python
returnValue = sectionAnalyses_var.createInput(cutPlaneEntity, distance)
```

## Return Value

| Type | Description |
|----|----|
| [SectionAnalysisInput](SectionAnalysisInput.md) | Returns a SectionAnalysisInput object if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| cutPlaneEntity | [Base](Base.md) | The planar entity used to define the cut plane and can be either a planar BRepFace or a ConstructionPlane object. |
| distance | double | The offset distance of the section from the cut plane. A positive value will offset in the positive normal direction of the cut plane entity. The value is in centimeters. This value is used to create a transformation matrix that defines the specified offset. |

## Version

Introduced in version April 2023  

