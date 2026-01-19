# Analyses.itemByName Method

Parent Object: [Analyses](Analyses.md)  

## Description

A method that returns the specified Analysis using the name of the analysis as it is displayed in the browser.

## Syntax

"analyses_var" is a variable referencing an [Analyses](Analyses.md) object.

```python
returnValue = analyses_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Analysis](Analysis.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type   | Description                                                 |
|------|--------|-------------------------------------------------------------|
| name | string | The name of the Analysis as it is displayed in the browser. |

## Version

Introduced in version January 2023  

