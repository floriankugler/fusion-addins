# DataFile.isConfiguredDesign Property

Parent Object: [DataFile](DataFile.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets if this file represents a configured design. This is a design where a configuration table is defined. Use the configurationTable property to get the associated table.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.isConfiguredDesign
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2024  

