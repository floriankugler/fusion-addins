# DataFile.dateCreated Property

Parent Object: [DataFile](DataFile.md)  

## Description

Returns the date when this data file was created as UNIX epoch time. UNIX epoch time is the number of seconds since January 1, 1970 (midnight UTC/GMT).  

In Python you can import the standard time module to work with UNIX epoch time.  

In C++ you can use functions in time.h and std::chrono to work with UNIX epoch time.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.dateCreated
```

## Property Value

This is a read only property whose value is a uinteger.

## Version

Introduced in version August 2020  

