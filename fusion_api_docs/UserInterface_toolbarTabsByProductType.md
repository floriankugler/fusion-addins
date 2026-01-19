# UserInterface.toolbarTabsByProductType Method

Parent Object: [UserInterface](UserInterface.md)  

## Description

Gets all of the toolbar tabs associated with the specified product.

## Syntax

"userInterface_var" is a variable referencing a [UserInterface](UserInterface.md) object.

```python
returnValue = userInterface_var.toolbarTabsByProductType(productType)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTabList](ToolbarTabList.md) | Returns a list of the tabs associated with the specified product. |

## Parameters

| Name | Type | Description |
|----|----|----|
| productType | string | The name of the product that you want the associated tabs for. The full list of available products can be obtained by using the Application.supportedProductTypes property. |

## Version

Introduced in version August 2019  

