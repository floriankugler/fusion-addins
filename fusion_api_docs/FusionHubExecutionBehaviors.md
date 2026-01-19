# FusionHubExecutionBehaviors Enumerator

## Description

Enum to define the behavior when posting to Fusion hub.  

## Methods

| Name | Value | Description |
|----|----|----|
| FusionHubExecutionBehavior_ExportWithRelationship | 2 | Post to Fusion Hub while setting the parent document as a relationship. In the UI this will raise a "save document" dialog if the parent document's save state is not up to date. Cancelling the dialog, or if none is shown, will result in the document not being saved and the post result being exported without setting the relationship in Fusion Hub. This is the default value. |
| FusionHubExecutionBehavior_ForceExportWithRelationship | 0 | Post to Fusion Hub while setting the parent document as a relationship. In the UI this will raise a "save document" dialog if the parent document's save state is not up to date. Cancelling the dialog, or if none is shown, will result in the document not being saved and the post result not being exported. |
| FusionHubExecutionBehavior_SilentForceExportWithRelationship | 1 | Post to Fusion Hub while setting the parent document as a relationship. The document and post result are both saved in the Fusion Hub folder specified. If the document has not been saved before, then a new document named "NCProgramPostProcess_YYYYMMDD_HH:MM:SS" will be created with YYYYMMDD_HH:MM:SS being substituted with the current date time. |
| FusionHubExecutionBehavior_SkipRelationship | 3 | Post to Fusion Hub without setting the parent document as a relationship. The parent document does not need to be saved to post to Fusion Hub. |

## Version

Introduced in version July 2024  

