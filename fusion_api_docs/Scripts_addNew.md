# Scripts.addNew Method

Parent Object: [Scripts](Scripts.md)  

## Description

Creates a new script or add-in. This uses the same internal template that's used when creating a new script or add-in using the "Scripts and Add-Ins" dialog. The provided ScriptInput object defines the information needed to create a new script or add-in.

## Syntax

"scripts_var" is a variable referencing a [Scripts](Scripts.md) object.

```python
returnValue = scripts_var.addNew(input)
```

## Return Value

| Type                 | Description                              |
|----------------------|------------------------------------------|
| [Script](Script.md) | Returns the newly created Script object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ScriptInput](ScriptInput.md) | A ScriptInput object which defines the required information to create a new script or add-in. It is created using the createNewScriptInput method. |

## Version

Introduced in version October 2023  

