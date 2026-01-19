# ImportManager.importToTarget2 Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Executes the import operation to import a file (of the format specified by the input ImportOptions object) into an existing component in an existing design and returns the imported objects.

## Remarks

There is currently a limitation with this method where it cannot be used within any of the Command related events.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.importToTarget2(importOptions, target)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns an ObjectCollection containing the results of whatever was created as a result of the import. null is returned in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| importOptions | [ImportOptions](ImportOptions.md) | An ImportOptions object that is created using one of the create methods on the ImportManager object. This defines the type of file and any available options supported for that file type. Supplying a DXF2DImportOptions object will result in the creation of one or more sketches (depending on the layers in the DXF file) in the target component. |
| target | [Base](Base.md) | For most import types this will be a Component. For SVGImportOptions this is the sketch you want to import the SVG data into. |

## Version

Introduced in version September 2017  

