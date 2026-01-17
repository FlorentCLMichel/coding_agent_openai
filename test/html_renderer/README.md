# HTML Renderer

A simple HTML renderer written in Rust. This project parses HTML files and renders them to PNG images using Cairo and Pango.

## Features

- Parse HTML files using `html5ever` and `markup5ever_rcdom`.
- Render HTML content to PNG images using `cairo-rs` and `pango`.
- Command-line interface for specifying input and output files.

## Prerequisites

Ensure you have the following installed:

- [Rust](https://www.rust-lang.org/tools/install) (latest stable version)
- Required system libraries for Cairo and Pango (installation instructions below)

### Installing System Libraries

#### Ubuntu/Debian

```bash
sudo apt-get install libcairo2-dev libpango1.0-dev
```

#### Fedora

```bash
sudo dnf install cairo-devel pango-devel
```

#### macOS (using Homebrew)

```bash
brew install cairo pango
```

## Building the Project

1. Clone the repository or navigate to the project directory:

```bash
cd html_renderer
```

2. Build the project:

```bash
cargo build --release
```

This will create an optimized binary in `target/release/html_renderer`.

## Running the Project

### Basic Usage

Render an HTML file and save the output as `output.png`:

```bash
./target/release/html_renderer example.html
```

### Custom Output Name

Specify a custom output file name:

```bash
./target/release/html_renderer example.html custom_output.png
```

### Example

```bash
# Render example.html and save as output.png
./target/release/html_renderer example.html

# Render example.html and save as my_rendering.png
./target/release/html_renderer example.html my_rendering.png
```

## Project Structure

- `src/main.rs`: Main application logic for parsing HTML and rendering to PNG.
- `example.html`: Example HTML file for testing.
- `Cargo.toml`: Project configuration and dependencies.

## Dependencies

- `html5ever`: HTML parser.
- `markup5ever_rcdom`: DOM representation for parsed HTML.
- `cairo-rs`: 2D graphics library for rendering.
- `pango`: Text layout and rendering library.
- `pangocairo`: Integration between Pango and Cairo.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- Thanks to the Rust community for providing excellent libraries and tools.
- Inspired by the need for a simple, offline HTML renderer.
