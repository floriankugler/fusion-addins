# RuleFilletSettings.topologyType Property

Parent Object: [RuleFilletSettings](RuleFilletSettings.md)  

## Description

Gets and sets the topology type of the rule fillet.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"ruleFilletSettings_var" is a variable referencing a RuleFilletSettings object.  

```python
# Get the value of the property.
propertyValue = ruleFilletSettings_var.topologyType

# Set the value of the property.
ruleFilletSettings_var.topologyType = propertyValue
```

## Property Value

This is a read/write property whose value is a [RuleFilletTopologyTypes](RuleFilletTopologyTypes.md).

## Version

Introduced in version November 2025  

