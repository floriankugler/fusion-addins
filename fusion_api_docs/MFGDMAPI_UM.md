## Using the MFGDM API with the Fusion desktop API

[Overview](#Overview)  
[DataComponent Object](#DataComponentObject)  
[Knowing when the MDGDM Data is Available](#MFGDMDataReadyEvent)  
[Understanding modelId and componentId](#ModelIdAndComponentID)  
[Legacy PartNumber and PartDescription Desktop API](#LegacyPropertyAPI)  
[Custom Properties](#CustomProperties)  
[Samples](#SampleScripts)  

## Overview

This topic introduces recent enhancements to the Fusion Desktop API that enable interoperability with the **MFGDM GraphQL API**, Autodesk’s cloud-based service for managing and querying design data. For more details, see the documentation specific to the [MFGDM GraphQL API](https://aps.autodesk.com/en/docs/mfgdataapi/v3/developers_guide/)

Historically, most properties accessible through the Desktop API were held in memory and available locally. However, with the shift toward managing some of this data in the cloud via the MFGDM service, certain properties (*PartNumber, PartDescription*) reside in the cloud and require a different mechanism to access them efficiently and reliably.

To support this change, the Fusion Desktop API now exposes new properties (such as mfgdmModelId and timestamp) and events (such as MFGDMDataReadyEvent) that allow client applications to coordinate with the MFGDM GraphQL API. These additions make it possible to retrieve cloud-managed data in a robust and time-aware manner.

This topic will explain:

- The motivation for this change.
- How to use the new API properties and events in conjunction with the MFGDM GraphQL API.
- A complete example workflow, including how to fetch cloud-backed metadata like part numbers.

By using the MFGDM GraphQL API, you gain improved performance and flexibility when working with cloud-managed data, as you can query precisely the information you need from multiple components in a single request.

## DataComponent Object

The DataComponent object in the Fusion Desktop API has been enhanced to support interoperability with Autodesk’s MFGDM GraphQL API. This object provides a bridge between the local design representation and the underlying cloud MFG DM model. It exposes key metadata that enables clients to identify and synchronize with the correct model version in the cloud.

The DataComponent exposes properties such as mfgdmModelId (a timeless identifier) and timestamp (indicating the time at which the model data was fetched). These identifiers are essential when interacting with cloud APIs such as GraphQL.

### How to Access the DataComponent

- From the root of the design:  
  Use design.rootDataComponent to access the DataComponent associated with the top-level model.

```python
  design: adsk.fusion.Design = args.document.products.itemByProductType('DesignProductType')
  data = design.rootDataComponent
  app.log(f'root model id: {data.mfgdmModelId}, timestamp: {data.timestamp}')
  
```

- From individual occurrences: Each Occurrence object in the design may also expose its own dataComponent, allowing access to metadata for inserted subassemblies or components.

This structure ensures that clients can retrieve cloud model metadata not only for the full design but also for each part or subassembly in the hierarchy—supporting workflows like part tracking, versioning, and GraphQL queries at any level of the model tree.

### Key Properties

**mfgdmModelId**  
This property returns the unique model ID associated with the current design or the inserted component if obtained from an Occurrence. It serves as a reference for querying component properties via GraphQL APIs.

**timestamp**  
The timestamp property indicates the time at which the model data was fetched. This datetime value is useful for tracking when the model snapshot was retrieved. In scenarios where the model is fetched “at-tip” (i.e., the latest state), this value may be empty string.

These properties ensure that client working with the Fusion Desktop API can track cloud-sourced models accurately, providing consistent integration across local and remote data environments.

## Knowing when the MDGDM Data is Available

Accessing cloud-based model metadata—such as the mfgdmModelId and timestamp from the DataComponent—requires the model to be saved and successfully registered with the cloud (MFG DM). This process may take some time after saving, during which the data is not immediately available.

To ensure these values are accessed only when they are ready, the Fusion Desktop API provides a specialized event: **MFGDMDataReady**.

### Why this Event is Needed

While the standard documentOpened event indicates that a document is available in the local environment, it **does not guarantee** that the cloud metadata (MFG DM IDs) has been populated. In scenarios involving newly saved designs or first-time cloud syncs, there can be a delay between document save and metadata availability.

This delay introduces uncertainty for clients that rely on cloud model IDs (mfgdmModelId) to call MFGDM GraphQL APIs or perform downstream cloud operations. As a result, you **cannot assume** that model IDs will be immediately available for unsaved designs or even for saved designs immediately after opening.

Moreover, this event is also required after saving a design that includes newly added local components. These components are only registered in the cloud **after the save**, and their corresponding occurrence DataComponent information (including model IDs) will become available **only after the `MFGDMDataReadyEvent` fires again**.

### MFGDMDataReady Event

The MFGDMDataReady event is triggered once the MFG DM metadata—such as the model ID and timestamp—is fully initialized and ready to be accessed. This ensures a reliable point at which clients can safely retrieve the values and proceed with further processing.

This event is also essential in dynamic assembly workflows—for example, when inserting new assemblies or subassemblies into the design. In such cases, the newly inserted components also require a brief processing window for the cloud metadata to become available. The MFGDMDataReadyEvent ensures the application is notified only when those new components' model IDs are ready for use, avoiding premature access and potential errors.

By subscribing to this event, clients can reliably coordinate the timing of GraphQL API calls and other model-dependent operations in both document load and insertion scenarios.

## Understanding modelId and componentId

When working with components and assemblies in Fusion’s cloud-backed environment (MFGDM), it’s important to understand the distinction between two key identifiers: modelId and componentId. These serve different purposes and are used in different contexts, especially when querying data via GraphQL.

### modelId (also referred to as mfgdmModelId)

- The *modelId* is a **timeless, unique identifier** for a component or assembly in the MFGDM cloud environment.
- It is persistent and invariant — it does not change across different versions or states of the component.
- Think of the *modelId* as the identity of the component in the cloud world. No matter how the component evolves (changes in geometry, parameters, or metadata), its *modelId* remains constant.
- We intentionally use *modelId* in client applications to abstract away the internal cloud storage or versioning details, providing a clean and consistent way to reference a component.

### componentId

- The componentId is a **time-specific identifier** that represents the exact state (geometry, features, properties) of a component **at a particular point in time**.
- It is derived from the combination of *modelId* and a specific **timestamp**.
- This ID is useful when you need to track or compare how a component has evolved over time. For instance, a component might have a different part number in one version and another in different version — each of those versions will have the same *modelId* but a different componentId.

## Legacy PartNumber and PartDescription Desktop API

Historically, legacy APIs for PartNumber (PN) and PartDescription (PD) on the desktop side did not require a save operation to function correctly.

With the support of direct GraphQL APIs, properties can be fetched in bulk together, improving performance compared to the legacy method which will now make individual GraphQL calls. However, there is a significant change to note: these properties now require the document to be saved before they can be accessed and edited, due to their nature as cloud properties. This is a crucial adjustment as unsaved documents will not support editing these properties through scripts.

### Observation and Limitations

When the root document is not saved:  

- Root Component:  
  Legacy PN/PD set property works as it goes through the cache route and reflects after save.
- Add new internal component (unsaved):  
  Legacy PN/PD set property works as it goes through the cache route and reflects after save.
- Add new external component (unsaved):  
  Legacy PN/PD set property works as it goes through the cache route and reflects after save.

When the root document is saved already:  

- Root Component:  
  Legacy PN/PD set property works as it goes through the new GraphQL route.
- Add new internal component (unsaved):  
  ❌ Legacy PN/PD set property **fails** as it goes through the new GraphQL route and internal component doesn’t have a valid model ID.
- Add new external component (unsaved):  
  Legacy PN/PD set property works as it goes through the cache route and reflects after save.

This limitation highlights the necessity of saving the document to ensure proper functionality of cloud-integrated properties and the improvement graphql support is providing to avoid performance hits with individual fetching of properties.

It is essential for developers to understand this limitation and the transition from the legacy system to effectively leverage the new API enhancements and ensure smooth interoperability between desktop and cloud services.

## Custom Properties

#### Limitations on Creating or Editing Custom Properties

When working with the Fusion Desktop API, it is important to note that certain GraphQL API operations related to creating or editing custom properties cannot be performed. The following GraphQL operations will not work within the Fusion Desktop API:

- createPropertyDefinitionCollection
- updatePropertyDefinitionCollection
- createPropertyDefinition
- linkPropertyDefinitionCollection
- setProperties
- archivePropertyDefinition
- unlinkPropertyDefinitionCollection

This limitation arises because custom property definitions must be created using an access token that was generated by the app that owns the property collection. To create collections and definitions requires a user who is also an admin/editor of the app. Since the GraphQL API calls via Fusion desktop are not being made by a specific 3rd party application, the necessary permissions to create or modify custom properties are not available.

As a result, operations involving the modification of the structure or values of custom properties are prohibited to ensure adherence to authorization protocols. This ensures that the operations are performed within the appropriate security context.

Understanding these limitations ensures that developers do not attempt unsupported operations within the Fusion Desktop API, thus avoiding potential errors and maintaining smooth workflow integration between local and cloud environments.

## Samples

There are three samples that demonstrate calling the MFGDM API using the GraphQL API to get and set properties.

- [Set part number using the MFGDM GraphQL API](SetPartNumberUsingGraphQL_Sample.md)
- [Get the part number from components using the MFGDM GraphQL API](FetchPartNumberForComponents_Sample.md)
- [Gets all properties using the MFGDM GraphQL API](FetchBulkComponentProperties_Sample.md)

