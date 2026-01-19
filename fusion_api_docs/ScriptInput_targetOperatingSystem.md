# ScriptInput.targetOperatingSystem Property

Parent Object: [ScriptInput](ScriptInput.md)  

## Description

Specifies the operating systems this script or add-in will be displayed in the "Scripts and Add-Ins" dialog and where it will be automatically run on startup, if that option is specified. Defaults to WindowsAndMacOperatingSystem

## Syntax

"scriptInput_var" is a variable referencing a ScriptInput object.  

```python
# Get the value of the property.
propertyValue = scriptInput_var.targetOperatingSystem

# Set the value of the property.
scriptInput_var.targetOperatingSystem = propertyValue
```

## Property Value

This is a read/write property whose value is an [OperatingSystems](OperatingSystems.md).

## Version

Introduced in version October 2023  

