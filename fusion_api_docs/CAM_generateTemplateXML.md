# CAM.generateTemplateXML Method

Parent Object: [CAM](CAM.md)  

## Description

Generates a template for the specified Operations, Setups, or Folders and returns the template as an XML string.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.generateTemplateXML(operations)
```

## Return Value

| Type   | Description                           |
|--------|---------------------------------------|
| string | Returns the template XML as a string. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operations | [Base](Base.md) | An Operation, Setup or Folder object from which to generate the template. You can also specify a collection of any combination of these object types. |

## Version

Introduced in version April 2023  

