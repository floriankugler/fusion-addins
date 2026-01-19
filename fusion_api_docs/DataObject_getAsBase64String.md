# DataObject.getAsBase64String Method

Parent Object: [DataObject](DataObject.md)  

## Description

Gets the binary data represented by the DataObject as a Base64 encoded string.

## Syntax

"dataObject_var" is a variable referencing a [DataObject](DataObject.md) object.

```python
returnValue = dataObject_var.getAsBase64String()
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the binary data represented by the DataObject as a standard Base64 encoded string. Fails with an appropriate error in the case where the data cannot be provided. |

## Version

Introduced in version September 2024  

