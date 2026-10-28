from pathlib import Path
import io, math, zipfile, html, json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
import pymupdf

ROOT=Path(__file__).parent
OUT=ROOT/'presentation'; OUT.mkdir(exist_ok=True)
DATA=[]
def n(name, members, col, row, kind='class'):
    return (name,members,col,row,kind)
def add(title,category,case,desc,problem,solution,before,after,module,pnodes,pedges,snodes,sedges,reuse=''):
    DATA.append(dict(title=title,category=category,case=case,desc=desc,problem=problem,solution=solution,before=before,after=after,module=module,pnodes=pnodes,pedges=pedges,snodes=snodes,sedges=sedges,reuse=reuse))

add('Singleton','Creational','Shared Config across services',
'Ensures a class has only one instance and provides a global point of access to it.',
'• User drives UserService / OrderService / ReportService; each needs Config.\n'
'• Call order is not fixed—any service may run first.\n'
'• Each service copies if config == null: config = new Config() → multiple instances.',
'• User still calls doWork(); services only call Config.getInstance().\n'
'• The null-check and construction live once inside Config.\n'
'• First caller creates it; every service shares that instance.',
'// inside each service (User API unchanged)\nif config == null:\n    config = new Config()\nconfig.load()\n// same guard in UserService, OrderService, ReportService',
'// inside each service (User API unchanged)\nconfig = Config.getInstance()\nconfig.load()\n// same load; guard moved into Config',
'// MODULE — Config singleton (owns the lazy init)\nprivate static instance\nprivate Config(): load()\nstatic getInstance():\n    if instance == null:\n        instance = new Config()\n    return instance',
[n('User','+ run()',1.2,0),
 n('UserService','+ doWork()',0,1),n('OrderService','+ doWork()',1.2,1),n('ReportService','+ doWork()',2.4,1),
 n('Config #1','+ load()',0,2),n('Config #2','+ load()',1.2,2),n('Config #3','+ load()',2.4,2)],
[(0,1,'dep'),(0,2,'dep'),(0,3,'dep'),(1,4,'dep'),(2,5,'dep'),(3,6,'dep')],
[n('User','+ run()',1.2,0),
 n('UserService','+ doWork()',0,1),n('OrderService','+ doWork()',1.2,1),n('ReportService','+ doWork()',2.4,1),
 n('Config','- instance: Config {static}\n- Config()\n+ getInstance(): Config {static}\n+ load()',1.2,2)],
[(0,1,'dep'),(0,2,'dep'),(0,3,'dep'),(1,4,'dep'),(2,4,'dep'),(3,4,'dep')], 'Singleton Pattern_ Thread-Safe Instance Sharing.png')

add('Factory Method','Creational','Plane, truck, and ship transport',
'Provides an interface for creating objects, but lets subclasses decide which class to instantiate.',
'• Client code needs to create different types of objects (e.g. Plane, Truck, Ship).\n'
'• The client contains conditional logic and knows about all concrete classes.\n'
'• Adding a new type requires modifying client code (violates Open/Closed Principle).\n'
'• Object creation logic is scattered and duplicated across the application.\n'
'• Client is tightly coupled to concrete classes.',
'• Define a factory interface/class for creating products (e.g. Transport).\n'
'• Concrete factory decides which concrete product to instantiate.\n'
'• Client code works with the factory and the product interface, not concrete classes.\n'
'• To add a new type, add a new product and update the factory (client code unchanged).\n'
'• Centralizes and encapsulates object creation logic.',
'plane = new Plane(); plane.fly()\ntruck = new Truck(); truck.drive()\nship = new Ship(); ship.sail()\n// three types; three different method names',
'fleet = [factory.create("plane"),\n         factory.create("truck"),\n         factory.create("ship")]\nfor t in fleet: t.transport()\n// same three results; one Transport method',
'// MODULE — creation API for client developers\n// TransportFactory.create(type)\nif type == "plane": return new Plane()\nelif type == "truck": return new Truck()\nelif type == "ship": return new Ship()\n// Plane/Truck/Ship implement Transport.transport()',
[n('Client','+ run()',1,0),n('Plane','+ fly()',0,1),n('Truck','+ drive()',1,1),n('Ship','+ sail()',2,1)],[(0,1,'dep'),(0,2,'dep'),(0,3,'dep')],
[n('Client','+ run()',0,0),n('TransportFactory','+ create(type: String): Transport',1,0),n('Transport','+ transport()',2.5,0,'interface'),n('Plane','+ transport()',1,1),n('Truck','+ transport()',2,1),n('Ship','+ transport()',3,1)],[(0,1,'dep'),(1,2,'dep'),(3,2,'real'),(4,2,'real'),(5,2,'real')], 'Factory Pattern Infographic_ Before and After (1).png')

add('Abstract Factory','Creational','UPS and DHL transport families',
'Create related product families through a factory interface.',
'Client news every carrier concrete and calls drive / sail / fly separately.',
'Pick a family factory; create as Transport; one transport() loop.',
'dt = new DHLTruck(); dt.drive()\nds = new DHLShip();  ds.sail()\ndp = new DHLPlane(); dp.fly()\nut = new UPSTruck(); ut.drive()\nus = new UPSShip();  us.sail()\nup = new UPSPlane(); up.fly()',
'dhl = new DHLFactory()\ndp = dhl.createPlane(); ds = dhl.createShip(); dt = dhl.createTruck()\nups = new UPSFactory()\nup = ups.createPlane(); us = ups.createShip(); ut = ups.createTruck()\nfleet = [dp, ds, dt, up, us, ut]\nfor t in fleet: t.transport()',
'',
# Before: Client between UPS row and DHL row (each product its own box).
[n('Client','',1.5,1),
 n('UPSPlane','',0,0),n('UPSTruck','',1.5,0),n('UPSShip','',3,0),
 n('DHLPlane','',0,2),n('DHLTruck','',1.5,2),n('DHLShip','',3,2)],
[(0,1,'dep'),(0,2,'dep'),(0,3,'dep'),(0,4,'dep'),(0,5,'dep'),(0,6,'dep')],
# After: sample arrangement — factories sandwich TF; products flank Transport; create links.
[n('Client','',0,1),
 n('UPSFactory','',1,0),
 n('TransportFactory','+ createPlane()\n+ createShip()\n+ createTruck()',1,1,'interface'),
 n('DHLFactory','',1,2),
 n('UPSPlane','',2.2,0),n('UPSTruck','',2.9,0),n('UPSShip','',3.6,0),
 n('Transport','+ transport()',2.9,1,'interface'),
 n('DHLPlane','',2.2,2),n('DHLTruck','',2.9,2),n('DHLShip','',3.6,2)],
[(0,1,'dep'),(0,3,'dep'),
 (1,2,'real'),(3,2,'real'),
 (4,7,'real'),(5,7,'real'),(6,7,'real'),(8,7,'real'),(9,7,'real'),(10,7,'real'),
 (1,4,'assoc'),(1,5,'assoc'),(1,6,'assoc'),
 (3,8,'assoc'),(3,9,'assoc'),(3,10,'assoc')], 'abstractfactory.png')

add('Builder','Creational','Houses with optional features',
'Separate construction steps from the representation being assembled.',
'• House grows telescoping constructors (rooms/doors/windows + pool/trees/…).\n'
'• Client passes long positional bool lists—unclear which flag is which.\n'
'• Adding a feature forces new overloads and updates every call site.',
'• HouseBuilder names each step; ConcreteHouseBuilder adds extras.\n'
'• HouseDirector encodes recipes (simple / family); Client can also chain steps.\n'
'• Same houses; readable construction; product is House.',
'houseA = new House(1, 1, 1)\nhouseB = new House(2, 2, 1, false, false, true, true)\nhouseC = new House(4, 3, 3, true, false, false, true)\nhouseD = new House(2, 1, 2, false, true, false, false)\nhouseE = new House(6, 4, 5, true, true, true, true)\n// five houses; magic bool positions',
'director = new HouseDirector()\nhouseA = director.buildSimpleHouse(new ConcreteHouseBuilder())\nhouseB = new ConcreteHouseBuilder().addWindow().addWindow()\n    .addDoor().addDoor().addRoom().addStatues().addGarden().getResult()\nhouseC = director.buildFamilyHouse(new ConcreteHouseBuilder())\nhouseD = new ConcreteHouseBuilder().addWindow().addWindow()\n    .addDoor().addRoom().addRoom().addTrees().getResult()\nhouseE = new ConcreteHouseBuilder()\n    .addWindow().addWindow().addWindow().addWindow().addWindow().addWindow()\n    .addDoor().addDoor().addDoor().addDoor()\n    .addRoom().addRoom().addRoom().addRoom().addRoom()\n    .addPool().addTrees().addStatues().addGarden().getResult()\n// same five houses; named steps / director recipes',
'',
[n('Client','+ buildHouses()',0,0),
 n('House','+ House(windows, doors, rooms)\n'
  '+ House(windows, doors, rooms, pool)\n'
  '+ House(windows, doors, rooms, pool, tree)\n'
  '+ House(windows, doors, rooms, pool, tree, statues)\n'
  '+ House(windows, doors, rooms, pool, tree, statues, garden)',1.2,0)],
[(0,1,'dep')],
[n('Client','+ buildHouses()',0,0),
 n('HouseBuilder','+ addRoom()\n+ addDoor()\n+ addWindow()\n+ getResult(): House',1,0,'interface'),
 n('HouseDirector','+ buildSimpleHouse(b)\n+ buildFamilyHouse(b)',2.6,0),
 n('ConcreteHouseBuilder','+ addStatues()\n+ addTrees()\n+ addPool()\n+ addGarden()',1,1),
 n('House','+ rooms: int\n+ doors: int\n+ windows: int',2.6,1)],
[(0,1,'dep'),(0,2,'dep'),(2,1,'dep'),(3,1,'real'),(3,4,'assoc')], 'builder.png')

