# OperationBase.operationId Property

Parent Object: [OperationBase](OperationBase.md)  

## Description

Returns the id of the operation. This id is unique as compared to the ids of all other operations in the document. This id will not change when changing the order or parent of the operation. This id will remain valid when the document is saved and reloaded.

## Syntax

"operationBase_var" is a variable referencing an OperationBase object.  

```python
# Get the value of the property.
propertyValue = operationBase_var.operationId
```

## Property Value

This is a read only property whose value is an integer.

## Version

Introduced in version May 2020  

