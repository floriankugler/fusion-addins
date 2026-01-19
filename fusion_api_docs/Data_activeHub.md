# Data.activeHub Property

Parent Object: [Data](Data.md)  

## Description

Gets the active DataHub.

## Remarks

Setting the active hub is not supported within any of the Command related events. When a command is running, a transaction is open, and changing the active hub cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"data_var" is a variable referencing a Data object.  

```python
# Get the value of the property.
propertyValue = data_var.activeHub

# Set the value of the property.
data_var.activeHub = propertyValue
```

## Property Value

This is a read/write property whose value is a [DataHub](DataHub.md).

## Version

Introduced in version September 2016  