add('Adapter','Structural','XML stock data and JSON analytics',
'Translate an existing interface into the interface a client expects.',
'The stock app supplies XML; the analytics library requires JSON.',
'Adapter inherits AnalyticsService and composes JsonAnalyticsLibrary; converts then delegates.',
'xml = provider.getStockData()\njson = convertXmlToJson(xml)\nreport = library.analyze(json)\n// same stock report; client does the conversion',
'xml = provider.getStockData()\nreport = adapter.analyze(xml)\n// same stock report; adapter owns the conversion',
'// MODULE — AnalyticsService API for client developers\n// XmlAnalyticsAdapter extends AnalyticsService\n// composes library: JsonAnalyticsLibrary\n// analyze(xml):\n//   json = convert(xml)\n//   return library.analyze(json)',
[n('Client','+ analyzeStocks()',0,0),n('StockDataProvider','+ getStockData(): XML',0,1),n('JsonAnalyticsLibrary','+ analyze(json): Report',2,1)],[(0,1,'dep'),(0,2,'dep')],
[n('Client','- analytics: AnalyticsService\n+ analyzeStocks()',0,0),
 n('AnalyticsService','+ analyze(xml): Report {abstract}',1.5,0,'abstract'),
 n('XmlAnalyticsAdapter','- library: JsonAnalyticsLibrary\n+ analyze(xml): Report\n- convert(xml): JSON',1.5,1),
 n('JsonAnalyticsLibrary','+ analyze(json): Report',3.2,1)],
[(0,1,'assoc'),(2,1,'gen'),(2,3,'compose')], 'adapter.png')

add('Bridge','Structural','Shapes and colors',
'Separate two independent dimensions so both can evolve independently.',
'Each shape/color combination requires another subclass.', 'Shapes hold a Color reference instead of encoding color in inheritance.',
'new RedCircle().draw()\nnew BlueSquare().draw()\n// red circle + blue square; one class per combo',
'shapes = [new Circle(new Red()),\n          new Square(new Blue())]\nfor s in shapes: s.draw()\n// same two drawings; compose shape × color',
'// MODULE — Shape API for client developers\n// Circle.draw()\ncolor.apply()\nrenderCircleGeometry()\n// color and geometry vary independently',
[n('RedCircle','+ draw()',0,0),n('BlueCircle','+ draw()',1.2,0),n('RedSquare','+ draw()',2.4,0),
 n('Client','+ render()',1.2,1)],[(3,0,'dep'),(3,1,'dep'),(3,2,'dep')],
[n('Client','+ render()',0,0),n('Shape','- color: Color\n+ draw() {abstract}',1.2,0,'abstract'),n('Color','+ apply()',3.2,0,'interface'),n('Circle','+ draw()',0.7,1),n('Square','+ draw()',1.7,1),n('Red','+ apply()',2.7,1),n('Blue','+ apply()',3.7,1)],[(0,1,'dep'),(1,2,'compose'),(3,1,'gen'),(4,1,'gen'),(5,2,'real'),(6,2,'real')], 'bridge.png')

add('Facade','Structural','Video conversion subsystem',
'Expose a simple entry point to a complex subsystem.',
'Every client coordinates codecs, bitrate conversion, and audio repair.', 'A facade orchestrates the subsystem behind one conversion call.',
'codec = CodecFactory.extract(file)\nraw = BitrateReader.read(file, codec)\nvideo = BitrateReader.convert(raw, mp4)\nresult = AudioMixer.fix(video)\n// export file as mp4 via subsystem steps',
'result = new VideoConverter().convert(file, "mp4")\n// same mp4 export; one facade call',
'// MODULE — VideoConverter facade API for client developers\n// VideoConverter.convert(file, format)\nsource = CodecFactory.extract(file)\nraw = BitrateReader.read(file, source)\nvideo = BitrateReader.convert(raw, codecFor(format))\nreturn AudioMixer.fix(video)',
[n('Client','+ export()',1,0),n('CodecFactory','+ extract(file)',0,1),n('BitrateReader','+ read()\n+ convert()',1,1),n('AudioMixer','+ fix(video)',2,1)],[(0,1,'dep'),(0,2,'dep'),(0,3,'dep')],
[n('Client','+ export()',0,0),n('VideoConverter','+ convert(file, format): File',2,0),n('CodecFactory','+ extract(file)',0,1),n('BitrateReader','+ read()\n+ convert()',1,1),n('AudioMixer','+ fix(video)',2,1)],[(0,1,'dep'),(1,2,'dep'),(1,3,'dep'),(1,4,'dep')], 'facade.png')

add('Proxy','Structural','Expensive database service with caching',
'A stand-in object that controls access to a real service without changing its interface.',
'• The real service is expensive to create or use (e.g. database, remote API, large object).\n'
'• Repeated queries can be slow and waste resources.\n'
'• The client may need to handle initialization or access control logic.\n'
'• We want extra behavior (caching, logging, access control) without changing client code.',
'• Introduce a proxy that implements the same interface as the real service.\n'
'• The proxy controls access, adding lazy init, caching, logging, or access control.\n'
'• Client uses the same interface—only the class it instantiates changes.\n'
'• Adds: caching, lazy initialization, optional access control and logging.',
'db = new ExpensiveDatabaseService()\nr1 = db.query("users")\nr2 = db.query("users")\n// two "users" results; two expensive hits',
'db = new DatabaseProxy()\nr1 = db.query("users")\nr2 = db.query("users")\n// same two "users" results; second from cache',
'// MODULE — DatabaseService API for client developers\n// DatabaseProxy.query(key)\nif cache.contains(key): return cache[key]\nif realService == null: realService = new RealDatabaseService()\nresult = realService.query(key)\ncache[key] = result; return result',
[n('Client','+ run()',0,0),n('ExpensiveDatabaseService','+ ExpensiveDatabaseService()\n+ query(key): Result',2,1)],[(0,1,'dep')],
[n('Client','+ run()',0,0),n('DatabaseService','+ query(key: String): Result',1.5,0,'interface'),n('DatabaseProxy','- realService: DatabaseService\n- cache: Map\n+ query(key): Result\n- getRealService()',0.5,1),n('RealDatabaseService','+ query(key): Result',2.5,1)],[(0,2,'dep'),(2,1,'real'),(3,1,'real'),(2,3,'assoc')], 'Proxy Pattern_ Access Control Infographic.png')

add('Composite','Structural','Boxes containing products and boxes',
'Treat individual objects and recursive groups through one interface.',
'Pricing code distinguishes products from nested boxes repeatedly.', 'A box sums child prices; each child follows the same contract.',
'total = 0\nfor item in order.contents:\n    if item is Product: total += item.price\n    else: total += priceNestedBox(item)\n// price of product + nested box',
'total = order.getPrice()\n// same total; one getPrice() on OrderItem',
'// MODULE — OrderItem API for client developers\n// Box.getPrice()\ntotal = 0\nfor child in children:\n    total += child.getPrice()\nreturn total',
[n('Client','+ total(box)',1,0),
 n('Product','+ price: Money',0.5,1),n('Box','+ contents: List',1.5,1)],[(0,1,'dep'),(0,2,'dep')],
# Client left of OrderItem on top; Product/Box only under OrderItem (no cross).
[n('Client','+ total(item)',0,0),
 n('OrderItem','+ getPrice(): Money',2.2,0,'interface'),
 n('Product','- price: Money\n+ getPrice(): Money',1.6,1.25),
 n('Box','- children: OrderItem[0..*]\n+ getPrice(): Money\n+ add(item)',2.8,1.25)],
[(0,1,'dep'),(2,1,'real'),(3,1,'real'),(3,1,'aggregate')])

add('Template Method','Behavioral','Mining PDF and CSV documents',
'Fix an algorithm’s order while subclasses implement selected steps.',
'Format-specific miners duplicate the processing and reporting pipeline.', 'Move the sequence into a base method; override extraction only.',
'pdfReport = analyze(pdf.extract(pdfPath))\ncsvReport = analyze(csv.extract(csvPath))\n// two reports; client repeats extract+analyze',
'miners = [new PdfMiner(), new CsvMiner()]\nreports = []\nfor m in miners: reports.add(m.mine(pathFor(m)))\n// same two reports; one mine() pipeline each',
'// MODULE — DataMiner.mine API for client developers\n// DataMiner.mine(path): fixed sequence\ndata = extract(path)\nreturn analyze(data)\n// PdfMiner.extract(path): return parsePdf(path)',
[n('Client','+ run()',1,0),n('PdfMiner','+ extract(path)\n+ analyze(data)',0,1),n('CsvMiner','+ extract(path)\n+ analyze(data)',2,1)],[(0,1,'dep'),(0,2,'dep')],
[n('Client','+ run()',0,0),n('DataMiner','+ mine(path): Report\n# extract(path): Data {abstract}\n# analyze(data): Report',1.5,0,'abstract'),n('PdfMiner','# extract(path): Data',1,1),n('CsvMiner','# extract(path): Data',2.5,1)],[(0,1,'dep'),(2,1,'gen'),(3,1,'gen')])

add('Strategy','Behavioral','Navigation route algorithms',
'Make alternative algorithms interchangeable through a shared contract.',
'A navigator grows conditionals for road, walking, and transit routes.', 'Delegate routing to a strategy selected by the client.',
'road = roadRoute(a, b)\nwalk = walkRoute(a, b)\ntransit = transitRoute(a, b)\n// three routes; client branches per mode',
'for s in [new RoadRoute(), new WalkingRoute(),\n          new TransitRoute()]:\n    navigator.setStrategy(s)\n    routes.add(navigator.buildRoute(a, b))\n// same three routes; one buildRoute() API',
'// MODULE — Navigator API for client developers\n// Navigator.buildRoute(a, b)\nreturn strategy.buildRoute(a, b)\n// WalkingRoute builds pedestrian paths',
[n('Client','+ navigate()',0,0),n('Navigator','- mode: String\n+ buildRoute(a, b): Route',2,0)],[(0,1,'dep')],
[n('Client','+ navigate()',0,0),n('Navigator','- strategy: RouteStrategy\n+ setStrategy(s)\n+ buildRoute(a, b): Route',1,0),n('RouteStrategy','+ buildRoute(a, b): Route',2.5,0,'interface'),n('RoadRoute','+ buildRoute(a, b): Route',1.5,1),n('WalkingRoute','+ buildRoute(a, b): Route',2.5,1),n('TransitRoute','+ buildRoute(a, b): Route',3.5,1)],[(0,1,'dep'),(1,2,'assoc'),(3,2,'real'),(4,2,'real'),(5,2,'real')])

