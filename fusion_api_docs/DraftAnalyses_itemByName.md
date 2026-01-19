# DraftAnalyses.itemByName Method

Parent Object: [DraftAnalyses](DraftAnalyses.md)  

## Description

A method that returns the specified DraftAnalysis object using the name of the analysis as displayed in the browser.

## Syntax

"draftAnalyses_var" is a variable referencing a [DraftAnalyses](DraftAnalyses.md) object.

```python
returnValue = draftAnalyses_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [DraftAnalysis](DraftAnalysis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the DraftAnalysis object as displayed in the browser. |

## Version

Introduced in version January 2023  

