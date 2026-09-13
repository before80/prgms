# Building a document-based app with SwiftUI

Create, save, and open documents in a multiplatform app.

## Overview {#Overview}

With this sample app, people can create, save, and open checklist documents on iPhone, iPad, Mac, and Vision Pro. In the app, people can also:

- Add, delete, and reorder checklist items.
- Select and deselect items to mark them complete.
- Undo and redo their changes.

The app uses SwiftUI’s [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) scene and [Document](https://developer.apple.com/documentation/swiftui/document) protocol to open, save, and manage checklist files, and registers its own custom document type so the system knows to open checklist files with this app.

![A screenshot displaying the document launch experience on iPad with a robot and plant accessory to the left and right of the title view, respectively.](./images/writing-app-ipad@2x.png)

> Note: This sample targets the [Document](https://developer.apple.com/documentation/swiftui/document) protocol described in [Creating a document-based app](../5.1-CreatingADocumentBasedApp/) and [Updating your document-based app](../5.3-UpdatingYourDocumentBasedApp/).

## Configure the sample code project {#Configure-the-sample-code-project}

To build and run this sample on your device, select your development team for the project’s target using these steps:

1. Open the sample with the latest version of Xcode.
1. Select the top-level project.
1. For the project’s target, choose your team from the Team pop-up menu in the Signing & Capabilities pane to let Xcode automatically manage your provisioning profile.

## Create the data model {#Create-the-data-model}

This sample has a data model that defines a checklist as a collection of items. Each item has a title and a Boolean value that tracks whether someone checked it off. `ChecklistItem` and `Checklist` conform to [Codable](https://developer.apple.com/documentation/swift/codable) for serialization, and to [Identifiable](https://developer.apple.com/documentation/swift/identifiable) for unique identification during enumeration. `ChecklistItem` also conforms to [Equatable](https://developer.apple.com/documentation/swift/equatable) so SwiftUI can detect when an item’s content changes, as shown here:

```swift
struct ChecklistItem: Identifiable, Codable, Equatable {
    var id = UUID()
    var isChecked = false
    var title: String
}

struct Checklist: Identifiable, Codable {
    var id = UUID()
    var items: [ChecklistItem]
}
```

## Define the app’s scene {#Define-the-apps-scene}

An app becomes document-based when its first scene in the `App` declaration is either a `DocumentGroup` or a `DocumentGroupLaunchScene`. In this sample, the document type conforms to the [Document](https://developer.apple.com/documentation/swiftui/document) protocol. The `editor` closure of the initializer returns a view that renders the document’s contents, and the `makeDocument` closure creates a new document instance, like this:

```swift
@main
struct DocumentBasedApp: App {
    var body: some Scene {
        DocumentGroup { document in
            ChecklistView(document: document)
        } makeDocument: { configuration, context in
            ChecklistDocument()
        }
    }
}
```

## Customize the iOS and iPadOS launch experience {#Customize-the-iOS-and-iPadOS-launch-experience}

You can update the default launch experience on iOS and iPadOS with a custom title, action buttons, and a screen background. To add an action button with a custom label, use `Button`. For a button that creates new documents, use a [NewDocumentButton](https://developer.apple.com/documentation/swiftui/newdocumentbutton) with a custom title. You can customize the background, such as adding a view or a `backgroundStyle` with an initializer, for example, [init(_:backgroundStyle:_:backgroundAccessoryView:overlayAccessoryView:)](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene/init(_:backgroundstyle:_:backgroundaccessoryview:overlayaccessoryview:)-2d13c). This sample customizes the background of the title view using a [init(_:_:background:overlayAccessoryView:)](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene/init(_:_:background:overlayaccessoryview:)) initializer of [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene), and places a robot and a plant on either side of the title as an overlay accessory view, as shown here:

```swift
DocumentGroupLaunchScene("Checklist") {
    NewDocumentButton("Start a Checklist")
} background: {
    Image(.pinkJungle)
        .resizable()
        .scaledToFill()
} overlayAccessoryView: { _ in
    AccessoryView()
}
```

Because [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene) isn’t available in macOS, add this scene alongside the sample’s [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) scene within an `#if os(iOS)` conditional compilation block.

## Adopt the document protocol {#Adopt-the-document-protocol}

The `ChecklistDocument` class adopts the [Document](https://developer.apple.com/documentation/swiftui/document) protocol to read and write checklists from and to files. Because [Document](https://developer.apple.com/documentation/swiftui/document) requires a reference type, `ChecklistDocument` is a `final class` marked with [Observable()](https://developer.apple.com/documentation/observation/observable()), rather than a structure. The [readableContentTypes](https://developer.apple.com/documentation/swiftui/readabledocument/readablecontenttypes) property defines the types that the sample can read, specifically, the `.checklistDocument` type, like this:

```swift
static let readableContentTypes: [UTType] = [.checklistDocument]
```

The sample reads a checklist from a file using a [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) that its [reader(configuration:)](https://developer.apple.com/documentation/swiftui/readabledocument/reader(configuration:)) method returns. This sample uses [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) with a closure that decodes a file wrapper’s contents using a [JSONDecoder](https://developer.apple.com/documentation/foundation/jsondecoder), as shown here:

```swift
func reader(configuration: sending ReadConfiguration) -> sending FileWrapperDocumentReader<Checklist> {
    FileWrapperDocumentReader(configuration) { fileWrapper in
        guard let data = fileWrapper.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        return try JSONDecoder().decode(Checklist.self, from: data)
    }
}
```

After SwiftUI reads a checklist in the background, it delivers the result to the document’s [apply(snapshot:previous:)](https://developer.apple.com/documentation/swiftui/readabledocument/apply(snapshot:previous:)) method on the main actor, which updates the document’s observable state, like this:

```swift
@MainActor
func apply(snapshot: sending Checklist, previous: sending Checklist?) async throws {
    checklist = snapshot
}
```

When someone saves the document, the sample returns a snapshot of its data from [snapshot(contentType:)](https://developer.apple.com/documentation/swiftui/writabledocument/snapshot(contenttype:)), which also runs on the main actor as follows:

```swift
@MainActor
func snapshot(contentType: UTType) async throws -> sending Checklist {
    checklist // Make a copy.
}
```

Conversely, the [writer(configuration:)](https://developer.apple.com/documentation/swiftui/writabledocument/writer(configuration:)) method returns a [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) that encodes the snapshot and writes it to disk. This sample uses [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter) with a closure that serializes the snapshot into a file wrapper using a [JSONEncoder](https://developer.apple.com/documentation/foundation/jsonencoder) instance, like this:

```swift
func writer(configuration: sending WriteConfiguration) -> sending FileWrapperDocumentWriter<Checklist> {
    FileWrapperDocumentWriter(configuration) { snapshot, _ in
        let data = try JSONEncoder().encode(snapshot)
        return FileWrapper(regularFileWithContents: data)
    }
}
```

## Register undo and redo actions {#Register-undo-and-redo-actions}

With the [Document](https://developer.apple.com/documentation/swiftui/document) protocol, undo management is mandatory to enable autosave. Read the active [UndoManager](https://developer.apple.com/documentation/foundation/undomanager) from the environment and update the document through methods that register an undo action. Calling the same method again from the undo closure also registers the redo action, so most operations only need one method, as shown here:

```swift
@MainActor
func toggleItem(_ item: Binding<ChecklistItem>, undoManager: UndoManager? = nil) {
    item.wrappedValue.isChecked.toggle()

    undoManager?.registerUndo(withTarget: self) { doc in
        doc.toggleItem(item, undoManager: undoManager)
    }
}
```

## Export a custom document type {#Export-a-custom-document-type}

The app defines and exports a custom content type for the documents it creates. It declares this custom type in the project’s [Information Property List](https://developer.apple.com/documentation/bundleresources/information-property-list) file under the [UTExportedTypeDeclarations](https://developer.apple.com/documentation/bundleresources/information-property-list/utexportedtypedeclarations) key. This sample uses `com.example.checklist` as the identifier in the information property list file, as the following code demonstrates:

```swift
<key>CFBundleDocumentTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>LSHandlerRank</key>
        <string>Default</string>
        <key>LSItemContentTypes</key>
        <array>
            <string>com.example.checklist</string>
        </array>
        <key>NSUbiquitousDocumentUserActivityType</key>
        <string>$(PRODUCT_BUNDLE_IDENTIFIER).example-document</string>
    </dict>
</array>
<key>UTExportedTypeDeclarations</key>
<array>
    <dict>
        <key>UTTypeConformsTo</key>
        <array>
            <string>public.data</string>
            <string>public.content</string>
        </array>
        <key>UTTypeDescription</key>
        <string>Checklist Document</string>
        <key>UTTypeIconFiles</key>
        <array/>
        <key>UTTypeIdentifier</key>
        <string>com.example.checklist</string>
        <key>UTTypeTagSpecification</key>
        <dict>
            <key>public.filename-extension</key>
            <array>
                <string>checklist</string>
            </array>
        </dict>
    </dict>
</array>
```

For convenience, you can also define the content type in code, as seen in the following example:

```swift
extension UTType {
    static let checklistDocument = UTType(exportedAs: "com.example.checklist")
}
```

Specify a file extension for every custom format you declare to make sure the operating system opens files with the given extension using your app. For more information about custom file and data types, see [Defining file and data types for your app](https://developer.apple.com/documentation/uniformtypeidentifiers/defining-file-and-data-types-for-your-app).

## See Also {#See-Also}

#### Related samples {#Related-samples}

- [Building a document-based app using SwiftData](../5.5-BuildingADocumentBasedAppUsingSwiftdata/)

#### Related articles {#Related-articles}

- [Creating a document-based app](../5.1-CreatingADocumentBasedApp/)
- [Updating your document-based app](../5.3-UpdatingYourDocumentBasedApp/)
- [Defining file and data types for your app](https://developer.apple.com/documentation/uniformtypeidentifiers/defining-file-and-data-types-for-your-app)

#### Related videos {#Related-videos}

- [What’s new in SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269)
