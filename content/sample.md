# Markdown Demo Page

This content comes from a Markdown file in the `content/` directory.

## Features Supported

The `Markdown` component uses `markdown2` which supports various extensions:

*   Lists (like this one)
*   **Bold** and *italic* text
*   `Inline code`
*   [Links](https://example.com) with `target-blank-links` option.
*   Tables:

| Header 1 | Header 2 | Header 3 |
| :------- | :------: | -------: |
| Left     | Center   | Right    |
| Cell     | Cell     | Cell     |

*   Fenced Code Blocks:

```python
def hello(name):
  print(f"Hello, {name}!")

hello("Markdown")
```

```javascript
console.log("Hello from JavaScript!");
```

*   Blockquotes:

> This is a blockquote within Markdown.
> It can span multiple lines.

*   Horizontal Rules:

---

*   Footnotes[^1]

[^1]: This is the footnote definition.

And more! Check the `markdown2` documentation for all supported extras.