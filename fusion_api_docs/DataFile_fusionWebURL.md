# DataFile.fusionWebURL Property

Parent Object: [DataFile](DataFile.md)  

## Description

Returns a URL that can be used to access the Fusion Web interface for this file within a browser. The person using the URL must have an Autodesk account and have authority to access the hub this file is owned by.

You can also use this URL to directly open the file in Fusion using the Fusion protocol handler as discussed in the [Opening Files from a Web Page](OpeningFilesFromWebPage_UM.md) topic in the API user manual.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.fusionWebURL
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2024  

