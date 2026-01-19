# Workspace.tooltip Property

Parent Object: [Workspace](Workspace.md)  

## Description

Gets or sets the tooltip text displayed for the workspace. This is the first line of text shown when the user hovers over the workspace name in the Fusion toolbar drop-down. This is typically the name of the workspace. This is different from the name in the that the name is a short name shown in the drop-down. The tooltip is only shown when the user hovers over the name and box appears providing more information about the workspace. For example, the name of the model workspace is "Model" and the tooltip is "Model Workspace".

## Syntax

"workspace_var" is a variable referencing a Workspace object.  

```python
# Get the value of the property.
propertyValue = workspace_var.tooltip

# Set the value of the property.
workspace_var.tooltip = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version December 2017  

