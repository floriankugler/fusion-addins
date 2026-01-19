# Scripts.createScriptInput Method

Parent Object: [Scripts](Scripts.md)  

## Description

Creates a new ScriptInput object. Logically, this object is equivalent to the dialog that is shown when you click the "Create" button in the "Scripts and Add-Ins" command dialog. It collects the information needed to create a new script or add-in. To create the script or add-in, call the addNew method, passing in the ScriptInput object.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.createScriptInput(name, programmingLanguage, isAddIn)
```

## Return Value

| Type | Description |
|----|----|
| [ScriptInput](ScriptInput.md) | Returns a ScriptInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the script or add-in to create. By default, it will be created in the folder specified by the "Default Path for Scripts and Add-Ins" preference, but a different path can be specified using the returned ScriptInput object. Regardless of where it is created, the name must be unique with respect to the other scripts and add-ins in that folder. If it's not unique the creation of the script or add-in will fail. |
| programmingLanguage | [ProgrammingLanguages](ProgrammingLanguages.md) | The programming language to use for the new script or add-in. |
| isAddIn | boolean | Specifies if a script or add-in is to be created. If true, an add-in is created. |

## Version

Introduced in version October 2023  

