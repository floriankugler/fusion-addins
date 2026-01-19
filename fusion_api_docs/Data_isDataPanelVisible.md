# Data.isDataPanelVisible Property

Parent Object: [Data](Data.md)  

## Description

Gets and sets if the data panel is visible within Fusion.

## Remarks

Setting if the data panel is visible is not supported within any of the Command related events. When a command is running, a transaction is open, and changing the visibility of the data panel cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"data_var" is a variable referencing a Data object.  

```python
# Get the value of the property.
propertyValue = data_var.isDataPanelVisible

# Set the value of the property.
data_var.isDataPanelVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2016  

