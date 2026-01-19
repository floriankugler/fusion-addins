# VariableRadiusFilletEdgeSet.endRadius Property

Parent Object: [VariableRadiusFilletEdgeSet](VariableRadiusFilletEdgeSet.md)  

## Description

Returns the model parameter that controls the end radius of the fillet. You can edit the end radius by using the properties on the returned ModelParameter object.

## Syntax

"variableRadiusFilletEdgeSet_var" is a variable referencing a VariableRadiusFilletEdgeSet object.  

```python
# Get the value of the property.
propertyValue = variableRadiusFilletEdgeSet_var.endRadius
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Samples

| Name | Description |  |
| --- | --- | --- |
| [Fillet Feature Edit API Sample](FilletFeatureEditSample_Sample.md) | Demonstrates editing a fillet feature. To successfully run this sample you can use this [Version Introduced in version November 2014](../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3C/td%3E%0A%20%20%20%20%20%20%3C/tr%3E%0A%20%20%20%20%3C/Table%3E%0A%20%20%20%20%3Ch2%20class=) © Copyright 2026 Autodesk, Inc. | Comment on this page.) |

