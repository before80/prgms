# Documents

Enable people to open and manage documents.

## Overview {#Overview}

Create a user interface for opening and editing documents.

![](./images/documents-hero@2x.png)

Use the [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) and [WritableDocument](https://developer.apple.com/documentation/swiftui/writabledocument) protocols to define your document model, or adopt [Document](https://developer.apple.com/documentation/swiftui/document), a convenience protocol that combines both, when your document needs to support reading and writing. They give you direct access to file URLs, integrate with Swift concurrency, and support progress reporting. You can also use SwiftData-backed documents using an initializer like [init(editing:contentType:editor:prepareDocument:)](https://developer.apple.com/documentation/swiftui/documentgroup/init(editing:contenttype:editor:preparedocument:)).

SwiftUI supports standard behaviors people expect from a document-based app, appropriate for each platform, like multiwindow support, open and save panels. For related design guidance, see [Patterns](https://developer.apple.com/design/human-interface-guidelines/patterns) in the Human Interface Guidelines.

## Creating a document {#Creating-a-document}

- [Creating a document-based app](5.1-CreatingADocumentBasedApp/) — Build apps that people can use to open, edit, and save files using coordinated file access.
- [Handling advanced document scenarios](5.2-HandlingAdvancedDocumentScenarios/) — Extend your document-based app to support custom file formats, on-demand file access, and progress reporting.
- [Updating your document-based app](5.3-UpdatingYourDocumentBasedApp/) — Migrate an existing app to adopt URL-based document reading and writing with Swift concurrency.
- [Building a document-based app with SwiftUI](5.4-BuildingADocumentBasedAppWithSwiftui/) — Create, save, and open documents in a multiplatform app.
- [Building a document-based app using SwiftData](5.5-BuildingADocumentBasedAppUsingSwiftdata/) — Code along with the WWDC presenter to transform an app with SwiftData.
- [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) — A scene that enables support for opening, creating, and saving documents.

## Storing document data in a reference type instance {#Storing-document-data-in-a-reference-type-instance}

- [Document](https://developer.apple.com/documentation/swiftui/document) — A document that supports both reading and writing.
- [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) — A document type that supports reading from file.
- [WritableDocument](https://developer.apple.com/documentation/swiftui/writabledocument) — A document type that supports writing to file.
- [URLDocumentConfiguration](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration) — The configuration of an open document that stores its file URL, last modification date, and related metadata.
- [DocumentCreationContext](https://developer.apple.com/documentation/swiftui/documentcreationcontext) — Context about how a document was created.
- [DocumentBaseBox](https://developer.apple.com/documentation/swiftui/documentbasebox) — A Box that allows setting its Document base not requiring the caller to know the exact types of the box and its base.

## Accessing document configuration {#Accessing-document-configuration}

- [documentConfiguration](https://developer.apple.com/documentation/swiftui/environmentvalues/documentconfiguration) — The configuration of a document in a [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup).
- [DocumentConfiguration](https://developer.apple.com/documentation/swiftui/documentconfiguration) — The configuration of a document in a [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup).
- [undoManager](https://developer.apple.com/documentation/swiftui/environmentvalues/undomanager) — The undo manager used to register a view’s undo operations.

## Reading and writing documents {#Reading-and-writing-documents}

- [DocumentReadConfiguration](https://developer.apple.com/documentation/swiftui/documentreadconfiguration) — The context SwiftUI passes to [reader(configuration:)](https://developer.apple.com/documentation/swiftui/readabledocument/reader(configuration:)).
- [DocumentWriteConfiguration](https://developer.apple.com/documentation/swiftui/documentwriteconfiguration) — The context SwiftUI passes to [writer(configuration:)](https://developer.apple.com/documentation/swiftui/writabledocument/writer(configuration:)).
- [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) — A type that reads a document’s content from a file.
- [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) — A type that writes a document’s content to a file.
- [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) — A document reader that deserializes a `FileWrapper` into a snapshot.
- [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter) — A document writer that serializes a snapshot into a `FileWrapper`.

## Opening a document programmatically {#Opening-a-document-programmatically}

- [newDocument](https://developer.apple.com/documentation/swiftui/environmentvalues/newdocument) — An action in the environment that presents a new document.
- [openDocument](https://developer.apple.com/documentation/swiftui/environmentvalues/opendocument) — An action in the environment that presents an existing document.
- [OpenDocumentAction](https://developer.apple.com/documentation/swiftui/opendocumentaction) — An action that presents an existing document.

## Configuring the document launch experience {#Configuring-the-document-launch-experience}

- [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene) — A launch scene for document-based applications.
- [documentLaunchTitle(_:)](https://developer.apple.com/documentation/swiftui/scene/documentlaunchtitle(_:)) — Sets the title displayed on the document launch card.
- [documentLaunchSubtitle(_:)](https://developer.apple.com/documentation/swiftui/scene/documentlaunchsubtitle(_:)) — Sets the subtitle displayed beneath the title on the document launch card.
- [DocumentLaunchView](https://developer.apple.com/documentation/swiftui/documentlaunchview) — A view to present when launching document-related user experience.
- [documentLaunchTitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchtitle(_:)) — Sets the title displayed on the document launch card.
- [documentLaunchSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchsubtitle(_:)) — Sets the subtitle displayed beneath the title on the document launch card.
- [documentBrowserContextMenu(_:)](https://developer.apple.com/documentation/swiftui/view/documentbrowsercontextmenu(_:)) — Adds to a `DocumentLaunchView` actions that accept a list of selected files as their parameter.
- [DocumentLaunchGeometryProxy](https://developer.apple.com/documentation/swiftui/documentlaunchgeometryproxy) — A proxy for access to the frame of the scene and its title view.
- [DefaultDocumentGroupLaunchActions](https://developer.apple.com/documentation/swiftui/defaultdocumentgrouplaunchactions) — The default actions for the document group launch scene and the document launch view.
- [NewDocumentButton](https://developer.apple.com/documentation/swiftui/newdocumentbutton) — A button that creates and opens new documents.
- [DefaultNewDocumentButtonLabel](https://developer.apple.com/documentation/swiftui/defaultnewdocumentbuttonlabel) — The default label used for a new document button.
- [DocumentCreationSource](https://developer.apple.com/documentation/swiftui/documentcreationsource) — Describes the source used to create a new document.

## Renaming a document {#Renaming-a-document}

- [RenameButton](https://developer.apple.com/documentation/swiftui/renamebutton) — A button that triggers a standard rename action.
- [renameAction(_:)](https://developer.apple.com/documentation/swiftui/view/renameaction(_:)) — Sets a closure to run for the rename action.
- [rename](https://developer.apple.com/documentation/swiftui/environmentvalues/rename) — An action that activates the standard rename interaction.
- [RenameAction](https://developer.apple.com/documentation/swiftui/renameaction) — An action that activates a standard rename interaction.

## Deprecated {#Deprecated}

- [FileDocument](https://developer.apple.com/documentation/swiftui/filedocument) — A type that you use to serialize documents to and from file.
- [FileDocumentConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentconfiguration) — The properties of an open file document.
- [FileDocumentReadConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentreadconfiguration) — The configuration for reading file contents.
- [FileDocumentWriteConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentwriteconfiguration) — The configuration for serializing file contents.
- [NewDocumentAction](https://developer.apple.com/documentation/swiftui/newdocumentaction) — An action that presents a new document.
- [ReferenceFileDocument](https://developer.apple.com/documentation/swiftui/referencefiledocument) — A type that you use to serialize reference type documents to and from file.
- [ReferenceFileDocumentConfiguration](https://developer.apple.com/documentation/swiftui/referencefiledocumentconfiguration) — The properties of an open reference file document.
