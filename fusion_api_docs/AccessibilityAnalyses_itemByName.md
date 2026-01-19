# AccessibilityAnalyses.itemByName Method

Parent Object: [AccessibilityAnalyses](AccessibilityAnalyses.md)  

## Description

A method that returns the specified AccessibilityAnalysis object using the name of the analysis as displayed in the browser.

## Syntax

"accessibilityAnalyses_var" is a variable referencing an [AccessibilityAnalyses](AccessibilityAnalyses.md) object.

```python
returnValue = accessibilityAnalyses_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [AccessibilityAnalysis](AccessibilityAnalysis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the AccessibilityAnalysis object as displayed in the browser. |

## Version

Introduced in version January 2023  

