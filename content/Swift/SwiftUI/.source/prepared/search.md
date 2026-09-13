# Search

Enable people to search for text or other content within your app.

## Overview {#Overview}

To present a search field in your app, create and manage storage for search text and optionally for discrete search terms known as *tokens*. Then bind the storage to the search field by applying the searchable view modifier to a view in your app.

![](./images/search-hero@2x.png)

As people interact with the field, they implicitly modify the underlying storage and, thereby, the search parameters. Your app correspondingly updates other parts of its interface. To enhance the search interaction, you can also:

- Offer suggestions during search, for both text and tokens.
- Implement search scopes that help people to narrow the search space.
- Detect when people activate the search field, and programmatically dismiss the search field using environment values.

For design guidance, see [Searching](https://developer.apple.com/design/human-interface-guidelines/searching) in the Human Interface Guidelines.

## Searching your app’s data model {#Searching-your-apps-data-model}

- [Adding a search interface to your app](9.1-AddingASearchInterfaceToYourApp/) — Present an interface that people can use to search for content in your app.
- [Performing a search operation](9.2-PerformingASearchOperation/) — Update search results based on search text and optional tokens that you store.
- [searchable(text:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:placement:prompt:)) — Marks this view as searchable, which configures the display of a search field.
- [searchable(text:tokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:placement:prompt:token:)) — Marks this view as searchable with text and tokens.
- [searchable(text:editableTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:placement:prompt:token:)) — Marks this view as searchable, which configures the display of a search field.
- [SearchFieldPlacement](https://developer.apple.com/documentation/swiftui/searchfieldplacement) — The placement of a search field in a view hierarchy.

## Making search suggestions {#Making-search-suggestions}

- [Suggesting search terms](9.3-SuggestingSearchTerms/) — Provide suggestions to people searching for content in your app.
- [searchSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:)) — Configures the search suggestions for this view.
- [searchSuggestions(_:for:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:for:)) — Configures how to display search suggestions within this view.
- [searchCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/searchcompletion(_:)) — Associates a fully formed string with the value of this view when used as a search suggestion.
- [searchable(text:tokens:suggestedTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:placement:prompt:token:)) — Marks this view as searchable with text, tokens, and suggestions.
- [SearchSuggestionsPlacement](https://developer.apple.com/documentation/swiftui/searchsuggestionsplacement) — The ways that SwiftUI displays search suggestions.

## Limiting search scope {#Limiting-search-scope}

- [Scoping a search operation](9.4-ScopingASearchOperation/) — Divide the search space into a few broad categories.
- [searchScopes(_:scopes:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:scopes:)) — Configures the search scopes for this view.
- [searchScopes(_:activation:_:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:activation:_:)) — Configures the search scopes for this view with the specified activation strategy.
- [SearchScopeActivation](https://developer.apple.com/documentation/swiftui/searchscopeactivation) — The ways that searchable modifiers can show or hide search scopes.

## Detecting, activating, and dismissing search {#Detecting-activating-and-dismissing-search}

- [Managing search interface activation](9.5-ManagingSearchInterfaceActivation/) — Programmatically detect and dismiss a search field.
- [isSearching](https://developer.apple.com/documentation/swiftui/environmentvalues/issearching) — A Boolean value that indicates when the user is searching.
- [dismissSearch](https://developer.apple.com/documentation/swiftui/environmentvalues/dismisssearch) — An action that ends the current search interaction.
- [DismissSearchAction](https://developer.apple.com/documentation/swiftui/dismisssearchaction) — An action that can end a search interaction.
- [searchable(text:isPresented:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:ispresented:placement:prompt:)) — Marks this view as searchable with programmatic presentation of the search field.
- [searchable(text:tokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:ispresented:placement:prompt:token:)) — Marks this view as searchable with text and tokens, as well as programmatic presentation.
- [searchable(text:editableTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:ispresented:placement:prompt:token:)) — Marks this view as searchable, which configures the display of a search field.
- [searchable(text:tokens:suggestedTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:ispresented:placement:prompt:token:)) — Marks this view as searchable with text, tokens, and suggestions, as well as programmatic presentation.

## Displaying toolbar content during search {#Displaying-toolbar-content-during-search}

- [searchPresentationToolbarBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchpresentationtoolbarbehavior(_:)) — Configures the search toolbar presentation behavior for any searchable modifiers within this view.
- [SearchPresentationToolbarBehavior](https://developer.apple.com/documentation/swiftui/searchpresentationtoolbarbehavior) — A type that defines how the toolbar behaves when presenting search.

## Searching for text in a view {#Searching-for-text-in-a-view}

- [findNavigator(isPresented:)](https://developer.apple.com/documentation/swiftui/view/findnavigator(ispresented:)) — Programmatically presents the find and replace interface for text editor views.
- [findDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/finddisabled(_:)) — Prevents find and replace operations in a text editor.
- [replaceDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/replacedisabled(_:)) — Prevents replace operations in a text editor.
- [FindContext](https://developer.apple.com/documentation/swiftui/findcontext) — The status of the find navigator for views which support text editing.
