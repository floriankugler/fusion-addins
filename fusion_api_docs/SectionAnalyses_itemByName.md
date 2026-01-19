# SectionAnalyses.itemByName Method

Parent Object: [SectionAnalyses](SectionAnalyses.md)  

## Description

A method that returns the specified SectionAnalysis object using the name of the analysis as displayed in the browser.

## Syntax

"sectionAnalyses_var" is a variable referencing a [SectionAnalyses](SectionAnalyses.md) object.

```python
returnValue = sectionAnalyses_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SectionAnalysis](SectionAnalysis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the SectionAnalysis object as displayed in the browser. |

## Version

Introduced in version January 2023  

