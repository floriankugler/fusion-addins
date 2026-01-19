# ConfigurationColumns.addThreadTypeColumns Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Creates the columns in the configuration table to control the type of thread associated with a thread feature or a tapped hole. Because configuring a thread requires several pieces of information, this method collects it all at once and creates all the corresponding feature aspect columns.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addThreadTypeColumns(threadFeature, threadColumns)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationFeatureAspectColumn](ConfigurationFeatureAspectColumn.md)\[\] | Returns an array of the columns created. They are in order of type, size, designation, and class. |

## Parameters

| Name | Type | Description |
|----|----|----|
| threadFeature | [Feature](Feature.md) | The thread or tapped hole feature whose thread will be controlled by the configuration table. |
| threadColumns | [ConfigurationThreadColumns](ConfigurationThreadColumns.md) | Enum value that indicates which columns should be created to control the thread type. You can fully define the thread type by specifying the type, size, designation, and class. Or you can leave the thread type controlled by the feature and only configure the size, designation, and class. Or you can leave the thread type and size controlled by the feature and only configure the designation and class. Or you can leave the thread type, size, and designation controlled by the feature and only configure the class. As a result, this can create and return 4, 3, 2, or 1 columns. |

## Version

Introduced in version September 2024  

