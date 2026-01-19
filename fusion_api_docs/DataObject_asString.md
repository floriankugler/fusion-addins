# DataObject.asString Method

Parent Object: [DataObject](DataObject.md)  

## Description

Gets the file as a string (UTF-8). This is convenient when the saved file contains string data. For example, if the file contains JSON data. This eliminates the need to convert the Base64 string into a standard string.

## Syntax

"dataObject_var" is a variable referencing a [DataObject](DataObject.md) object.

```python
returnValue = dataObject_var.asString()
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the data as a standard (UTF-8) string. Fails with an appropriate error in the case where the data cannot be provided. |

## Version

Introduced in version September 2024  

