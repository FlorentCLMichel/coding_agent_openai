use html5ever::parse_document;
use html5ever::driver::ParseOpts;
use html5ever::tendril::TendrilSink;
use markup5ever_rcdom::RcDom;
use std::fs::File;
use std::io::Read;
use std::env;

use cairo::{Context, Format, ImageSurface};
use pangocairo::functions::create_layout;

fn main() {
    // Parse command-line arguments
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: {} <input_html_file> [output_png_file]", args[0]);
        std::process::exit(1);
    }
    
    let input_file = &args[1];
    let output_file = if args.len() > 2 {
        &args[2]
    } else {
        "output.png"
    };

    // Read HTML file
    let mut file = File::open(input_file).expect("Failed to open HTML file");
    let mut html_content = String::new();
    file.read_to_string(&mut html_content).expect("Failed to read HTML file");

    // Parse HTML
    let dom = parse_document(RcDom::default(), ParseOpts::default())
        .from_utf8()
        .read_from(&mut html_content.as_bytes())
        .unwrap();

    println!("HTML parsed successfully!");

    // Create a Cairo surface for rendering
    let surface = ImageSurface::create(Format::ARgb32, 800, 600).expect("Failed to create surface");
    let context = Context::new(&surface).expect("Failed to create context");

    // Set up Pango for text rendering
    let layout = create_layout(&context);
    layout.set_text("Hello, World!");

    // Render the layout
    context.set_source_rgb(1.0, 1.0, 1.0); // White background
    context.paint().expect("Failed to paint background");

    context.set_source_rgb(0.0, 0.0, 0.0); // Black text
    context.move_to(50.0, 50.0);
    pangocairo::functions::show_layout(&context, &layout);

    // Save the surface to a PNG file
    let mut output_file_handle = File::create(output_file).expect("Failed to create output file");
    surface.write_to_png(&mut output_file_handle).expect("Failed to save PNG");

    println!("Rendering complete! Output saved to {}", output_file);
}