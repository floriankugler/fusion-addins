# SectionAnalyses Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to any section analyses results in the design and supports the ability to create new sections.

## Methods

| Name | Description |
|----|----|
| [add](SectionAnalyses_add.md) | Creates a new Section Analysis. |
| [classType](SectionAnalyses_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](SectionAnalyses_createInput.md) | Creates a new SectionAnalysisInput object to use when creating a new Section Analysis. A SectionAnalysisInput object is the API equivalent of the command dialog that contains the inputs to create a section analysis. Use this object to define the settings you need and then pass this into the add method to create the section analysis. |
| [item](SectionAnalyses_item.md) | A method that returns the specified SectionAnalysis object using an index into the collection. |
| [itemByName](SectionAnalyses_itemByName.md) | A method that returns the specified SectionAnalysis object using the name of the analysis as displayed in the browser. |

## Properties

| Name | Description |
| --- | --- |
| [count](SectionAnalyses_count.md) | Returns the number of SectionAnalysis objects in the collection. |
| [isValid](SectionAnalyses_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SectionAnalyses_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Analyses.sectionAnalyses](Analyses_sectionAnalyses.md)

## Version

Introduced in version January 2023  

