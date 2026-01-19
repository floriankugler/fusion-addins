# ConfigurationColumns.addFeatureAspectColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Creates a new column to control an aspect of a feature that supports being configured.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addFeatureAspectColumn(feature, aspectType)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationFeatureAspectColumn](ConfigurationFeatureAspectColumn.md) | Retruns the created ConfigurationFeatureAspectColumn or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| feature | [Base](Base.md) | The feature to be configured. The term "feature" is used broadly and includes ThreadFeature, HoleFeature that is tapped, Joint, and AsBuiltJoint objects. The existing column is returned if a feature aspect column already exists for the feature and aspect type. |
| aspectType | [ConfigurationFeatureAspectTypes](ConfigurationFeatureAspectTypes.md) | The aspect type to create a column for. The type specified must be a valid type for the specified feature; otherwise, this will fail with an error. |

## Version

Introduced in version September 2024  

