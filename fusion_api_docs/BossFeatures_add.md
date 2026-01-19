# BossFeatures.add Method

Parent Object: [BossFeatures](BossFeatures.md)  

## Description

Creates a new boss feature (or more boss features) based on the information provided by a BossFeatureInput object. To create a new boss or boss connection, use createInput function to define a new input object for the type of boss feature you want to create. Use the methods and properties on the input object to define any additional inputs. Once the information is defined on the input object, you can pass it to the Add method to create the boss feature or boss connection.

## Syntax

"bossFeatures_var" is a variable referencing a [BossFeatures](BossFeatures.md) object.

```python
returnValue = bossFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [BossFeature](BossFeature.md)\[\] | Returns the newly created BossFeature objects or empty vector/list if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [BossFeatureInput](BossFeatureInput.md) | The BossFeatureInput object that defines the boss or boss connection you want to create. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