add('State','Behavioral','Document publication workflow',
'Delegate behavior to an object representing the current state.',
'Publication rules accumulate in a switch over document status.', 'Each state handles publish and can transition the document.',
'doc.status = "draft"\ndoc.status = "moderation"   // submit\ndoc.status = "published"    // admin approve\n// draft → moderation → published via status ifs',
'doc = new Document(new Draft())\ndoc.publish(user)   // enters moderation\ndoc.publish(admin)  // becomes published\n// same draft → moderation → published path',
'// MODULE — Document.publish API for client developers\n// Moderation.publish(doc, user)\nif user.isAdmin:\n    doc.changeState(new Published())\n// Published.publish(...) does nothing',
[n('Client','+ publishDoc()',0,0),n('Document','- status: String\n+ publish(user)',2,0)],[(0,1,'dep')],
[n('Client','+ publishDoc()',0,0),n('Document','- state: PublicationState\n+ publish(user)\n+ changeState(s)',1,0),n('PublicationState','+ publish(doc, user)',2.5,0,'interface'),n('Draft','+ publish(doc, user)',1.5,1),n('Moderation','+ publish(doc, user)',2.5,1),n('Published','+ publish(doc, user)',3.5,1)],[(0,1,'dep'),(1,2,'assoc'),(3,2,'real'),(4,2,'real'),(5,2,'real')])

add('Observer','Behavioral','Editor events notify logging and email',
'Notify registered subscribers when a publisher emits an event.',
'Editor logic directly invokes concrete logging and email services.', 'Publish an event; subscribers handle their own reactions.',
'editor.saveFile()\nlogger.write(file.name)\nmailer.send(file.name)\n// save + log + email; client wires reactions',
'events.subscribe("save", new LogListener())\nevents.subscribe("save", new EmailListener())\neditor.saveFile()\n// same save + log + email; listeners react',
'// MODULE — EventManager API for client developers\n// EventManager.notify(type, data)\nfor listener in listeners[type]:\n    listener.update(data)\n// Editor.saveFile(): write(); events.notify("save", name)',
[n('Client','+ save()',0,0),n('Editor','+ saveFile()',1,0),n('Logger','+ write(name)',0,1),n('Mailer','+ send(name)',2,1)],[(0,1,'dep'),(1,2,'dep'),(1,3,'dep')],
[n('Client','+ setup()',0,0),n('Editor','- events: EventManager\n+ saveFile()',1,0),n('EventManager','- listeners: EventListener[0..*]\n+ subscribe(type, listener)\n+ notify(type, data)',2,0),n('EventListener','+ update(data)',3,0,'interface'),n('LogListener','+ update(data)',2,1),n('EmailListener','+ update(data)',3,1)],[(0,1,'dep'),(0,2,'dep'),(1,2,'assoc'),(2,3,'assoc'),(4,3,'real'),(5,3,'real')])

add('Command','Behavioral','Undoable text-editor actions',
'Represent a request as an object that can be invoked and undone.',
'Buttons and shortcuts duplicate editing actions without shared undo.', 'Bind both triggers to a command; store successful edits in history.',
'pasteButton.click()  // editor.insert(text)\nshortcut.press()     // editor.insert(text)\n// paste from two triggers; logic duplicated, no undo',
'paste = new PasteCommand(editor, text)\npasteButton.bind(() => app.execute(paste))\nshortcut.bind(() => app.execute(paste))\npasteButton.click(); shortcut.press()\n// same two pastes via shared command',
'// MODULE — Command API for client developers\n// PasteCommand.execute()\nbackup = editor.text; editor.insert(text)\nreturn true  // app records command in history\n// undo(): editor.text = backup',
[n('Client','+ trigger()',1,0),n('PasteButton','+ click()',0,1),n('Shortcut','+ press()',1,1),n('Editor','+ insert(text)',2,1)],[(0,1,'dep'),(0,2,'dep'),(1,3,'dep'),(2,3,'dep')],
[n('Client','+ trigger()',0,0),n('Application','- history: Command[*]\n+ execute(command)\n+ undo()',1,0),n('Command','+ execute(): Boolean\n+ undo()',2.5,0,'interface'),n('PasteCommand','- editor: Editor\n- backup: String\n+ execute(): Boolean\n+ undo()',2,1),n('Editor','+ text: String\n+ insert(text)',0.5,1)],[(0,1,'dep'),(1,2,'assoc'),(3,2,'real'),(3,4,'assoc')])

