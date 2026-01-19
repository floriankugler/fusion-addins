# CAM.export3MFForDefaultAdditiveSetup Method

Parent Object: [CAM](CAM.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

This method is only valid for an additive setup and exports the default additive setup's models as a 3MF file. The 3MF also contains machine and support information.

## Remarks

This property has been retired. Please use the ExportManager to export setups.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
# Uses no optional arguments.
returnValue = cAM_var.export3MFForDefaultAdditiveSetup(filepath)

# Uses optional arguments.
returnValue = cAM_var.export3MFForDefaultAdditiveSetup(filepath, addSimulationInfo, simPostProcess, simSplitSurrogates, simKeepThickeningStructure)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | True on success, false on errors or wrong setup type |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| filepath | string |  |
| addSimulationInfo | boolean | This is an optional argument whose default value is False. |
| simPostProcess | boolean | This is an optional argument whose default value is False. |
| simSplitSurrogates | boolean | This is an optional argument whose default value is False. |
| simKeepThickeningStructure | boolean | This is an optional argument whose default value is False. |

## Version

Introduced in version May 2020  
Retired in version July 2023  

