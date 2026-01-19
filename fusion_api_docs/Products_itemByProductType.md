# Products.itemByProductType Method

Parent Object: [Products](Products.md)  

## Description

Returns the specified product, if it exists within this document.

## Syntax

"products_var" is a variable referencing a [Products](Products.md) object.

```python
returnValue = products_var.itemByProductType(productType)
```

## Return Value

| Type | Description |
|----|----|
| [Product](Product.md) | Returns the specified item or null if the specified productType does not exist within this document. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| productType | string | The product type string. For example, to get the product that represents the design data you use "DesignProductType" or to get the product that represent the CAM data you use "CAMProductType". A complete list of available products can be obtained by using the Application.supportedProductTypes property. |

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version June 2015  

