# CAM.generateSetupSheet Method

Parent Object: [CAM](CAM.md)  

## Description

Generate the setup sheets for the specified objects

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
# Uses no optional arguments.
returnValue = cAM_var.generateSetupSheet(operations, format, folder)

# Uses optional arguments.
returnValue = cAM_var.generateSetupSheet(operations, format, folder, openDocument)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| operations | [Base](Base.md) | An Operation, Setup, Folder, or Pattern object. You can also use an ObjectCollection to specify multiple objects of any of the supported types. |
| format | [SetupSheetFormats](SetupSheetFormats.md) | The document format for the setup sheet. Valid options are HTMLFormat and ExcelFormat. Limitation: "ExcelFormat" can be used in windows OS only. |
| folder | string | The destination folder to locate the setup sheet documents in. |
| openDocument | boolean | An option to allow to open the document instantly after the generation. By default, the document is opened. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |

## Version

Introduced in version January 2016  

