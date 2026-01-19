# UserInterface.workspacesByProductType Method

Parent Object: [UserInterface](UserInterface.md)  

## Description

Returns all of the workspaces associated with the specified product.

## Syntax

"userInterface_var" is a variable referencing a [UserInterface](UserInterface.md) object.

```python
returnValue = userInterface_var.workspacesByProductType(productType)
```

## Return Value

| Type | Description |
|----|----|
| [WorkspaceList](WorkspaceList.md) | Returns a list of the associated work spaces. |

## Parameters

| Name | Type | Description |
|----|----|----|
| productType | string | The name of the product that you want the associated workspaces for. The full list of available products can be obtained by using the Application.supportedProductTypes property. |

## Version

Introduced in version June 2015  

