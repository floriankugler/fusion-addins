# CAMExportOptions.error Property

Parent Object: [CAMExportOptions](CAMExportOptions.md)  

## Description

Gets the last encountered error message. When the CAMExportManager's executeWithExportFuture() method is used, this method only returns errors encoutered when setting up the export. Errors thrown afterwards can be retrieved via the CAMExportFuture object. When the CAMExportManager's execute() method is used, any error can be retrieved using this property.

## Syntax

"cAMExportOptions_var" is a variable referencing a CAMExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAMExportOptions_var.error
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2023  

