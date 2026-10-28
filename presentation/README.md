Design Patterns — cover + 14 pattern slides

Deliverables:
- Design Patterns.pptx: native editable text; only the UML diagrams are images.
- Design Patterns.pdf: cover plus 14 pattern pages with selectable prose and code, plus a sidebar outline (bookmarks by category and pattern).
- Design Patterns.html: self-contained browser version with a Download PDF button (use that for bookmarks; browser Print→PDF usually omits the outline). Print at 100%, no headers/footers, using its CSS page size.

Cover frames the deck as a client/module handover: each pattern shows caller dependencies (Client box) versus the module API you hand to another developer.
- content.json: slide content and UML model source.

The slide order and pattern selection come from ../Design Patterns.pdf.
Each slide cites the corresponding Refactoring Guru article linked by that PDF.
Code is abbreviated, original teaching pseudocode rather than a complete runnable program. The before examples reconstruct the design problem; articles do not always supply before code.

Local example reuse:
- Adapter: retained the stock XML/JSON analytics case and adapter delegation.
- Bridge: retained the shape/color dimensions and before/after construction.
- Facade: retained the subsystem orchestration and video conversion example.
- Singleton: retained private construction and thread-safe shared access, using the article's database case rather than Config.
- Factory: retained the local Application / TransportFactory / Plane–Truck–Ship case and problem/solution wording from the Factory Pattern Infographic.
- Abstract Factory: retained the local UPS/DHL carrier families from abstractfactory.png; UML shows methods only on TransportFactory / Transport.
- Proxy: retained the local expensive-database / DatabaseProxy case (caching + lazy init) and problem/solution wording from the Proxy Access Control Infographic.
Existing PNG slides were reconstructed, not embedded as slide screenshots, to preserve text editability and improve UML notation.

UML uses class compartments, visibility markers, interface stereotypes, hollow inheritance/realization triangles, dashed dependencies, solid navigable associations, and hollow aggregation for Box children. Abstract class names are italic. Diagrams focus on the relationships relevant to each pattern; incidental classes and methods are omitted.

Validation: all PPTX XML and relationship files parsed successfully; 14 slides, 22 native text boxes per slide, 28 UML images. PDF has selectable text on all 14 pages and no text outside page bounds. Layout inspected in rendered PDF. Desktop PowerPoint could not be opened for rendering because the available Windows COM session returned error 80070520.

Rebuild: clear the environment's incompatible PYTHONHOME, then run ../build_slides.py with the installed Python 3.12 (requires pymupdf, reportlab, Pillow).

Styling revision: large black sample-style titles, red/teal problem and solution panels, shaded before/after UML and code headers. UML follows the sample/website organization: sibling subclasses sit side-by-side under their parent (Factory Method, Abstract Factory, Proxy, Bridge, Strategy, State, Template Method) so inheritance uses short vertical arrows instead of wrapping around stacked boxes. Dependencies prefer a straight connector when clear (no long diagonal doglegs); inheritance/realization stay orthogonal with inverted-T routes and hollow triangles. All 14 pages rebuilt and inspected.
