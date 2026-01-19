# ZebraAnalyses.itemByName Method

Parent Object: [ZebraAnalyses](ZebraAnalyses.md)  

## Description

A method that returns the specified ZebraAnalysis object using the name of the analysis as it is displayed in the browser.

## Syntax

"zebraAnalyses_var" is a variable referencing a [ZebraAnalyses](ZebraAnalyses.md) object.

```python
returnValue = zebraAnalyses_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ZebraAnalysis](ZebraAnalysis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the ZebraAnalysis object as it is displayed in the browser. |

## Version

Introduced in version January 2023  

