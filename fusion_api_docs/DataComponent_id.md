# DataComponent.id Property

Parent Object: [DataComponent](DataComponent.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets the unique ID of this DataComponent. This ID can be used within the MFG DM API. This ID is created by the MFG DM API when the component is first saved.

## Syntax

"dataComponent_var" is a variable referencing a DataComponent object.  

```python
# Get the value of the property.
propertyValue = dataComponent_var.id
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version May 2024  

