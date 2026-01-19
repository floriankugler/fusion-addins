# Occurrence.configuredDataFile Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the DataFile object that represents the specific version of the design used by this occurrence. From the DataFile you can access other version of the file, most importantly, you can access the latest version and get the top configuration table from it.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.configuredDataFile
```

## Property Value

This is a read only property whose value is a [DataFile](DataFile.md).

## Version

Introduced in version March 2024  

