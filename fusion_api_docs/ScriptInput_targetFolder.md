# ScriptInput.targetFolder Property

Parent Object: [ScriptInput](ScriptInput.md)  

## Description

The full path to the folder where the script or add-in will be created. By default, this is an empty string which uses the default folder specified by the "Default Path for Scripts and Add-Ins" preference. Specifying a path overrides the default and will create the script or add-in in the specified location. No "Scripts" or "AddIns" sub-folder is created.

## Syntax

"scriptInput_var" is a variable referencing a ScriptInput object.  

```python
# Get the value of the property.
propertyValue = scriptInput_var.targetFolder

# Set the value of the property.
scriptInput_var.targetFolder = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version October 2023  

