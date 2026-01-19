# DataFile.isReadOnly Property

Parent Object: [DataFile](DataFile.md)  

## Description

Gets if this file is currently read-only or not. A file can be read-only for various reasons. For example, if you are running with a "Fusion for Personal Use license" and have not designate the file to be editable or if someone else is editing the file.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.isReadOnly
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version July 2021  

