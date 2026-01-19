# ImportManager.createSVGImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates a SVGImportOptions object that is used to import SVG data into a sketch. Creation of the SVGImportOptions object does not perform the import. You must pass this object to the importToTarget or importToTarget2 methods to perform the import and provide the sketch you want to import to as the target.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createSVGImportOptions(fullFilename)
```

## Return Value

| Type | Description |
|----|----|
| [SVGImportOptions](SVGImportOptions.md) | The created SVGImportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| fullFilename | string | The full filename, including the path, of the SVG file. |

## Version

Introduced in version October 2022  

