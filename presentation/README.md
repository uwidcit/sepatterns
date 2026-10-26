Design Patterns — 14 slides

Deliverables:
- Design Patterns.pptx: native editable text; only the 28 UML diagrams are images.
- Design Patterns.pdf: 14 pages with selectable prose and code.
- Design Patterns.html: self-contained browser version; print at 100%, no headers/footers, using its CSS page size.
- content.json: slide content and UML model source.

The slide order and pattern selection come from ../Design Patterns.pdf.
Each slide cites the corresponding Refactoring Guru article linked by that PDF.
Code is abbreviated, original teaching pseudocode rather than a complete runnable program. The before examples reconstruct the design problem; articles do not always supply before code.

Local example reuse:
- Adapter: retained the stock XML/JSON analytics case and adapter delegation.
- Bridge: retained the shape/color dimensions and before/after construction.
- Facade: retained the subsystem orchestration and video conversion example.
- Singleton: retained private construction and thread-safe shared access, using the article's database case rather than Config.
- Factory: retained the transport theme, replacing the local simple factory with actual creator subclasses for Factory Method.
- Abstract Factory: retained family-based creation; used the article's furniture case rather than the local carrier case.
- Proxy: retained same-interface delegation and caching; used the article's video-service case rather than the local database case.
Existing PNG slides were reconstructed, not embedded as slide screenshots, to preserve text editability and improve UML notation.

UML uses class compartments, visibility markers, interface stereotypes, hollow inheritance/realization triangles, dashed dependencies, solid navigable associations, and hollow aggregation for Box children. Abstract class names are italic. Diagrams focus on the relationships relevant to each pattern; incidental classes and methods are omitted.

Validation: all PPTX XML and relationship files parsed successfully; 14 slides, 22 native text boxes per slide, 28 UML images. PDF has selectable text on all 14 pages and no text outside page bounds. Layout inspected in rendered PDF. Desktop PowerPoint could not be opened for rendering because the available Windows COM session returned error 80070520.

Rebuild: clear the environment's incompatible PYTHONHOME, then run ../build_slides.py with the installed Python 3.12 (requires pymupdf, reportlab, Pillow).

Styling revision: large black sample-style titles, red/teal problem and solution panels, shaded before/after UML and code headers. UML connectors now use only horizontal and vertical segments, with darker 1.9-point strokes and larger arrowheads. An obstacle-aware router avoids class boxes; every generated connector is checked for orthogonal segments. All 14 revised pages were rendered and inspected; no PDF text falls outside page bounds.
