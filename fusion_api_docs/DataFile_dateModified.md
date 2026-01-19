# DataFile.dateModified Property

Parent Object: [DataFile](DataFile.md)  

## Description

Returns the date when this data file was modified. Most changes to a file result in a new version which means a new DataFile is created and will have a new creation date. There are a few changes, like rename, that modify a DataFile without creating a new version and the date of that change is returned by this property.  

The date is returned as UNIX epoch time, which is the number of seconds since January 1, 1970 (midnight UTC/GMT). In Python you can import the standard time module to work with UNIX epoch time. In C++ you can use functions in time.h and std::chrono to work with UNIX epoch time.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.dateModified
```

## Property Value

This is a read only property whose value is a uinteger.

## Version

Introduced in version July 2023  

