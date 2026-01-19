# DataFile.publicLink Property

Parent Object: [DataFile](DataFile.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Returns a short URL of this data file which can be shared with others.

## Remarks

This method has been retired and replaced by the functionality on the SharedLink object which can be obtained using the DataFile.sharedLink property. The behavior of this property has changed so it can return an empty string if a public link has not been generated.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.publicLink
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2019  
Retired in version May 2024  

