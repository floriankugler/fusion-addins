# CAMTemplateOperationInput.toolPreset Property

Parent Object: [CAMTemplateOperationInput](CAMTemplateOperationInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Optionally specify the preset of the tool. If no preset is specified, the operation gets its default feed and speed. The Tool provides access to available presets. Use one of those presets to override the default. An invalid preset will cause a failure during the creation of the operation.

## Syntax

"cAMTemplateOperationInput_var" is a variable referencing a CAMTemplateOperationInput object.  

```python
# Get the value of the property.
propertyValue = cAMTemplateOperationInput_var.toolPreset

# Set the value of the property.
cAMTemplateOperationInput_var.toolPreset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ToolPreset](ToolPreset.md).

## Version

Introduced in version March 2025  

