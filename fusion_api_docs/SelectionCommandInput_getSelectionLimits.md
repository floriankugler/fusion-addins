# SelectionCommandInput.getSelectionLimits Method

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Get the limits currently defined for this input.

## Syntax

"selectionCommandInput_var" is a variable referencing a [SelectionCommandInput](SelectionCommandInput.md) object.  

```python
(returnValue, minimum, maximum) = selectionCommandInput_var.getSelectionLimits()
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if the selection limits were successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| minimum | uinteger | The minimum number of selections required. A value of zero means that there is no minimum limit. |
| maximum | uinteger | The maximum number of selections required. A value of zero means that there is no maximum limit. |

## Version

Introduced in version August 2014  

