# DocumentEventArgs.isOperationCancelled Property

Parent Object: [DocumentEventArgs](DocumentEventArgs.md)  

## Description

Gets and sets if the operation for this event is to be canceled. The description of the reason for canceling the operation can be set with the cancelReason property. This is only supported for the documentSaving event.

## Syntax

"documentEventArgs_var" is a variable referencing a DocumentEventArgs object.  

```python
# Get the value of the property.
propertyValue = documentEventArgs_var.isOperationCancelled

# Set the value of the property.
documentEventArgs_var.isOperationCancelled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

