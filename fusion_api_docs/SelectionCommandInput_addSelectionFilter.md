# SelectionCommandInput.addSelectionFilter Method

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Adds an additional filter to the existing filter list.

## Syntax

"selectionCommandInput_var" is a variable referencing a [SelectionCommandInput](SelectionCommandInput.md) object.

```python
returnValue = selectionCommandInput_var.addSelectionFilter(filter)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if the filter was added successfully. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filter | string | The name of a selection filter to add. The valid list of selection filters can be found here: [Selection Filters](SelectionFilters_UM.md). |

## Version

Introduced in version August 2014  

