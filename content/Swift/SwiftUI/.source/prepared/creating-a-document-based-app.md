# Creating a document-based app

Build apps that people can use to open, edit, and save files using coordinated file access.

## Overview {#overview}

With document-based apps, people can create and manage their own files, like text documents, drawings, and spreadsheets. The [Document](https://developer.apple.com/documentation/swiftui/document) protocol — available in iOS 27, macOS 27, and visionOS 27 — gives you direct access to your document’s file URL, so you can:

- Read and write files
- Pass the URL to other frameworks like Core Graphics, AVFoundation, or PDFKit to report progress during long operations
- Access the file safely using a `FileCoordinator`, provided by [makeFileCoordinator()](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration/makefilecoordinator())

The [Document](https://developer.apple.com/documentation/swiftui/document) combined protocol has no requirements of its own but conforms to [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) and [WritableDocument](https://developer.apple.com/documentation/swiftui/writabledocument). With it, you can conveniently declare the conformance of your type, as follows:

```swift
 @Observable
 final class TextDocument: Document { }
```

Because [Document](https://developer.apple.com/documentation/swiftui/document) is a reference type, SwiftUI doesn’t need to recreate the document on every change, and you can observe individual property changes with the [@Observable](https://developer.apple.com/documentation/observation/observable) macro.

The following diagram shows the relationship between the document protocols and the reader and writer protocols:

![A diagram showing two document protocols side by side. On the left, a writable document protocol lists three requirements and connects with an arrow to a document writer protocol below it. On the right, a readable document protocol lists three requirements and connects with an arrow to a document reader protocol below it.](./images/Creating-a-document-based-app-document-protocols@2x.png)

## Set up a document-based app {#Set-up-a-document-based-app}

To opt into the document infrastructure — autosaving, file coordination, file dialogs, keyboard shortcuts, conflict resolution, and more — use [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) or [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene) as your app’s first scene. In iOS, set [UISupportsDocumentBrowser](https://developer.apple.com/documentation/bundleresources/information-property-list/uisupportsdocumentbrowser) to `YES` in your information property list to present a document browser.

A minimal document-based app looks like this:

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        DocumentGroup { document in
            TextEditorView(document: document)
        } makeDocument: { configuration, context in
            TextDocument(configuration: configuration, context)
        }
    }
}
```

The [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) initializers take two closures: an `editor` or `viewer` closure parameter that builds the user interface for an open document, and a `makeDocument` or `makeReadableDocument` closure that returns the document instance.

The [URLDocumentConfiguration](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration) class that SwiftUI passes to your document’s initializer exposes the file URL, [lastContentModificationDate](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration/lastcontentmodificationdate), and [makeFileCoordinator()](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration/makefilecoordinator()), which creates a file coordinator for accessing the document’s URL outside of read and write. Plus, it conforms to [@Observable](https://developer.apple.com/documentation/observation/observable) so your code can react to changes.

In iOS, use [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene) to customize the document browser launch screen with a custom background and multiple creation buttons, like this example:

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        DocumentGroupLaunchScene("My Notes and Lists") {
            NewDocumentButton("New Note", source: .note)
            NewDocumentButton("New List", source: .list)
        } background: {
            LinearGradient(
                colors: [.brandColorGradientStart, .brandColorGradientEnd],
                startPoint: .top,
                endPoint: .bottom
            )
        }

        DocumentGroup { document in
            TextEditorView(document: document)
        } makeDocument: { configuration, context in
            TextDocument(configuration: configuration, context)
        }
    }
}

extension DocumentCreationSource {
    static let note = DocumentCreationSource(id: "note")
    static let list = DocumentCreationSource(id: "list")
}
```

In your `TextDocument` initializer, check [creationSource](https://developer.apple.com/documentation/swiftui/documentcreationcontext/creationsource) to find out which button a person tapped and to set up the document as a list or as a note.

## Display a custom UI before presenting a document {#Display-a-custom-UI-before-presenting-a-document}

Because the `makeDocument` and `makeReadableDocument` closures are asynchronous, you can also suspend document creation to display a custom user interface — such as a template picker, a configuration wizard, or an import preview — before the document appears. Refer to [NewDocumentButton](https://developer.apple.com/documentation/swiftui/newdocumentbutton) for an end-to-end example of using the [CheckedContinuation](https://developer.apple.com/documentation/swift/checkedcontinuation) structure to present a template picker or other setup UI before the document opens.

## Create a simple document {#Create-a-simple-document}

To conform your model to [Document](https://developer.apple.com/documentation/swiftui/document), provide values that conform to the [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) and [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) protocols. In most cases, use the [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) and [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter) convenience types provided by SwiftUI to handle writing and reading for you.

Declare [readableContentTypes](https://developer.apple.com/documentation/swiftui/readabledocument/readablecontenttypes) to list the formats your document can open and [writableContentTypes](https://developer.apple.com/documentation/swiftui/writabledocument/writablecontenttypes) to list the formats it can save. The document browser consults the [readableContentTypes](https://developer.apple.com/documentation/swiftui/readabledocument/readablecontenttypes) to allow opening the files of supported types; the save panel uses [writableContentTypes](https://developer.apple.com/documentation/swiftui/writabledocument/writablecontenttypes) for format options.

Both [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) and [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) are independent protocols. When saving, SwiftUI calls [snapshot(contentType:)](https://developer.apple.com/documentation/swiftui/writabledocument/snapshot(contenttype:)) to capture the current state, then passes the result to [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) in the background. When reading, [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) runs in the background and returns a snapshot, which SwiftUI delivers to your document through [apply(snapshot:previous:)](https://developer.apple.com/documentation/swiftui/readabledocument/apply(snapshot:previous:)).

A snapshot represents the document’s state at a given moment. A document type can use different snapshot types for reading and writing. You can use anything as a snapshot, including the document type itself. SwiftUI coordinates file access for reading and writing automatically.

Define an [Observable](https://developer.apple.com/documentation/observation/observable) class that conforms to `Document`, like this:

```swift
import SwiftUI
import UniformTypeIdentifiers

@Observable
final class TextDocument: Document {
    static let readableContentTypes = [UTType.plainText]

    var text: String
    var configuration: URLDocumentConfiguration

    init(configuration: URLDocumentConfiguration) {
        self.text = ""
        self.configuration = configuration
    }

    // Returns a reader that converts a `FileWrapper` into a snapshot.

    func reader(
        configuration: sending ReadConfiguration
    ) -> sending FileWrapperDocumentReader<String> {
        FileWrapperDocumentReader(configuration) { fileWrapper in
            if let data = fileWrapper.regularFileContents,
               let text = String(data: data, encoding: .utf8) {
                return text
            }
            return ""
        }
    }

    @MainActor
    func apply(snapshot: String, previous: String?) async throws {
        self.text = snapshot
    }

    // Returns a writer that converts a snapshot into a `FileWrapper`.

    func writer(
        configuration: sending WriteConfiguration
    ) -> sending FileWrapperDocumentWriter<String> {
        FileWrapperDocumentWriter(configuration) { snapshot, previous in
            let data = Data(snapshot.utf8)
            return FileWrapper(regularFileWithContents: data)
        }
    }

    @MainActor
    func snapshot(contentType: UTType) async throws -> sending String {
        text
    }
}
```

With this document model and the [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) setup from the previous section, you have a complete document-based app with open and save support.

When SwiftUI autosaves the document or a person presses Command-S, it calls [snapshot(contentType:)](https://developer.apple.com/documentation/swiftui/writabledocument/snapshot(contenttype:)) on the main actor to capture the current state, then calls `writer(configuration:)` to get the [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter). SwiftUI then passes the snapshot and destination URL to `write(snapshot:to:previous:progress:)` in the background with coordinated file access.

Reading works the same way: SwiftUI calls `reader(configuration:)`, passes the file URL to `read(from:progress:)` in the background, then delivers the snapshot to your document through [apply(snapshot:previous:)](https://developer.apple.com/documentation/swiftui/readabledocument/apply(snapshot:previous:)).

## Support read-only documents {#Support-read-only-documents}

To set up your app to display read-only documents, conform to [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) and use the initializer that produces a `ReadableDocument`-conforming value:

```swift
DocumentGroup { document in
    PDFViewer(document: document)
} makeReadableDocument: { configuration, context in
    PDFDocument(configuration: configuration, context: context)
}
@Observable
final class PDFDocument: ReadableDocument { /* ... */}
```

Set [CFBundleTypeRole](https://developer.apple.com/documentation/bundleresources/information-property-list/cfbundleurltypes/cfbundletyperole) to `Viewer` in your information property list to indicate your app doesn’t edit this file type. For apps that can edit documents, set the role to `Editor`.

## Register undo actions {#Register-undo-actions}

SwiftUI tracks unsaved changes through undo actions, so every document-based app needs to register them. Read the active [UndoManager](https://developer.apple.com/documentation/foundation/undomanager) from the environment and update the document through methods that register an undo action. Calling the same method from the undo closure also registers the redo action automatically, as shown here:

```swift
struct TextEditorView: View {
    @Bindable var document: TextDocument
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        TextEditor(text: $document.text)
              .onChange(of: document.text) { oldValue, _ in
                  undoManager?.registerUndo(withTarget: document) { document in
                      document.text = oldValue
                  }
            }
    }
}
```

## Work with package documents {#Work-with-package-documents}

A package is a directory that the system presents as a single item. People see one icon in Finder, the Files app, and the document browser that they can drag, share, back up, and sync. Inside, your package can hold any files you need, including metadata, pages, layers, or embedded media.

Start with [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) and [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter). Then use a custom [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) and [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) only when you need to stream data or access URLs directly, or want to optimize disk operations.

The following example shows a minimal notebook document. Its on-disk layout looks like this:

```swift
MyNotebook.notebook/
├── metadata.json        ← title + ordered page IDs
└── pages/
    ├── <uuid>.txt       ← each page is plain text
    └── …
```

```swift
import UniformTypeIdentifiers

@Observable
final class NotebookDocument: Document {
    static let readableContentTypes: [UTType] = [.notebook]   // remember to declare in Info.plist

    var metadata: NotebookMetadata
    var pages: [UUID: String]

    init() {
        let initialPageID = UUID()
        self.metadata = NotebookMetadata(
            title: "Untitled", pageOrder: [initialPageID]
        )
        self.pages = [initialPageID: ""]
    }

    func reader(
        configuration: sending ReadConfiguration
    ) -> sending FileWrapperDocumentReader<NotebookSnapshot> {
        FileWrapperDocumentReader(configuration) { directory in
            let children = directory.fileWrappers ?? [:]

            guard let metadataData = children["metadata.json"]?.regularFileContents else {
                throw CocoaError(.fileReadCorruptFile)
            }
            let metadata = try JSONDecoder().decode(NotebookMetadata.self, from: metadataData)

            guard let pagesDirectory = children["pages"]?.fileWrappers else {
                throw CocoaError(.fileReadCorruptFile)
            }

            var pages: [UUID: String] = [:]
            for (filename, wrapper) in pagesDirectory {
                guard let data = wrapper.regularFileContents
                else { continue }
                let withoutExtension = filename.replacingOccurrences(
                    of: ".txt", with: ""
                )
                if let id = UUID(uuidString: withoutExtension) {
                    pages[id] = String(decoding: data, as: UTF8.self)
                }
            }

            return NotebookSnapshot(metadata: metadata, pages: pages)
        }
    }

    func writer(
        configuration: sending WriteConfiguration
    ) -> sending FileWrapperDocumentWriter<NotebookSnapshot> {
        FileWrapperDocumentWriter(configuration) { snapshot, _ in
            let metadata = try JSONEncoder().encode(snapshot.metadata)
            let metadataWrapper = FileWrapper(regularFileWithContents: metadata)

            var pageNamesToFileWrappers: [String: FileWrapper] = [:]
            for (pageID, content) in snapshot.pages {
                pageNamesToFileWrappers["\(pageID.uuidString).txt"] =
                    FileWrapper(regularFileWithContents: Data(content.utf8))
            }
            let pagesDirectory = FileWrapper(directoryWithFileWrappers: pageNamesToFileWrappers)

            let root = FileWrapper(directoryWithFileWrappers: [
                "metadata.json": metadataWrapper,
                "pages": pagesDirectory,
            ])
            return root
        }
    }

    @MainActor
    func snapshot(contentType: UTType) async throws -> sending NotebookSnapshot {
        NotebookSnapshot(metadata: metadata, pages: pages)
    }

    @MainActor
    func apply(
        snapshot: sending NotebookSnapshot,
        previous: sending NotebookSnapshot?
    ) async throws {
        metadata = snapshot.metadata
        pages = snapshot.pages
    }
}

struct NotebookMetadata: Codable, Sendable {
    var title: String
    var pageOrder: [UUID]
}

struct NotebookSnapshot: Sendable {
    var metadata: NotebookMetadata
    var pages: [UUID: String]
}

extension UTType {
    static let notebook = UTType(exportedAs: "com.example.notebook")
}
```

The [FileWrapper](https://developer.apple.com/documentation/foundation/filewrapper) class loads file contents on demand. When you open a package, [FileWrapper](https://developer.apple.com/documentation/foundation/filewrapper) reads the directory structure but doesn’t load any file contents. Each file only loads when you access its [regularFileContents](https://developer.apple.com/documentation/foundation/filewrapper/regularfilecontents), which makes [FileWrapper](https://developer.apple.com/documentation/foundation/filewrapper) a good fit when you only need part of a package. If you only need a metadata file, a thumbnail, or the first few pages, look through [fileWrappers](https://developer.apple.com/documentation/foundation/filewrapper/filewrappers) to find what you need and call [regularFileContents](https://developer.apple.com/documentation/foundation/filewrapper/regularfilecontents) only on those files.

> Important: If an app decides to read documents lazily — for example, only read a portion of a package that’s visible to a person at a moment — the app needs to be prepared that subsequent attempts to read from the file wrapper might fail because the files might be gone or moved. Always handle errors when you read from a `FileWrapper`.

## Implement custom readers and writers {#Implement-custom-readers-and-writers}

Both [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) and [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter) delegate reading and writing to [FileWrapper](https://developer.apple.com/documentation/foundation/filewrapper). For documents that need more control, such as streaming reads, custom writing logic, or direct URL access to frameworks like Core Graphics, AVFoundation, or PDFKit, implement your own types that conform to [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) and [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter).

The following example shows an image document that uses Core Graphics to load and save JPEG files with adjustable compression quality:

```swift
import SwiftUI
import CoreGraphics
import UniformTypeIdentifiers

struct ImageSnapshot {
    var image: CGImage?
    var compressionQuality: Double
}

@Observable
final class ImageDocument: Document {
    static let readableContentTypes: [UTType] = [.jpeg]

    var displayImage: CGImage?
    var compressionQuality: Double = 0.9

    init() { }
}
```

`ImageDocument.Reader` conforms to [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) by implementing `read(from:progress:)`, which passes the source URL to `CGImageSourceCreateWithURL(_:_:)` so Core Graphics handles format detection and decoding, as shown here:

```swift
extension ImageDocument {
    struct Reader: DocumentReader {
        @concurrent 
        func read(from source: URL, progress: consuming Subprogress) async throws -> sending ImageSnapshot {
            guard let imageSource = CGImageSourceCreateWithURL(source as CFURL, nil),
                  let image = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
                throw CocoaError(.fileReadCorruptFile)
            }
            return ImageSnapshot(image: image, compressionQuality: 0.9)
        }
    }

    func reader(configuration: sending ReadConfiguration) -> sending Reader {
        Reader()
    }

    @MainActor
    func apply(snapshot: sending ImageSnapshot, previous: sending ImageSnapshot?) async throws {
        self.compressionQuality = snapshot.compressionQuality
        self.displayImage = snapshot.image
    }
}
```

SwiftUI calls `reader(configuration:)` each time it needs to read or re-read the document, for example, when the document opens or when another process changes it. The [DocumentReadConfiguration](https://developer.apple.com/documentation/swiftui/documentreadconfiguration) provides the content type, and the file URL arrives as the `source` parameter to `read(from:progress:)`.

Next, the following code example shows how to use `CGImageDestination` to encode the image as JPEG and apply the snapshot’s compression quality. `ImageDocument.Writer` conforms to [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) by implementing `write(snapshot:to:previous:progress:)`, which passes the destination URL to `CGImageDestinationCreateWithURL(_:_:_:_:)` so Core Graphics handles JPEG encoding and compression.

```swift
extension ImageDocument {
    struct Writer: DocumentWriter {
        @concurrent
        func write(
            content snapshot: sending ImageSnapshot, to destination: URL,
            previous: sending ImageSnapshot?, progress: consuming Subprogress
        ) async throws {
            guard let image = snapshot.image else { return }

            guard let imageDestination = CGImageDestinationCreateWithURL(
                destination as CFURL, UTType.jpeg.identifier as CFString, 1, nil
            ) else {
                throw CocoaError(.fileWriteUnknown)
            }

            let options: [CFString: Any] = [
                kCGImageDestinationLossyCompressionQuality: snapshot.compressionQuality
            ]
            CGImageDestinationAddImage(imageDestination, image, options as CFDictionary)

            guard CGImageDestinationFinalize(imageDestination) else {
                throw CocoaError(.fileWriteUnknown)
            }
        }
    }

    func writer(configuration: sending WriteConfiguration) -> sending Writer {
        Writer()
    }

    @MainActor
    func snapshot(contentType: UTType) async throws -> sending ImageSnapshot {
        ImageSnapshot(image: displayImage, compressionQuality: compressionQuality)
    }
}
```

The `previous` parameter contains the last successfully written snapshot. For single-file documents like a JPEG, text file, or PDF, you can ignore `previous` because you can usually rewrite the whole file. For package documents, you can compare `previous` against the current snapshot to write only the files that changed.

> Important: The [snapshot(contentType:)](https://developer.apple.com/documentation/swiftui/writabledocument/snapshot(contenttype:)) method runs on the main thread. Keep it as lightweight as possible, and perform serialization in [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) because writing runs in the background. The snapshot captures *what* to save; the writer handles *how*.

The same approach works with any framework that reads and writes files via URLs, including AVFoundation’s [AVAssetExportSession](https://developer.apple.com/documentation/avfoundation/avassetexportsession), PDFKit’s [PDFDocument(url:)](https://developer.apple.com/documentation/pdfkit/pdfdocument/init(url:)-98jte), or any C library that accepts file paths.

## Export documents {#Export-documents}

To export a document to a new location or format, use the [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:oncancellation:)) view modifier, as shown here:

```swift
final class TextDocument: WritableDocument { /* ... */ }

struct TextEditorView: View {
    @Bindable var document: TextDocument
    @State private var isExporting = false

    var body: some View {
        TextEditor(text: $document.text)
            .toolbar {
                Button("Export…") { isExporting = true }
            }
            .fileExporter(
                isPresented: $isExporting, document: document,
                contentType: .utf8PlainText, defaultFilename: "Text"
            ) { result in
                switch result {
                case .success(let url):
                    // In production, use Logger from the os framework instead of print.
                    print("Exported to \(url)")
                case .failure(let error):
                    print("Export failed: \(error)")
                }
            }
    }
}
```

For information about declaring custom file formats, accessing files outside the read and write lifecycle methods, and reporting progress for long operations, see [Handling advanced document scenarios](../5.2-HandlingAdvancedDocumentScenarios/).
