# BossFeatureSideInput.setRibExtent Method

Parent Object: [BossFeatureSideInput](BossFeatureSideInput.md)  

## Description

Set rib extent type for particular rib for position point provided.

## Syntax

"bossFeatureSideInput_var" is a variable referencing a [BossFeatureSideInput](BossFeatureSideInput.md) object.

```python
returnValue = bossFeatureSideInput_var.setRibExtent(position, ribExtentTypes)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| position | [Base](Base.md) | Position point object for the rib extent types provided |
| ribExtentTypes | integer\[\] | Vector of BossRibExtentTypes for individual rib based on rib count input. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

