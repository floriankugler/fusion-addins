# DataObjectFuture.dataObject Property

Parent Object: [DataObjectFuture](DataObjectFuture.md)  

## Description

Returns the DataObject when the data has become available, (state returns FinishedFutureState). Returns null if the operation is still running or has failed.

## Syntax

"dataObjectFuture_var" is a variable referencing a DataObjectFuture object.  

```python
# Get the value of the property.
propertyValue = dataObjectFuture_var.dataObject
```

## Property Value

This is a read only property whose value is a [DataObject](DataObject.md).

## Version

Introduced in version September 2024  

