# AdditiveSetupUtility.assignPartsToBodyPreset Method

Parent Object: [AdditiveSetupUtility](AdditiveSetupUtility.md)  

## Description

Assigns an array of parts to the body preset operation corresponding to the chosen PrintSettingItem in the PrintSetting. If a part has been previously assigned to a different preset (i.e. the default preset), it will be removed from its previous owner to ensure a body can only be mapped to one preset. If the previous owner preset ends up being empty, it will be removed from the setup.

## Syntax

"additiveSetupUtility_var" is a variable referencing an [AdditiveSetupUtility](AdditiveSetupUtility.md) object.

```python
returnValue = additiveSetupUtility_var.assignPartsToBodyPreset(parts, presetName)
```

## Return Value

| Type | Description |
|----|----|
| [Operation](Operation.md) | The preset corresponding to the preset name. Returns null if the preset has been removed from the setup due to passing an empty or invalid array. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parts | Base\[\] | Parts to be assigned to a preset. The array may contain BRepBody, MeshBody or Occurrence objects. If occurrences are passed in, the preset will contain their resolved bodies or meshes. If the array is empty, the preset will be removed from the setup, but the PrintSettingItem will stay in the PrintSetting. |
| presetName | string | The name of the PrintSettingItem defined in the PrintSetting, which serves as the basis for the to be created operation. |

## Version

Introduced in version July 2024  

