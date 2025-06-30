# Static Site Generator

A flexible static site generator built in Python that converts Markdown files into beautiful HTML websites, optimized for GitHub Pages deployment.

## About

This project was built as part of the Boot.dev curriculum. It's a command-line tool that takes Markdown files and generates a complete static website with proper navigation, styling, and structure. The output is generated in a `docs` directory for seamless GitHub Pages hosting.

## Features

- Converts Markdown to HTML
- Generates navigation between pages
- Supports custom CSS themes
- Recursive directory processing
- Clean, semantic HTML output
- **Github Pages ready** - outputs to `docs` directory

## Installation

1. Clone this repository:
```
bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
2. Make sure you have Python 3.x installed.

## Usage

Run the static site generator with:
```
python main.py
```

The generator will:

1. Read Markdown files from your content directory
2. Convert them to HTML
3. Apply styling and navigation
4. Outpu the complete website to the `docs` directory

## Project structure

```
├── main.py              # Main application entry point
├── src/                 # Source code modules
├── content/             # Markdown content files
├── static/              # CSS and other static assets
├── docs/                # Generated HTML output (GitHub Pages ready)
```

## Github pages deployment

This project is configured to work with Github pages:

1. Push your repository to Github
2. Go to your repository settings
3. Navigate to "Pages" in the sidebar
4. Set source to "Deploy from a branch"
5. Select "main" branch and "/docs" folder
6. Your site will be available at https://YOUR-USERNAME.github.io/YOUR-REPO-NAME

## Live demo

[View the live site](https://camilleonoda.github.io/static-site-generator/)

## What I learned

Building this static site generator was a comprehensive learning experience that taught me:

## What I Learned

Building this static site generator was a comprehensive learning experience that taught me:

### Test-Driven Development (TDD)
- **Writing tests first** to define exactly what my functions should accomplish
- **Red-Green-Refactor cycle**: Writing failing tests, making them pass, then improving the code. _Red_ forces clarity, _Green_ builds confidence and _Refactor_ improves code quality without fear of breaking it.
- **Breaking down complex problems** into small, testable units
- **Focusing on requirements**: Tests helped me stay focused on what I actually needed to build
- **Code confidence**: Having tests made refactoring and improvements much safer

### Testing Best Practices
- **Unit testing**: Testing individual functions in isolation
- **Test organization**: Structuring test files and keeping tests maintainable
- **Edge case handling**: Thinking through what could go wrong and testing for it
- **Debugging through tests**: Using failing tests to pinpoint exactly where issues occur

### Code Quality & Design
- **Keeping functions simple**: TDD naturally led to smaller, more focused functions
- **Better code organization**: Writing testable code forced better separation of concerns
- **Understanding my own code**: Writing tests made me think deeply about what each piece does
- **Maintainable architecture**: Tests acted as documentation for how my code should behave

### Core Programming Concepts
- **File system operations**: Reading, writing, and organizing files programmatically
- **Recursive algorithms**: Traversing directory structures to process nested content
- **String manipulation**: Parsing Markdown syntax and generating clean HTML
- **Object-oriented programming**: Structuring code with classes and methods for maintainability

### Python-Specific Skills
- **Testing frameworks**: Using Python's built-in `unittest` module
- **Path handling** with `pathlib` for cross-platform compatibility
- **Exception handling** for robust file operations
- **Module organization** and code separation for cleaner architecture

### Development Workflow
- **Command-line applications**: Building tools that can be run from the terminal
- **Version control**: Managing code changes and project history with Git
- **Deployment**: Setting up GitHub Pages for web hosting

The biggest revelation was how **TDD changed my approach to programming**.

Instead of writing code and hoping it works, I now define success criteria first, then build to meet those exact requirements.

It forces me to think about what is needed before how it should be built. 

This kept my code simple, focused, and much easier to understand and maintain.

## Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)
- [Boot.dev](https://www.boot.dev/courses/build-static-site-generator-python)

## Acknowledgements

Built as part of the [Boot.dev](https://www.boot.dev/courses/build-static-site-generator-python)
