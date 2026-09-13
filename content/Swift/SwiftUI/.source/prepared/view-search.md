# Search modifiers

Enable people to search for content in your app.

## Overview {#Overview}

Use search view modifiers to add search capability to your app. For more information, see [Search](../../../appstructure/9-Search/).

## Displaying a search interface {#Displaying-a-search-interface}

- [searchable(text:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:placement:prompt:)) — Marks this view as searchable, which configures the display of a search field.
- [searchable(text:isPresented:placement:prompt:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:ispresented:placement:prompt:)) — Marks this view as searchable with programmatic presentation of the search field.
- [searchPresentationToolbarBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchpresentationtoolbarbehavior(_:)) — Configures the search toolbar presentation behavior for any searchable modifiers within this view.
- [searchToolbarBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchtoolbarbehavior(_:)) — Configures the behavior for search in the toolbar.
- [searchSelection(_:)](https://developer.apple.com/documentation/swiftui/view/searchselection(_:)) — Binds the selection of the search field associated with the nearest searchable modifier to the given [TextSelection](https://developer.apple.com/documentation/swiftui/textselection) value.

## Searching with tokens {#Searching-with-tokens}

- [searchable(text:tokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:placement:prompt:token:)) — Marks this view as searchable with text and tokens.
- [searchable(text:tokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:ispresented:placement:prompt:token:)) — Marks this view as searchable with text and tokens, as well as programmatic presentation.

## Searching with editable tokens {#Searching-with-editable-tokens}

- [searchable(text:editableTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:ispresented:placement:prompt:token:)) — Marks this view as searchable, which configures the display of a search field.
- [searchable(text:editableTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:editabletokens:placement:prompt:token:)) — Marks this view as searchable, which configures the display of a search field.

## Making search suggestions {#Making-search-suggestions}

- [searchSuggestions(_:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:)) — Configures the search suggestions for this view.
- [searchSuggestions(_:for:)](https://developer.apple.com/documentation/swiftui/view/searchsuggestions(_:for:)) — Configures how to display search suggestions within this view.
- [searchCompletion(_:)](https://developer.apple.com/documentation/swiftui/view/searchcompletion(_:)) — Associates a fully formed string with the value of this view when used as a search suggestion.
- [searchable(text:tokens:suggestedTokens:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:placement:prompt:token:)) — Marks this view as searchable with text, tokens, and suggestions.
- [searchable(text:tokens:suggestedTokens:isPresented:placement:prompt:token:)](https://developer.apple.com/documentation/swiftui/view/searchable(text:tokens:suggestedtokens:ispresented:placement:prompt:token:)) — Marks this view as searchable with text, tokens, and suggestions, as well as programmatic presentation.

## Limiting search scope {#Limiting-search-scope}

- [searchScopes(_:scopes:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:scopes:)) — Configures the search scopes for this view.
- [searchScopes(_:activation:_:)](https://developer.apple.com/documentation/swiftui/view/searchscopes(_:activation:_:)) — Configures the search scopes for this view with the specified activation strategy.

## Searching through dictation {#Searching-through-dictation}

- [searchDictationBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/searchdictationbehavior(_:)) — Configures the dictation behavior for any search fields configured by the searchable modifier.