# UML rendering: ordinary three-compartment classes, interface stereotypes,
# hollow generalization/realization triangles, open dependencies, navigable
# associations, and hollow aggregation at the whole (Box) end.
# Layout rule: place sibling subclasses side-by-side under their parent so
# inheritance uses short vertical arrows (sample / refactoring.guru style).
INK='#172B4D'; BLUE='#1662C4'; RED='#B14747'; GREEN='#13746A'
def uml(nodes,edges,path,compact=False):
    import heapq
    CW,CH=660,270
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(CW,CH))
    cols=sorted({float(n[2]) for n in nodes})
    span=(max(cols)-min(cols)+1) if cols else 1
    pitch=min(220,(CW-20)/span)
    box_w=min(198 if not compact else 168,pitch-12 if compact else pitch-16)
    max_row=max(float(n[3]) for n in nodes) or 1
    row_pitch=(CH-28)/(max_row+0.9)
    line_h=9 if compact else 11
    header_h=18 if compact else 20
    boxes=[]; centers=[]
    for name,members,col,row,kind in nodes:
        x=10+float(col)*pitch+(pitch-box_w)/2
        # Empty members → single-compartment (name-only) box; multi-line names allowed.
        if not (members or '').strip():
            h=max(header_h+4, 6+len(name.split('\n'))*line_h)
        else:
            h=header_h+8+len(members.split('\n'))*line_h
        y=CH-14-float(row)*row_pitch
        boxes.append((x,y,box_w,h)); centers.append((x+box_w/2,y-h/2))
    MARGIN=7
    def inflate(box,m=MARGIN):
        x,y,w,h=box; return (x-m,y+m,w+2*m,h+2*m)
    def segment_hits(u,v,ignore=()):
        for i,box in enumerate(boxes):
            if i in ignore: continue
            x,y,w,h=inflate(box)
            if abs(u[0]-v[0])<0.01:
                if x<u[0]<x+w and max(min(u[1],v[1]),y-h)<min(max(u[1],v[1]),y): return True
            else:
                if y-h<u[1]<y and max(min(u[0],v[0]),x)<min(max(u[0],v[0]),x+w): return True
        return False
    def clear_path(pts,ignore=()):
        return all(not segment_hits(u,v,ignore) for u,v in zip(pts,pts[1:]))
    def line_hits(u,v,ignore=()):
        # Axis-aligned or diagonal: sample so diagonal deps can stay clear of boxes.
        length=math.hypot(v[0]-u[0],v[1]-u[1]) or 1
        steps=max(10,int(length/3))
        for i in range(1,steps):
            t=i/steps
            px=u[0]+(v[0]-u[0])*t; py=u[1]+(v[1]-u[1])*t
            for j,box in enumerate(boxes):
                if j in ignore: continue
                x,y,w,h=inflate(box)
                if x<px<x+w and y-h<py<y: return True
        return False
    def stub(point,box,dist=9):
        x,y,w,h=box; px,py=point
        if abs(px-x)<0.5: return (px-dist,py)
        if abs(px-(x+w))<0.5: return (px+dist,py)
        if abs(py-y)<0.5: return (px,py+dist)
        return (px,py-dist)
    def top_anchor(box,frac=0.5):
        x,y,w,h=box; return (x+w*frac,y)
    def bottom_anchor(box,frac=0.5):
        x,y,w,h=box; return (x+w*frac,y-h)
    def side_anchor(box,toward_x):
        x,y,w,h=box
        return (x+w if toward_x>=x+w/2 else x, y-h/2)
    def simplify(pts):
        clean=[]
        for pt in pts:
            pt=(round(pt[0],1),round(pt[1],1))
            if clean and clean[-1]==pt: continue
            while len(clean)>1 and ((clean[-2][0]==clean[-1][0]==pt[0]) or (clean[-2][1]==clean[-1][1]==pt[1])):
                clean.pop()
            clean.append(pt)
        return clean
    def pick_anchors(ai,bi,t):
        A,B=boxes[ai],boxes[bi]
        ax,ay=centers[ai]; bx,by=centers[bi]
        if t in ('aggregate','compose'):
            # Diamond at whole (ai). PDF y grows up — smaller y is lower on screen.
            # When whole sits below the part (Composite Box under OrderItem),
            # pin both anchors on the outer vertical side so the loop does not
            # cross realization into the parent's bottom edge.
            if ay<by-8:
                if ax>=bx:
                    return (A[0]+A[2],ay),(B[0]+B[2],by)
                return (A[0],ay),(B[0],by)
            if abs(ax-bx)>8:
                return ((A[0]+A[2],ay) if ax<bx else (A[0],ay),
                        (B[0],by) if ax<bx else (B[0]+B[2],by))
            return ((bottom_anchor(A) if ay>by else top_anchor(A)),
                    (top_anchor(B) if ay>by else bottom_anchor(B)))
        # Inheritance / realization: arrow into the parent. Children may sit
        # below (into bottom) or above (into top) — Abstract Factory sample.
        if t in ('gen','real'):
            siblings=[i for i,j,tt in edges if j==bi and tt in ('gen','real')]
            if len(siblings)>1 and ai in siblings:
                idx=siblings.index(ai); n=len(siblings)
                frac=0.30+0.40*(idx/(n-1))
            else:
                frac=0.5
            if by>=ay-8:  # child below / level → parent bottom
                return top_anchor(A,0.5), bottom_anchor(B,frac)
            return bottom_anchor(A,0.5), top_anchor(B,frac)  # child above → parent top
        # Fan-out tree only: several children below share bottom → top anchors
        # (Factory before: Application down to Plane / Truck / Ship). A single
        # diagonal dependency must not take this path — it produces a long L.
        if ay>by+20:
            siblings=[i for i,j,tt in edges if i==ai and tt==t and centers[j][1]<ay-10]
            nearly_under=abs(ax-bx)<=max(box_w*0.55,pitch*0.35)
            if len(siblings)>1 or nearly_under:
                frac=0.5
                if len(siblings)>1 and bi in siblings:
                    idx=siblings.index(bi); n=len(siblings)
                    frac=0.28+0.44*(idx/(n-1))
                return bottom_anchor(A,frac), top_anchor(B,0.5)
        # Fan-out upward: Client under modules (Composite / Bridge problem).
        if by>ay+20 and t in ('dep','assoc'):
            siblings=[i for i,j,tt in edges if i==ai and tt==t and centers[j][1]>ay+10]
            nearly_over=abs(ax-bx)<=max(box_w*0.55,pitch*0.35)
            if len(siblings)>1 or nearly_over:
                frac=0.5
                if len(siblings)>1 and bi in siblings:
                    idx=siblings.index(bi); n=len(siblings)
                    frac=0.28+0.44*(idx/(n-1))
                return top_anchor(A,frac), bottom_anchor(B,0.5)
        # Facing sides for side-by-side or diagonal pairs (avoids bottom→across L).
        if abs(ax-bx)>8:
            return ((A[0]+A[2],ay) if ax<bx else (A[0],ay),
                    (B[0],by) if ax<bx else (B[0]+B[2],by))
        return ((bottom_anchor(A) if ay>by else top_anchor(A)),
                (top_anchor(B) if ay>by else bottom_anchor(B)))
    def try_routes(a,b,ai,bi):
        A,B=boxes[ai],boxes[bi]
        ax,ay=centers[ai]; bx,by=centers[bi]
        candidates=[]
        if abs(a[0]-b[0])<14:
            x=round((a[0]+b[0])/2,1)
            candidates.append([(x,a[1]),(x,b[1])])
        if abs(a[1]-b[1])<14:
            y=round((a[1]+b[1])/2,1)
            candidates.append([(a[0],y),(b[0],y)])
        # Inverted-T / sample tree: drop from parent, run a shared bus, drop to child top.
        if ay>by+16:
            bus_y=round((a[1]+b[1])/2,1)
            candidates.append([a,(a[0],bus_y),(b[0],bus_y),b])
            candidates.insert(0,[a,(a[0],bus_y),(b[0],bus_y),b])
        candidates.append([a,(b[0],a[1]),b])
        candidates.append([a,(a[0],b[1]),b])
        for gut_x in (A[0]-12, A[0]+A[2]+12, B[0]-12, B[0]+B[2]+12, (ax+bx)/2):
            gut_x=max(6,min(CW-6,gut_x))
            lift=10 if a[1]<b[1] else -10
            candidates.append([a,(a[0],a[1]+lift),(gut_x,a[1]+lift),(gut_x,b[1]),b])
            candidates.append([a,(gut_x,a[1]),(gut_x,b[1]),b])
        # Prefer routing above the top of both boxes so mid-row neighbors are not crossed.
        over=max(A[1],B[1])+16
        if over<CH-4:
            candidates.append([a,(a[0],over),(b[0],over),b])
        under=min(A[1]-A[3],B[1]-B[3])-16
        if under>4:
            candidates.append([a,(a[0],under),(b[0],under),b])
        for gut_y in (A[1]+12, A[1]-A[3]-12, B[1]+12, B[1]-B[3]-12, (ay+by)/2):
            gut_y=max(6,min(CH-6,gut_y))
            candidates.append([a,(a[0],gut_y),(b[0],gut_y),b])
        if by>ay:
            # Prefer the gutter toward open space (right first) so stacked children
            # do not wrap around the far left border of the diagram.
            gutters=[A[0]+A[2]+14]
            # If a neighboring box sits to the right, aim for the channel between them.
            for j,Bb in enumerate(boxes):
                if j in (ai,bi): continue
                if Bb[0]>A[0]+A[2]-2 and abs((Bb[1]-Bb[3]/2)-(ay))<row_pitch:
                    gutters.insert(0,(A[0]+A[2]+Bb[0])/2)
            gutters.append(A[0]-14)
            for gut_x in gutters:
                gut_x=max(6,min(CW-6,gut_x))
                lift=min(A[1]+12, (ay+by)/2)
                bus=max(B[1]-B[3]-14, lift+8)
                candidates.append([a,(a[0],lift),(gut_x,lift),(gut_x,bus),(b[0],bus),b])
                ps=side_anchor(B,gut_x)
                candidates.append([a,(a[0],lift),(gut_x,lift),(gut_x,ps[1]),ps])
        scored=[]
        for pts in candidates:
            pts=simplify(pts)
            if len(pts)<2: continue
            if not all(abs(u[0]-v[0])<0.01 or abs(u[1]-v[1])<0.01 for u,v in zip(pts,pts[1:])): continue
            if not clear_path(pts,ignore={ai,bi}): continue
            bends=max(0,len(pts)-2)
            length=sum(abs(u[0]-v[0])+abs(u[1]-v[1]) for u,v in zip(pts,pts[1:]))
            # Penalize long doglegs: short stub then a much longer crosspiece.
            dogleg=0
            if len(pts)>=3:
                segs=[abs(u[0]-v[0])+abs(u[1]-v[1]) for u,v in zip(pts,pts[1:])]
                if segs[0]<35 and max(segs[1:])>segs[0]*2.5:
                    dogleg=1
            scored.append((dogleg,bends,length,pts))
        if scored:
            scored.sort(); return scored[0][3]
        return None
    def route_astar(a,b,ai,bi):
        aa=stub(a,boxes[ai]); bb=stub(b,boxes[bi])
        xs={0,CW,a[0],b[0],aa[0],bb[0]}; ys={0,CH,a[1],b[1],aa[1],bb[1]}
        for x,y,w,h in boxes:
            xs.update((x-MARGIN-4,x+w+MARGIN+4,x-14,x+w+14,x+w/2))
            ys.update((y+MARGIN+4,y-h-MARGIN-4,y+14,y-h-14,y-h/2))
        xs=sorted({round(v,1) for v in xs if 0<=v<=CW})
        ys=sorted({round(v,1) for v in ys if 0<=v<=CH})
        def clear(u,v):
            return not segment_hits(u,v,ignore={ai,bi})
        def near(val,axis):
            grid=xs if axis=='x' else ys
            return min(range(len(grid)), key=lambda i: abs(grid[i]-val))
        initial=(near(aa[0],'x'),near(aa[1],'y'),-1)
        target=(near(bb[0],'x'),near(bb[1],'y'))
        queue=[(0,0,initial)]; cost={initial:0}; prev={}; finish=None
        while queue:
            _,g,state=heapq.heappop(queue)
            if g!=cost[state]: continue
            xi,yi,last=state
            if (xi,yi)==target: finish=state; break
            for dx,dy,direction in ((1,0,0),(-1,0,0),(0,1,1),(0,-1,1)):
                nx,ny=xi+dx,yi+dy
                if not (0<=nx<len(xs) and 0<=ny<len(ys)): continue
                u=(xs[xi],ys[yi]); v=(xs[nx],ys[ny])
                if not clear(u,v): continue
                ng=g+abs(u[0]-v[0])+abs(u[1]-v[1])+(20 if last not in (-1,direction) else 0)
                nxt=(nx,ny,direction)
                if ng<cost.get(nxt,float('inf')):
                    cost[nxt]=ng; prev[nxt]=state
                    heur=abs(v[0]-bb[0])+abs(v[1]-bb[1])
                    heapq.heappush(queue,(ng+heur,ng,nxt))
        if finish is None: raise RuntimeError('No UML route found')
        pts=[]; cur=finish
        while cur!=initial:
            pts.append((xs[cur[0]],ys[cur[1]])); cur=prev[cur]
        return simplify([a,aa]+list(reversed(pts))+[bb,b])
    def join_orthogonal(a,pts,b):
        # Force end caps onto the chosen anchors with HV/VH stubs only.
        if not pts:
            if abs(a[0]-b[0])<0.01 or abs(a[1]-b[1])<0.01: return [a,b]
            return [a,(b[0],a[1]),b]
        mid=list(pts)
        if mid[0]!=a:
            if abs(a[0]-mid[0][0])>0.01 and abs(a[1]-mid[0][1])>0.01:
                mid=[(a[0],mid[0][1])]+mid if abs(a[1]-mid[0][1])<=abs(a[0]-mid[0][0]) else [(mid[0][0],a[1])]+mid
            mid=[a]+mid
        if mid[-1]!=b:
            if abs(b[0]-mid[-1][0])>0.01 and abs(b[1]-mid[-1][1])>0.01:
                mid=mid+[(b[0],mid[-1][1])] if abs(b[1]-mid[-1][1])<=abs(b[0]-mid[-1][0]) else mid+[(mid[-1][0],b[1])]
            mid=mid+[b]
        return simplify(mid)
    def on_vertical_side(pt,box):
        x,y,w,h=box
        return abs(pt[0]-x)<0.5 or abs(pt[0]-(x+w))<0.5
    def route(a,b,ai,bi,t='dep'):
        # Straight connector only for side-facing deps/assocs (Singleton-style
        # diagonal pairs). Bottom→top fan-outs keep orthogonal inverted-T trees.
        if (t in ('dep','assoc') and on_vertical_side(a,boxes[ai]) and on_vertical_side(b,boxes[bi])
                and not line_hits(a,b,{ai,bi})):
            return [a,b]
        # Fan-out from a parent above: short inverted-T into each child's top.
        if t=='dep' and centers[ai][1]>centers[bi][1]+20:
            siblings=[i for i,j,tt in edges if i==ai and tt==t and centers[j][1]<centers[ai][1]-10]
            if len(siblings)>1:
                bus=round((a[1]+b[1])/2,1)
                pts=simplify([a,(a[0],bus),(b[0],bus),b])
                if clear_path(pts,ignore={ai,bi}) or abs(a[0]-b[0])<box_w:
                    return pts
                # Nearly under: drop straight with a tiny jog.
                if abs(a[0]-b[0])<box_w*0.7:
                    return simplify([a,(b[0],a[1]),b])
        # Composite aggregation/composition: from whole's right, up above the
        # parent, into the parent's top — clears Client→parent side deps and
        # realization into the parent's bottom. PDF y grows up.
        if t in ('aggregate','compose') and centers[ai][1]<centers[bi][1]-8:
            A,B=boxes[ai],boxes[bi]
            a=(A[0]+A[2],centers[ai][1])
            b=top_anchor(B,0.82)
            over=min(CH-10, B[1]+26)
            gut=min(CW-10, max(A[0]+A[2],B[0]+B[2])+36)
            return simplify([a,(gut,a[1]),(gut,over),(b[0],over),b])
        simple=try_routes(a,b,ai,bi)
        if simple is not None:
            return join_orthogonal(a,simple,b)
        try:
            return join_orthogonal(a,route_astar(a,b,ai,bi),b)
        except RuntimeError:
            # Factory→product create links must still draw (sample curved fans).
            if t not in ('assoc','aggregate','compose'):
                raise
            over=max(boxes[ai][1],boxes[bi][1])+18
            under=min(boxes[ai][1]-boxes[ai][3],boxes[bi][1]-boxes[bi][3])-18
            mid=(a[1]+b[1])/2
            for y in (over,under,mid):
                pts=simplify([a,(a[0],y),(b[0],y),b])
                if clear_path(pts,ignore={ai,bi}):
                    return pts
            gut=max(boxes[ai][0]+boxes[ai][2],boxes[bi][0])+14
            return simplify([a,(gut,a[1]),(gut,b[1]),b])
    def inheritance_path(a,b,ai,bi):
        # Inverted-T / upright-T so the hollow triangle always meets the parent
        # on a horizontal edge (bottom when child is below, top when above).
        # Keep the bus clearly between the boxes (never level with a top-row dep).
        lo,hi=min(a[1],b[1]),max(a[1],b[1])
        bus=round(lo+(hi-lo)*0.45,1)
        for bus_y in (bus, round(lo+(hi-lo)*0.35,1), round(lo+(hi-lo)*0.55,1)):
            pts=simplify([a,(a[0],bus_y),(b[0],bus_y),b])
            if clear_path(pts,ignore={ai,bi}): return pts
        return simplify([a,(a[0],bus),(b[0],bus),b])
    def is_orthogonal(pts):
        return all(abs(u[0]-v[0])<0.01 or abs(u[1]-v[1])<0.01 for u,v in zip(pts,pts[1:]))
    # Boxes first so composition diamonds / arrowheads paint on top and stay visible.
    c.setLineWidth(1.15 if compact else 1.25)
    name_fs=9 if compact else 10
    body_fs=7.5 if compact else 8.5
    for (name,members,col,row,kind),(x,y,w,h) in zip(nodes,boxes):
        c.setFillColor(white); c.rect(x,y-h,w,h,fill=1,stroke=1)
        c.setStrokeColor(HexColor('#17212E'))
        c.setFillColor(HexColor(INK))
        if not (members or '').strip():
            c.setFillColor(HexColor('#EBEEF4')); c.rect(x,y-h,w,h,fill=1,stroke=1)
            c.setFillColor(HexColor(INK))
            lines=name.split('\n')
            fs=min(name_fs,(w-8)/(max(max(len(L) for L in lines),1)*.54))
            c.setFont('Helvetica-Bold',fs)
            top=y-4-(h-len(lines)*line_h)/2
            for i,L in enumerate(lines):
                c.drawCentredString(x+w/2,top-i*line_h-fs*0.75,L)
            continue
        c.setFillColor(HexColor('#DFE5F0' if kind=='interface' else '#EBEEF4'))
        c.rect(x,y-header_h,w,header_h,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#17212E')); c.line(x,y-header_h,x+w,y-header_h)
        label=('<<interface>> ' if kind=='interface' else '')+name
        c.setFillColor(HexColor(INK))
        c.setFont('Helvetica-BoldOblique' if kind=='abstract' else 'Helvetica-Bold',
                  min(name_fs,(w-10)/(max(len(label),1)*.54)))
        c.drawCentredString(x+w/2,y-header_h+5,label)
        attrs=[s for s in members.split('\n') if '(' not in s]
        ops=[s for s in members.split('\n') if '(' in s]
        yy=y-header_h-line_h; c.setFont('Courier',body_fs)
        for s in attrs: c.drawString(x+5,yy,s); yy-=line_h
        c.line(x,yy+6,x+w,yy+6)
        for s in ops:
            size=min(body_fs,(w-12)/(max(len(s),1)*.55)); c.setFont('Courier',size)
            c.drawString(x+5,yy-3,s)
            if '{static}' in s:
                c.line(x+5,yy-5,x+5+pdfmetrics.stringWidth(s,'Courier',size),yy-5)
            yy-=line_h
    c.setStrokeColor(HexColor('#17212E')); c.setLineWidth(1.9); c.setLineJoin(0)
    for ai,bi,t in edges:
        a,b=pick_anchors(ai,bi,t)
        if t in ('gen','real'):
            points=inheritance_path(a,b,ai,bi)
        else:
            points=route(a,b,ai,bi,t)
        if t in ('gen','real') and not is_orthogonal(points):
            points=join_orthogonal(a,[],b)
        if t in ('gen','real'):
            assert is_orthogonal(points), (a,b,points)
        # Decorations follow the routed path (route may move aggregate anchors).
        a,b=points[0],points[-1]
        dx=b[0]-points[-2][0]; dy=b[1]-points[-2][1]
        length=math.hypot(dx,dy) or 1; ux,uy=dx/length,dy/length; vx,vy=-uy,ux
        c.setDash(6,3) if t in ('dep','real') else c.setDash()
        draw_pts=list(points)
        if t in ('gen','real') and len(draw_pts)>=2:
            tip_back=(b[0]-12*ux,b[1]-12*uy)
            draw_pts=draw_pts[:-1]+[tip_back]
        elif t in ('dep','assoc') and len(draw_pts)>=2:
            tip_back=(b[0]-10*ux,b[1]-10*uy)
            draw_pts=draw_pts[:-1]+[tip_back]
        if t in ('aggregate','compose') and len(draw_pts)>=2:
            dx0=draw_pts[1][0]-a[0]; dy0=draw_pts[1][1]-a[1]
            len0=math.hypot(dx0,dy0) or 1
            ux0,uy0=dx0/len0,dy0/len0
            tip_back=(b[0]-10*ux,b[1]-10*uy)
            draw_pts=[(a[0]+16*ux0,a[1]+16*uy0)]+draw_pts[1:-1]+[tip_back]
        for pa,pb in zip(draw_pts,draw_pts[1:]): c.line(*pa,*pb)
        c.setDash()
        if t in ('gen','real'):
            tip=b
            p=c.beginPath(); p.moveTo(*tip)
            p.lineTo(tip[0]-12*ux+5.5*vx,tip[1]-12*uy+5.5*vy)
            p.lineTo(tip[0]-12*ux-5.5*vx,tip[1]-12*uy-5.5*vy); p.close()
            c.setFillColor(white); c.drawPath(p,fill=1,stroke=1)
        elif t in ('aggregate','compose'):
            dx0=points[1][0]-a[0]; dy0=points[1][1]-a[1]; length=math.hypot(dx0,dy0) or 1
            ux0,uy0=dx0/length,dy0/length; vx0,vy0=-uy0,ux0
            p=c.beginPath(); p.moveTo(*a)
            p.lineTo(a[0]+8*ux0+5*vx0,a[1]+8*uy0+5*vy0)
            p.lineTo(a[0]+16*ux0,a[1]+16*uy0)
            p.lineTo(a[0]+8*ux0-5*vx0,a[1]+8*uy0-5*vy0); p.close()
            c.setFillColor(HexColor('#17212E') if t=='compose' else white)
            c.drawPath(p,fill=1,stroke=1)
            c.setStrokeColor(HexColor('#17212E'))
            c.line(*b,b[0]-11*ux+4.5*vx,b[1]-11*uy+4.5*vy)
            c.line(*b,b[0]-11*ux-4.5*vx,b[1]-11*uy-4.5*vy)
            if t=='aggregate':
                c.setFont('Helvetica',8); c.drawString(b[0]+5,b[1]-12,'0..*')
        else:
            c.line(*b,b[0]-11*ux+4.5*vx,b[1]-11*uy+4.5*vy)
            c.line(*b,b[0]-11*ux-4.5*vx,b[1]-11*uy-4.5*vy)
    c.save()
    doc=pymupdf.open(stream=buf.getvalue(),filetype='pdf')
    doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(path)

# Sample-style layouts: siblings share a row under their parent.
# Every before/after diagram keeps an explicit Client showing what caller code depends on.
# Factory — Client + TransportFactory (local Factory Pattern Infographic).
d=DATA[1]
d['pnodes']=[n('Client','+ run()',1,0),n('Plane','+ fly()',0,1),n('Truck','+ drive()',1,1),n('Ship','+ sail()',2,1)]
d['pedges']=[(0,1,'dep'),(0,2,'dep'),(0,3,'dep')]
d['snodes']=[
    n('Client','+ run()',0,0),
    n('TransportFactory','+ create(type: String): Transport',1,0),
    n('Transport','+ transport()',2.5,0,'interface'),
    n('Plane','+ transport()',1,1),
    n('Truck','+ transport()',2,1),
    n('Ship','+ transport()',3,1)]
d['sedges']=[(0,1,'dep'),(1,2,'dep'),(3,2,'real'),(4,2,'real'),(5,2,'real')]
# Abstract Factory — each product its own box; methods only on interfaces.
d=DATA[2]
d['pnodes']=[
    n('Client','',1.5,1),
    n('UPSPlane','',0,0),n('UPSTruck','',1.5,0),n('UPSShip','',3,0),
    n('DHLPlane','',0,2),n('DHLTruck','',1.5,2),n('DHLShip','',3,2)]
d['pedges']=[(0,1,'dep'),(0,2,'dep'),(0,3,'dep'),(0,4,'dep'),(0,5,'dep'),(0,6,'dep')]
d['snodes']=[
    n('Client','',0,1),
    n('UPSFactory','',1,0),
    n('TransportFactory','+ createPlane()\n+ createShip()\n+ createTruck()',1,1,'interface'),
    n('DHLFactory','',1,2),
    n('UPSPlane','',2.2,0),n('UPSTruck','',2.9,0),n('UPSShip','',3.6,0),
    n('Transport','+ transport()',2.9,1,'interface'),
    n('DHLPlane','',2.2,2),n('DHLTruck','',2.9,2),n('DHLShip','',3.6,2)]
d['sedges']=[(0,1,'dep'),(0,3,'dep'),
             (1,2,'real'),(3,2,'real'),
             (4,7,'real'),(5,7,'real'),(6,7,'real'),(8,7,'real'),(9,7,'real'),(10,7,'real'),
             (1,4,'assoc'),(1,5,'assoc'),(1,6,'assoc'),
             (3,8,'assoc'),(3,9,'assoc'),(3,10,'assoc')]
# Adapter — inherits AnalyticsService; composes JsonAnalyticsLibrary.
d=DATA[4]
d['snodes']=[
    n('Client','- analytics: AnalyticsService\n+ analyzeStocks()',0,0),
    n('AnalyticsService','+ analyze(xml): Report {abstract}',1.5,0,'abstract'),
    n('XmlAnalyticsAdapter','- library: JsonAnalyticsLibrary\n+ analyze(xml): Report\n- convert(xml): JSON',1.5,1),
    n('JsonAnalyticsLibrary','+ analyze(json): Report',3.2,1)]
d['sedges']=[(0,1,'assoc'),(2,1,'gen'),(2,3,'compose')]
# Bridge — Client under combo classes in problem; Shape composes Color in solution.
d=DATA[5]
d['pnodes']=[
    n('RedCircle','+ draw()',0,0),n('BlueCircle','+ draw()',1.2,0),n('RedSquare','+ draw()',2.4,0),
    n('Client','+ render()',1.2,1)]
d['pedges']=[(3,0,'dep'),(3,1,'dep'),(3,2,'dep')]
d['snodes']=[
    n('Client','+ render()',0,0),
    n('Shape','- color: Color\n+ draw() {abstract}',1.2,0,'abstract'),
    n('Color','+ apply()',3.2,0,'interface'),
    n('Circle','+ draw()',0.7,1),
    n('Square','+ draw()',1.7,1),
    n('Red','+ apply()',2.7,1),
    n('Blue','+ apply()',3.7,1)]
d['sedges']=[(0,1,'dep'),(1,2,'compose'),(3,1,'gen'),(4,1,'gen'),(5,2,'real'),(6,2,'real')]
# Proxy — local Access Control Infographic: Client → DatabaseProxy; shared DatabaseService.
d=DATA[7]
d['pnodes']=[n('Client','+ run()',0,0),n('ExpensiveDatabaseService','+ ExpensiveDatabaseService()\n+ query(key): Result',2,1)]
d['pedges']=[(0,1,'dep')]
d['snodes']=[
    n('Client','+ run()',0,0),
    n('DatabaseService','+ query(key: String): Result',1.5,0,'interface'),
    n('DatabaseProxy','- realService: DatabaseService\n- cache: Map\n+ query(key): Result\n- getRealService()',0.5,1),
    n('RealDatabaseService','+ query(key): Result',2.5,1)]
d['sedges']=[(0,2,'dep'),(2,1,'real'),(3,1,'real'),(2,3,'assoc')]
# Composite — Client|OrderItem on top (wide gap); children only under OrderItem.
d=DATA[8]
d['pnodes']=[
    n('Client','+ total(box)',1,0),
    n('Product','+ price: Money',0.5,1),n('Box','+ contents: List',1.5,1)]
d['pedges']=[(0,1,'dep'),(0,2,'dep')]
d['snodes']=[
    n('Client','+ total(item)',0,0),
    n('OrderItem','+ getPrice(): Money',2.2,0,'interface'),
    n('Product','- price: Money\n+ getPrice(): Money',1.6,1.25),
    n('Box','- children: OrderItem[0..*]\n+ getPrice(): Money\n+ add(item)',2.8,1.25)]
d['sedges']=[(0,1,'dep'),(2,1,'real'),(3,1,'real'),(3,1,'aggregate')]
# Template Method — Client uses DataMiner; subclasses side-by-side.
d=DATA[9]
d['snodes']=[
    n('Client','+ run()',0,0),
    n('DataMiner','+ mine(path): Report\n# extract(path): Data {abstract}\n# analyze(data): Report',1.5,0,'abstract'),
    n('PdfMiner','# extract(path): Data',1,1),
    n('CsvMiner','# extract(path): Data',2.5,1)]
d['sedges']=[(0,1,'dep'),(2,1,'gen'),(3,1,'gen')]
# Strategy / State — Client uses the context; concretes share one row under the interface.
d=DATA[10]
d['snodes']=[
    n('Client','+ navigate()',0,0),
    n('Navigator','- strategy: RouteStrategy\n+ setStrategy(s)\n+ buildRoute(a, b): Route',1,0),
    n('RouteStrategy','+ buildRoute(a, b): Route',2.5,0,'interface'),
    n('RoadRoute','+ buildRoute(a, b): Route',1.5,1),
    n('WalkingRoute','+ buildRoute(a, b): Route',2.5,1),
    n('TransitRoute','+ buildRoute(a, b): Route',3.5,1)]
d['sedges']=[(0,1,'dep'),(1,2,'assoc'),(3,2,'real'),(4,2,'real'),(5,2,'real')]
d=DATA[11]
d['snodes']=[
    n('Client','+ publishDoc()',0,0),
    n('Document','- state: PublicationState\n+ publish(user)\n+ changeState(s)',1,0),
    n('PublicationState','+ publish(doc, user)',2.5,0,'interface'),
    n('Draft','+ publish(doc, user)',1.5,1),
    n('Moderation','+ publish(doc, user)',2.5,1),
    n('Published','+ publish(doc, user)',3.5,1)]
d['sedges']=[(0,1,'dep'),(1,2,'assoc'),(3,2,'real'),(4,2,'real'),(5,2,'real')]

def wrap(text,font,size,width):
    result=[]
    for paragraph in text.split('\n'):
        if not paragraph:result.append('');continue
        line=''
        for word in paragraph.split(' '):
            attempt=(line+' '+word).lstrip()
            if line and pdfmetrics.stringWidth(attempt,font,size)>width:result.append(line);line=word
            else:line=attempt
        result.append(line)
    return result

KW_PSEUDO={'new','if','else','elif','for','in','return','assert','not','and','or','true','false','null','None','static','synchronized','while','class','def','function','var','let','const','this'}
CODE_COLORS={'kw':'#0B57D0','id':'#18356F','type':'#0F766E','str':'#B14747','cmt':'#64748B','num':'#9A3412','op':'#4B5563'}
def tokenize_pseudo(line):
    if '//' in line:
        code,_,cmt=line.partition('//')
        runs=tokenize_pseudo(code) if code else []
        runs.append(('//'+cmt, CODE_COLORS['cmt']))
        return runs
    runs=[]; i=0
    while i<len(line):
        ch=line[i]
        if ch in ' \t':
            j=i
            while j<len(line) and line[j] in ' \t': j+=1
            runs.append((line[i:j], CODE_COLORS['id'])); i=j; continue
        if ch in '"\'':
            q=ch; j=i+1
            while j<len(line) and line[j]!=q: j+=1
            j=min(j+1,len(line)); runs.append((line[i:j], CODE_COLORS['str'])); i=j; continue
        if ch.isdigit():
            j=i
            while j<len(line) and (line[j].isalnum() or line[j]=='.'): j+=1
            runs.append((line[i:j], CODE_COLORS['num'])); i=j; continue
        if ch.isalpha() or ch=='_':
            j=i
            while j<len(line) and (line[j].isalnum() or line[j]=='_'): j+=1
            tok=line[i:j]
            if tok in KW_PSEUDO: col=CODE_COLORS['kw']
            elif tok[0].isupper(): col=CODE_COLORS['type']
            else: col=CODE_COLORS['id']
            runs.append((tok, col)); i=j; continue
        runs.append((ch, CODE_COLORS['op'])); i+=1
    return runs or [('', CODE_COLORS['id'])]

W,H=1440,810
PDF=canvas.Canvas(str(OUT/'Design Patterns.pdf'),pagesize=(W,H))
PDF.setTitle('Design Patterns')
PDF.setSubject('Cover plus 14 creational, structural, and behavioral design pattern slides')
SLIDES=[]
PAGE_META=[]  # (kind, title, category?) for bookmarks / HTML

def begin_page():
    elements=[]
    def rect(x,y,w,h,fill):
        PDF.setFillColor(HexColor(fill));PDF.rect(x,H-y-h,w,h,fill=1,stroke=0);elements.append(('rect',x,y,w,h,fill))
    def text(s,x,y,w,size=18,color=INK,font='Helvetica',leading=None):
        lines=wrap(s,font,size,w);leading=leading or size*1.2
        PDF.setFillColor(HexColor(color));PDF.setFont(font,size)
        for j,line in enumerate(lines):PDF.drawString(x,H-y-size-j*leading,line)
        elements.append(('text',x,y,w,len(lines)*leading,s,size,color,font,leading))
        return y+len(lines)*leading
    def code(s,x,y,w,size=16,leading=21):
        lines=s.split('\n'); PDF.setFont('Courier',size)
        for j,line in enumerate(lines):
            cx=x; yy=H-y-size-j*leading
            for tok,col in tokenize_pseudo(line):
                PDF.setFillColor(HexColor(col)); PDF.drawString(cx,yy,tok)
                cx+=pdfmetrics.stringWidth(tok,'Courier',size)
        elements.append(('code',x,y,w,len(lines)*leading,s,size,'Courier',leading))
        return y+len(lines)*leading
    return elements,rect,text,code

# Cover: how to read the deck and why patterns exist (client / module DX).
elements,rect,text,code=begin_page()
rect(0,0,W,H,'#FFFFFF')
rect(0,0,W,8,'#0F766E')
text('Design Patterns',48,36,900,48,'#101319',font='Helvetica-Bold')
text('Creational · Structural · Behavioral',48,96,900,18,'#596273')
text('Modules built for another developer’s client code',48,124,1100,22,'#182230')
rect(48,168,1344,2,'#D0D7E2')
y=188
y=text('Purpose',48,y,600,22,'#0F766E',font='Helvetica-Bold')+8
y=text('Patterns are shared answers to recurring design pressures. They help you shape module boundaries so callers get a calm, intention-revealing API while the module stays free to grow, swap internals, or add variants without rewriting every consumer.',48,y,1344,16,'#192331',leading=22)+14
y=text('Developer experience goal',48,y,600,22,'#0F766E',font='Helvetica-Bold')+8
y=text('Treat each slide as a handover story: you own the module; another developer owns the client. Good patterns make that handover kind—small surface area, clear abstractions, and room to extend the module graciously so clients keep writing the same simple calls.',48,y,1344,16,'#192331',leading=22)+14
y=text('How to read each pattern slide',48,y,600,22,'#0F766E',font='Helvetica-Bold')+10
for label,body in [
    ('Problem / Solution','Why the current shape hurts, and what the pattern changes about dependencies and responsibilities.'),
    ('Before / After UML','Always includes a Client box. Follow dashed arrows from Client to see what caller code must know. After should depend on a narrow API, not a pile of concretes.'),
    ('Client Code','How the other developer uses (or is forced to misuse) your module.'),
    ('Module Code','The API boundary you hand over—the implementation clients should not need to reopen when requirements grow.'),
]:
    text(label,48,y,220,15,'#151B27',font='Helvetica-Bold')
    y=text(body,280,y,1112,15,'#192331',leading=20)+8
rect(48,H-88,1344,48,'#EDF0F6')
text('Look for fewer Client dependencies after the pattern, and for module code that stays easy to use while remaining easy to extend.',64,H-74,1312,15,'#374151')
PDF.bookmarkPage('cover')
PDF.addOutlineEntry('Cover — How to read', 'cover', 0, closed=0)
PDF.showPage(); SLIDES.append(elements); PAGE_META.append(('cover','Cover — How to read',None))

last_category=None
for idx,d in enumerate(DATA):
    elements,rect,text,code=begin_page()
    rect(0,0,W,H,'#FFFFFF')
    title_size=44 if len(d['title'])<15 else 39
    text(d['title'],24,9,460,title_size,'#101319',font='Helvetica-Bold')
    divider=24+pdfmetrics.stringWidth(d['title'],'Helvetica-Bold',title_size)+24
    rect(divider,14,2,52,'#858E9E')
    text(d['category']+' Design Pattern',divider+18,13,1385-divider,17,'#596273')
    text(d['desc'],divider+18,37,1385-divider,18,'#182230')
    rect(24,76,1392,24,'#EDF0F6')
    text('CASE STUDY: '+d['case'],34,79,1250,13,'#374151',font='Helvetica-Bold')
    text(f'{idx+1:02d} / 14',1340,79,75,13,'#374151',font='Helvetica-Bold')
    no_module=d['title'] in ('Abstract Factory','Builder')
    bullet_ps='\n' in d['problem'] or '\n' in d['solution']
    # Compact problem/solution + UML on every slide so code panels get the height.
    if bullet_ps:
        panel_h,body_size,body_lead,body_y=82,10,12,130
    else:
        panel_h,body_size,body_lead,body_y=52,12,14,126
    code_bottom=H-26
    code_top=428
    uml_top=109+panel_h+6
    uml_h=code_top-uml_top-8
    uml_img_y=uml_top+28
    uml_img_h=uml_h-32
    for side,x,col,key in [('Problem',24,'#C5222B','problem'),('Solution',732,'#007E78','solution')]:
        rect(x,109,684,panel_h,'#EFA5AA' if key=='problem' else '#94D9D1')
        rect(x+2,111,680,panel_h-4,'#FFE2E3' if key=='problem' else '#D9F5F0')
        rect(x+10,116,5,18,col)
        text(side,x+23,112,642,16,col,font='Helvetica-Bold')
        text(d[key],x+17,body_y,650,body_size,'#192331',leading=body_lead)
        rect(x,uml_top,684,uml_h,'#DFE3EC')
        rect(x+2,uml_top+2,680,uml_h-4,'#FFFFFF')
        rect(x+2,uml_top+2,680,24,'#E4E7F0')
        label='Before (direct coupling)' if key=='problem' else 'After (using '+d['title']+')'
        text(label,x+12,uml_top+3,660,13,'#151B27',font='Helvetica-Bold')
        imagepath=OUT/f'{idx+1:02d}-{key}.png'
        uml(d['pnodes' if key=='problem' else 'snodes'],d['pedges' if key=='problem' else 'sedges'],str(imagepath),compact=True)
        PDF.drawImage(str(imagepath),x+11,H-uml_img_y-uml_img_h,660,uml_img_h)
        elements.append(('image',x+11,uml_img_y,660,uml_img_h,str(imagepath)))
    module_in_solution=d['title'] in ('Factory Method','Proxy')
    code_area=code_bottom-code_top
    if no_module:
        # Client before/after only — full-height panels (Builder / Abstract Factory).
        csize,clead=(13,16) if d['title']=='Builder' else (13,16)
        for x,label,src in [(24,'Client Code (Before)',d['before']),(732,'Client Code (After)',d['after'])]:
            rect(x,code_top,684,code_area,'#DFE3EC')
            rect(x+2,code_top+2,680,code_area-4,'#F8F9FC')
            rect(x+2,code_top+2,680,24,'#E4E7F0')
            text(label,x+12,code_top+3,550,14,'#161D2B',font='Helvetica-Bold')
            text('Pseudocode',x+574,code_top+6,100,10,'#667085')
            code(src,x+14,code_top+30,650,csize,clead)
    elif d['title']=='Singleton':
        # Service before/after side-by-side; taller full-width module (Config API).
        svc_h=112
        mod_y=code_top+svc_h+6
        mod_h=code_bottom-mod_y
        for x,label,src in [(24,'Service Code (Before)',d['before']),(732,'Service Code (After)',d['after'])]:
            rect(x,code_top,684,svc_h,'#DFE3EC')
            rect(x+2,code_top+2,680,svc_h-4,'#F8F9FC')
            rect(x+2,code_top+2,680,24,'#E4E7F0')
            text(label,x+12,code_top+3,550,14,'#161D2B',font='Helvetica-Bold')
            text('Pseudocode',x+574,code_top+6,100,10,'#667085')
            code(src,x+14,code_top+28,650,13,16)
        rect(24,mod_y,1392,mod_h,'#DFE3EC')
        rect(26,mod_y+2,1388,mod_h-4,'#F8F9FC')
        rect(26,mod_y+2,1388,24,'#E4E7F0')
        text('Module Code (API boundary)',36,mod_y+4,1200,15,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',1296,mod_y+7,105,10,'#667085')
        code(d['module'],38,mod_y+30,1364,14,17)
    elif module_in_solution:
        # Before fills the left; after + module stack on the solution half.
        before_h=code_area
        after_h=int(code_area*0.52) if d['title']=='Builder' else int(code_area*0.40)
        mod_y=code_top+after_h+6
        mod_h=code_bottom-mod_y
        rect(24,code_top,684,before_h,'#DFE3EC')
        rect(26,code_top+2,680,before_h-4,'#F8F9FC')
        rect(26,code_top+2,680,24,'#E4E7F0')
        text('Client Code (Before)',36,code_top+3,550,14,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',598,code_top+6,100,10,'#667085')
        code(d['before'],38,code_top+28,650,13 if d['title']=='Builder' else 14,16 if d['title']=='Builder' else 17)
        rect(732,code_top,684,after_h,'#DFE3EC')
        rect(734,code_top+2,680,after_h-4,'#F8F9FC')
        rect(734,code_top+2,680,24,'#E4E7F0')
        text('Client Code (After)',744,code_top+3,550,14,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',1306,code_top+6,100,10,'#667085')
        code(d['after'],746,code_top+28,650,12 if d['title']=='Builder' else 13,15 if d['title']=='Builder' else 16)
        rect(732,mod_y,684,mod_h,'#DFE3EC')
        rect(734,mod_y+2,680,mod_h-4,'#F8F9FC')
        rect(734,mod_y+2,680,24,'#E4E7F0')
        text('Module Code (API boundary)',744,mod_y+4,520,14,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',1306,mod_y+7,100,10,'#667085')
        code(d['module'],746,mod_y+28,650,12,15)
    else:
        svc_h=int(code_area*0.42)
        mod_y=code_top+svc_h+6
        mod_h=code_bottom-mod_y
        for x,label,src in [(24,'Client Code (Before)',d['before']),(732,'Client Code (After)',d['after'])]:
            rect(x,code_top,684,svc_h,'#DFE3EC')
            rect(x+2,code_top+2,680,svc_h-4,'#F8F9FC')
            rect(x+2,code_top+2,680,24,'#E4E7F0')
            text(label,x+12,code_top+3,550,14,'#161D2B',font='Helvetica-Bold')
            text('Pseudocode',x+574,code_top+6,100,10,'#667085')
            code(src,x+14,code_top+28,650,13,16)
        rect(24,mod_y,1392,mod_h,'#DFE3EC')
        rect(26,mod_y+2,1388,mod_h-4,'#F8F9FC')
        rect(26,mod_y+2,1388,24,'#E4E7F0')
        text('Module Code (API boundary)',36,mod_y+4,1200,15,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',1296,mod_y+7,105,10,'#667085')
        code(d['module'],38,mod_y+30,1364,13,16)
    slug=d['title'].lower().replace(' ','-');url='https://refactoring.guru/design-patterns/'+slug;d['url']=url
    text('Source: '+url,24,788,800,10,'#566174')
    text('UML: Client box = caller code; hollow triangle = inheritance / realization; dashed open arrow = dependency',720,788,700,10,'#566174')
    # PDF outline / bookmarks (sidebar TOC in readers). HTML print-to-PDF cannot do this reliably.
    bookmark=f'p{idx}'
    PDF.bookmarkPage(bookmark)
    if d['category']!=last_category:
        PDF.addOutlineEntry(d['category'],bookmark,0,closed=0)
        last_category=d['category']
    PDF.addOutlineEntry(f'{idx+1:02d}. {d["title"]}',bookmark,1,closed=0)
    PDF.showPage();SLIDES.append(elements); PAGE_META.append(('pattern',d['title'],d['category']))
PDF.save()
# Ensure outline is present even if a reader prefers the PyMuPDF TOC form.
pdf_path=OUT/'Design Patterns.pdf'
doc=pymupdf.open(pdf_path)
toc=[[1,'Cover — How to read',1]]; prev=None
for i,d in enumerate(DATA):
    page=i+2  # cover is page 1
    if d['category']!=prev:
        toc.append([1,d['category'],page]); prev=d['category']
    toc.append([2,f'{i+1:02d}. {d["title"]}',page])
doc.set_toc(toc)
doc.set_metadata({'title':'Design Patterns','subject':'Design pattern slides'})
doc.saveIncr(); doc.close()

# Minimal standards-based OOXML. Every title, description, code line and
# caption is a native PowerPoint text run. Only UML is embedded raster media.
NS='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
def emu(v):return str(round(v*12700))
def xfrm(x,y,w,h):return f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
def run_xml(text,size,color,face,bold=''):
    return f'<a:r><a:rPr lang="en-US" sz="{round(size*100)}"{bold}><a:solidFill><a:srgbClr val="{color[1:]}"/></a:solidFill><a:latin typeface="{face}"/></a:rPr><a:t xml:space="preserve">{escape(text)}</a:t></a:r>'
def xmltext(e,i):
    _,x,y,w,h,s,size,color,font,leading=e
    face='Courier New' if font=='Courier' else 'Arial'
    bold=' b="1"' if font.endswith('Bold') else ''
    paragraphs=''.join(f'<a:p><a:pPr><a:lnSpc><a:spcPts val="{round(leading*100)}"/></a:lnSpc></a:pPr>{run_xml(line,size,color,face,bold)}<a:endParaRPr sz="{round(size*100)}"/></a:p>' for line in wrap(s,font,size,w))
    return f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h+5)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"/><a:lstStyle/>{paragraphs}</p:txBody></p:sp>'
def xmlcode(e,i):
    _,x,y,w,h,s,size,font,leading=e
    paragraphs=[]
    for line in s.split('\n'):
        runs=''.join(run_xml(tok,size,col,'Courier New') for tok,col in tokenize_pseudo(line)) or run_xml(' ',size,CODE_COLORS['id'],'Courier New')
        paragraphs.append(f'<a:p><a:pPr><a:lnSpc><a:spcPts val="{round(leading*100)}"/></a:lnSpc></a:pPr>{runs}<a:endParaRPr sz="{round(size*100)}"/></a:p>')
    return f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Code {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h+5)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"/><a:lstStyle/>{"".join(paragraphs)}</p:txBody></p:sp>'
def rels(items):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{i}" Type="{R}/{typ}" Target="{target}"/>' for i,typ,target in items)+'</Relationships>'
group='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
N_SLIDES=len(SLIDES); MASTER_RID=f'rId{N_SLIDES+1}'
with zipfile.ZipFile(OUT/'Design Patterns.pptx','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('_rels/.rels',rels([('rId1','officeDocument','ppt/presentation.xml')]))
    slideids=''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,N_SLIDES+1))
    z.writestr('ppt/presentation.xml',f'<p:presentation xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="{MASTER_RID}"/></p:sldMasterIdLst><p:sldIdLst>{slideids}</p:sldIdLst><p:sldSz cx="{emu(W)}" cy="{emu(H)}"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
    z.writestr('ppt/_rels/presentation.xml.rels',rels([(f'rId{i}','slide',f'slides/slide{i}.xml') for i in range(1,N_SLIDES+1)]+[(MASTER_RID,'slideMaster','slideMasters/slideMaster1.xml')]))
    z.writestr('ppt/slideMasters/slideMaster1.xml',f'<p:sldMaster xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>{group}</p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles/></p:sldMaster>')
    z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels',rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml')]))
    z.writestr('ppt/slideLayouts/slideLayout1.xml',f'<p:sldLayout xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}" type="blank"><p:cSld name="Blank"><p:spTree>{group}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
    z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels',rels([('rId1','slideMaster','../slideMasters/slideMaster1.xml')]))
    overrides=[('/ppt/presentation.xml','application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'),('/ppt/slideMasters/slideMaster1.xml','application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml'),('/ppt/slideLayouts/slideLayout1.xml','application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml')]
    for si,elements in enumerate(SLIDES,1):
        shapes=[]; relationships=[('rId1','slideLayout','../slideLayouts/slideLayout1.xml')];imageidx=0
        for i,e in enumerate(elements,2):
            typ,x,y,w,h,*rest=e
            if typ=='text':shapes.append(xmltext(e,i))
            elif typ=='code':shapes.append(xmlcode(e,i))
            elif typ=='rect':
                fill=rest[0][1:];shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Panel {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')
            else:
                imageidx+=1;rid=f'rId{imageidx+1}';name=f's{si}_{imageidx}.png';z.write(rest[0],'ppt/media/'+name);relationships.append((rid,'image','../media/'+name))
                shapes.append(f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="UML class diagram"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
        z.writestr(f'ppt/slides/slide{si}.xml',f'<p:sld xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>{group}{"".join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
        z.writestr(f'ppt/slides/_rels/slide{si}.xml.rels',rels(relationships));overrides.append((f'/ppt/slides/slide{si}.xml','application/vnd.openxmlformats-officedocument.presentationml.slide+xml'))
    z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'+''.join(f'<Override PartName="{part}" ContentType="{ct}"/>' for part,ct in overrides)+'</Types>')

# Self-contained printable HTML, with selectable text and embedded UML only.
# Bookmarks: browser Print→PDF does not reliably create a PDF outline. Use Download PDF.
import base64
pages=[]
for elements,meta in zip(SLIDES,PAGE_META):
    parts=[]
    for e in elements:
        typ,x,y,w,h,*r=e;style=f'position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
        if typ=='rect':parts.append(f'<div style="{style}background:{r[0]}"></div>')
        elif typ=='image':parts.append(f'<img alt="UML class diagram" style="{style}" src="data:image/png;base64,{base64.b64encode(Path(r[0]).read_bytes()).decode()}">')
        elif typ=='code':
            s,size,font,leading=r
            rows=[]
            for line in s.split('\n'):
                spans=''.join(f'<span style="color:{col}">{html.escape(tok)}</span>' for tok,col in tokenize_pseudo(line)) or '&nbsp;'
                rows.append(spans)
            parts.append(f'<div style="{style}font-family:Courier New,monospace;font-size:{size}px;line-height:{leading}px;white-space:pre;">{("<br>".join(rows))}</div>')
        else:
            s,size,color,font,leading=r;family='Courier New' if font=='Courier' else 'Arial';weight='bold' if font.endswith('Bold') else 'normal'
            lines=wrap(s,font,size,w);parts.append(f'<div style="{style}font-family:{family};font-size:{size}px;line-height:{leading}px;color:{color};font-weight:{weight};white-space:pre;">{html.escape(chr(10).join(lines))}</div>')
    title=meta[1]; slug=title.lower().replace(' ','-').replace('—','-').replace(',','')
    pages.append(f'<section id="{html.escape(slug)}" aria-label="{html.escape(title)}"><h1 class="slide-title">{html.escape(title)}</h1>'+''.join(parts)+'</section>')
toolbar=(''
    '<header class="toolbar" role="banner">'
    '<strong>Design Patterns</strong>'
    '<span class="hint">Bookmarks ship in the PDF download — browser Print→PDF usually omits them.</span>'
    '<a class="btn" href="Design%20Patterns.pdf" download="Design Patterns.pdf">Download PDF</a>'
    '<button class="btn secondary" type="button" onclick="window.print()">Print</button>'
    '</header>')
css=(''
    '@page{size:15in 8.4375in;margin:0}'
    '*{box-sizing:border-box}'
    'body{margin:0;background:#cbd5e1;font-family:Arial,sans-serif}'
    '.toolbar{position:sticky;top:0;z-index:20;display:flex;gap:12px;align-items:center;flex-wrap:wrap;'
    'padding:10px 18px;background:#182230;color:#F8FAFC;box-shadow:0 1px 0 rgba(0,0,0,.2)}'
    '.toolbar .hint{flex:1;min-width:200px;font-size:13px;color:#CBD5E1}'
    '.toolbar .btn{appearance:none;border:0;border-radius:6px;padding:8px 14px;background:#0F766E;color:white;'
    'font:600 14px Arial,sans-serif;text-decoration:none;cursor:pointer}'
    '.toolbar .btn.secondary{background:#334155}'
    '.toolbar .btn:hover{filter:brightness(1.08)}'
    'section{position:relative;width:1440px;height:810px;background:white;break-after:page;margin:20px auto;'
    'overflow:hidden}'
    'h1.slide-title{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
    'clip:rect(0,0,0,0);white-space:nowrap;border:0}'
    '@media print{body{background:white}.toolbar{display:none}section{margin:0}}')
(OUT/'Design Patterns.html').write_text(
    '<!doctype html><html><head><meta charset="utf-8"><title>Design Patterns</title>'
    f'<style>{css}</style></head><body>{toolbar}{"".join(pages)}</body></html>',
    encoding='utf-8')
(OUT/'content.json').write_text(json.dumps(DATA,indent=2),encoding='utf-8')
print(f'Created {N_SLIDES}-slide PPTX, PDF (with bookmarks), and HTML in',OUT)
