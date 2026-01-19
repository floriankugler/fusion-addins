# DataFile.configurationTable Property

Parent Object: [DataFile](DataFile.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

If this file is a configured design or a configuration, this property returns the associated ConfigTable object. If this is not a configured design or configuration, this property returns null.  

This property is typed as core.Base because the adsk.core library does not reference the fusion library where the ConfigurationTable object is defined. At runtime, this property will return a ConfigurationTable object.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.configurationTable
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2024  

