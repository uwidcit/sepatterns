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

add('Singleton','Creational','Shared database connection',
'Provide one shared instance through a controlled access point.',
'Independent callers create separate database connections.', 'Hide construction; return the same instance to every caller.',
'a = new Database()\nb = new Database()\na.query(sql)\n// a and b are different objects',
'a = Database.getInstance()\nb = Database.getInstance()\na.query(sql)\nassert a is b',
'// Database: lazy, thread-safe accessor\nstatic synchronized getInstance():\n    if instance == null: instance = new Database()\n    return instance',
[n('Application','+ run()',0,0),n('Database','+ Database()\n+ query(sql)',2,1)],[(0,1,'dep')],
[n('Application','+ run()',0,0),n('Database','- instance: Database {static}\n- Database()\n+ getInstance(): Database {static}\n+ query(sql)',2,1)],[(0,1,'dep')], 'Singleton Pattern_ Thread-Safe Instance Sharing.png')

add('Factory Method','Creational','Road and sea logistics',
'Let creator subclasses choose the product used by shared business logic.',
'Logistics directly constructs trucks; sea delivery forces edits.', 'Override a creation method while preserving delivery planning.',
'truck = new Truck()\ntruck.deliver()\n// sea support needs another branch',
'logistics = new SeaLogistics()\nlogistics.planDelivery()\n// planning uses Transport',
'// Logistics.planDelivery()\nvehicle = createTransport()\nvehicle.deliver()\n// SeaLogistics.createTransport(): return new Ship()',
[n('Logistics','+ planDelivery()',0,0),n('Truck','+ deliver()',2,1)],[(0,1,'dep')],
[n('Logistics','+ planDelivery()\n+ createTransport(): Transport {abstract}',0,0,'abstract'),n('Transport','+ deliver()',2,0,'interface'),n('RoadLogistics','+ createTransport(): Transport',0,2),n('SeaLogistics','+ createTransport(): Transport',1,2),n('Truck / Ship','+ deliver()',2,2)],[(2,0,'gen'),(3,0,'gen'),(0,1,'dep'),(4,1,'real')], 'Factory Pattern Infographic_ Before and After (1).png')

add('Abstract Factory','Creational','Matching furniture families',
'Create related products through a family-specific factory.',
'Direct construction can mix modern chairs with Victorian sofas.', 'Select one family factory; request products through interfaces.',
'chair = new ModernChair()\nsofa = new VictorianSofa()\n// mismatched furniture family',
'factory = new ModernFactory()\nchair = factory.createChair()\nsofa = factory.createSofa()',
'// ModernFactory\ncreateChair(): return new ModernChair()\ncreateSofa():  return new ModernSofa()\n// VictorianFactory returns Victorian products',
[n('Shop','+ furnish()',1,0),n('ModernChair','+ sitOn()',0,2),n('VictorianSofa','+ lieOn()',2,2)],[(0,1,'dep'),(0,2,'dep')],
[n('FurnitureFactory','+ createChair(): Chair\n+ createSofa(): Sofa',1,0,'interface'),n('ModernFactory','+ createChair(): Chair\n+ createSofa(): Sofa',0,1),n('VictorianFactory','+ createChair(): Chair\n+ createSofa(): Sofa',2,1),n('Chair','+ sitOn()',0,2,'interface'),n('Sofa','+ lieOn()',2,2,'interface')],[(1,0,'real'),(2,0,'real'),(0,3,'dep'),(0,4,'dep')], 'abstractfactory.png')

add('Builder','Creational','Cars and their manuals',
'Separate construction steps from the representation being assembled.',
'Long car constructors and separate manual assembly duplicate choices.', 'A director runs the same recipe against different builders.',
'car = new Car(2, sportEngine, true)\nmanual = new Manual(2, "sport", "GPS")\n// maintain the same recipe twice',
'builder = new CarBuilder()\ndirector.sportsCar(builder)\ncar = builder.getResult()\n// use ManualBuilder for a matching manual',
'// Director.sportsCar(builder)\nbuilder.reset()\nbuilder.setSeats(2)\nbuilder.setEngine(sportEngine)\nbuilder.setGPS(true)',
[n('Client','+ assemble()',1,0),n('Car','+ Car(seats, engine, gps)',0,2),n('Manual','+ Manual(seats, engine, gps)',2,2)],[(0,1,'dep'),(0,2,'dep')],
[n('Director','+ sportsCar(b: Builder)',0,0),n('Builder','+ reset()\n+ setSeats(n)\n+ setEngine(e)\n+ setGPS(on)',2,0,'interface'),n('CarBuilder','+ getResult(): Car',1,2),n('ManualBuilder','+ getResult(): Manual',2,2)],[(0,1,'dep'),(2,1,'real'),(3,1,'real')])

add('Adapter','Structural','XML stock data and JSON analytics',
'Translate an existing interface into the interface a client expects.',
'The stock app supplies XML; the analytics library requires JSON.', 'An adapter accepts XML, converts it, then delegates analytics.',
'xml = provider.getStockData()\nlibrary = new JsonAnalyticsLibrary()\nreport = library.analyze(xml)\n// incompatible input format',
'service = new XmlAnalyticsAdapter(library)\nxml = provider.getStockData()\nreport = service.analyze(xml)',
'// XmlAnalyticsAdapter.analyze(xml)\njson = convertXmlToJson(xml)\nreturn library.analyze(json)',
[n('StockApplication','+ analyzeStocks()',0,0),n('StockDataProvider','+ getStockData(): XML',0,2),n('JsonAnalyticsLibrary','+ analyze(json): Report',2,1)],[(0,1,'dep'),(0,2,'dep')],
[n('StockApplication','- analytics: AnalyticsService',0,0),n('AnalyticsService','+ analyze(xml): Report',2,0,'interface'),n('XmlAnalyticsAdapter','- library: JsonAnalyticsLibrary\n+ analyze(xml): Report',2,1),n('JsonAnalyticsLibrary','+ analyze(json): Report',0,2)],[(0,1,'assoc'),(2,1,'real'),(2,3,'assoc')], 'adapter.png')

add('Bridge','Structural','Shapes and colors',
'Separate two independent dimensions so both can evolve independently.',
'Each shape/color combination requires another subclass.', 'Shapes hold a Color reference instead of encoding color in inheritance.',
'redCircle = new RedCircle()\nblueSquare = new BlueSquare()\nredCircle.draw()\n// more combinations, more classes',
'shape = new Circle(new Red())\nshape.draw()\nshape.color = new Blue()\nshape.draw()',
'// Circle.draw()\ncolor.apply()\nrenderCircleGeometry()\n// color and geometry vary independently',
[n('Shape','+ draw()',1,0,'abstract'),n('RedCircle','+ draw()',0,2),n('BlueCircle','+ draw()',1,2),n('RedSquare','+ draw()',2,2)],[(1,0,'gen'),(2,0,'gen'),(3,0,'gen')],
[n('Shape','- color: Color\n+ draw() {abstract}',0,0,'abstract'),n('Color','+ apply()',2,0,'interface'),n('Circle / Square','+ draw()',0,2),n('Red / Blue','+ apply()',2,2)],[(0,1,'assoc'),(2,0,'gen'),(3,1,'real')], 'bridge.png')

add('Facade','Structural','Video conversion subsystem',
'Expose a simple entry point to a complex subsystem.',
'Every client coordinates codecs, bitrate conversion, and audio repair.', 'A facade orchestrates the subsystem behind one conversion call.',
'codec = CodecFactory.extract(file)\nraw = BitrateReader.read(file, codec)\nvideo = BitrateReader.convert(raw, mp4)\nresult = AudioMixer.fix(video)',
'converter = new VideoConverter()\nresult = converter.convert(file, "mp4")',
'// VideoConverter.convert(file, format)\nsource = CodecFactory.extract(file)\nraw = BitrateReader.read(file, source)\nvideo = BitrateReader.convert(raw, codecFor(format))\nreturn AudioMixer.fix(video)',
[n('Client','+ export()',1,0),n('CodecFactory','+ extract(file)',0,2),n('BitrateReader','+ read()\n+ convert()',1,2),n('AudioMixer','+ fix(video)',2,2)],[(0,1,'dep'),(0,2,'dep'),(0,3,'dep')],
[n('Client','+ export()',0,0),n('VideoConverter','+ convert(file, format): File',2,0),n('CodecFactory','+ extract(file)',0,2),n('BitrateReader','+ read()\n+ convert()',1,2),n('AudioMixer','+ fix(video)',2,2)],[(0,1,'dep'),(1,2,'dep'),(1,3,'dep'),(1,4,'dep')], 'facade.png')

add('Proxy','Structural','Cached third-party video service',
'Control access to a service through the same interface.',
'Repeated video downloads invoke the remote service again.', 'A proxy caches results and delegates only on a cache miss.',
'service = new ThirdPartyVideoService()\na = service.downloadVideo(id)\nb = service.downloadVideo(id)\n// two remote requests',
'service = new CachedVideoProxy(realService)\na = service.downloadVideo(id)\nb = service.downloadVideo(id)\n// second request uses the cache',
'// CachedVideoProxy.downloadVideo(id)\nif not cache.contains(id):\n    cache[id] = real.downloadVideo(id)\nreturn cache[id]',
[n('VideoManager','+ play(id)',0,0),n('ThirdPartyVideoService','+ downloadVideo(id): Video',2,1)],[(0,1,'dep')],
[n('VideoManager','- service: VideoService',0,0),n('VideoService','+ downloadVideo(id): Video',2,0,'interface'),n('CachedVideoProxy','- real: VideoService\n- cache: Map\n+ downloadVideo(id): Video',1,2),n('ThirdPartyVideoService','+ downloadVideo(id): Video',2,2)],[(0,1,'assoc'),(2,1,'real'),(3,1,'real'),(2,3,'assoc')], 'Proxy Pattern_ Access Control Infographic.png')

add('Composite','Structural','Boxes containing products and boxes',
'Treat individual objects and recursive groups through one interface.',
'Pricing code distinguishes products from nested boxes repeatedly.', 'A box sums child prices; each child follows the same contract.',
'total = 0\nfor item in box.contents:\n    if item is Product: total += item.price\n    else: total += priceNestedBox(item)',
'order = new Box([product, innerBox])\ntotal = order.getPrice()\n// leaf and group are both OrderItem',
'// Box.getPrice()\ntotal = 0\nfor child in children:\n    total += child.getPrice()\nreturn total',
[n('PriceClient','+ total(box)',1,0),n('Product','+ price: Money',0,2),n('Box','+ contents: List',2,2)],[(0,1,'dep'),(0,2,'dep')],
[n('OrderItem','+ getPrice(): Money',1,0,'interface'),n('Product','- price: Money\n+ getPrice(): Money',0,2),n('Box','- children: OrderItem[0..*]\n+ getPrice(): Money\n+ add(item)',2,2)],[(1,0,'real'),(2,0,'real'),(2,0,'aggregate')])

add('Template Method','Behavioral','Mining PDF and CSV documents',
'Fix an algorithm’s order while subclasses implement selected steps.',
'Format-specific miners duplicate the processing and reporting pipeline.', 'Move the sequence into a base method; override extraction only.',
'if format == "pdf":\n    data = pdf.extract(path)\nelse: data = csv.extract(path)\nreport = analyze(data)',
'miner = new PdfMiner()\nreport = miner.mine(path)\n// CsvMiner uses the same pipeline',
'// DataMiner.mine(path): fixed sequence\ndata = extract(path)\nreturn analyze(data)\n// PdfMiner.extract(path): return parsePdf(path)',
[n('Client','+ run()',1,0),n('PdfMiner','+ extract(path)\n+ analyze(data)',0,2),n('CsvMiner','+ extract(path)\n+ analyze(data)',2,2)],[(0,1,'dep'),(0,2,'dep')],
[n('DataMiner','+ mine(path): Report\n# extract(path): Data {abstract}\n# analyze(data): Report',1,0,'abstract'),n('PdfMiner','# extract(path): Data',0,2),n('CsvMiner','# extract(path): Data',2,2)],[(1,0,'gen'),(2,0,'gen')])

add('Strategy','Behavioral','Navigation route algorithms',
'Make alternative algorithms interchangeable through a shared contract.',
'A navigator grows conditionals for road, walking, and transit routes.', 'Delegate routing to a strategy selected by the client.',
'if mode == "road": route = roadRoute(a, b)\nelif mode == "walk": route = walkRoute(a, b)\nelse: route = transitRoute(a, b)',
'navigator.setStrategy(new WalkingRoute())\nroute = navigator.buildRoute(a, b)\n// choose another strategy at runtime',
'// Navigator.buildRoute(a, b)\nreturn strategy.buildRoute(a, b)\n// WalkingRoute builds pedestrian paths',
[n('Navigator','- mode: String\n+ buildRoute(a, b): Route',1,1)],[],
[n('Navigator','- strategy: RouteStrategy\n+ setStrategy(s)\n+ buildRoute(a, b): Route',0,0),n('RouteStrategy','+ buildRoute(a, b): Route',2,0,'interface'),n('RoadRoute','+ buildRoute(a, b): Route',0,2),n('WalkingRoute','+ buildRoute(a, b): Route',1,2),n('TransitRoute','+ buildRoute(a, b): Route',2,2)],[(0,1,'assoc'),(2,1,'real'),(3,1,'real'),(4,1,'real')])

add('State','Behavioral','Document publication workflow',
'Delegate behavior to an object representing the current state.',
'Publication rules accumulate in a switch over document status.', 'Each state handles publish and can transition the document.',
'if doc.status == "draft":\n    doc.status = "moderation"\nelif doc.status == "moderation" and user.isAdmin:\n    doc.status = "published"',
'doc = new Document(new Draft())\ndoc.publish(user)  // enters moderation\ndoc.publish(admin) // becomes published',
'// Moderation.publish(doc, user)\nif user.isAdmin:\n    doc.changeState(new Published())\n// Published.publish(...) does nothing',
[n('Document','- status: String\n+ publish(user)',1,1)],[],
[n('Document','- state: PublicationState\n+ publish(user)\n+ changeState(s)',0,0),n('PublicationState','+ publish(doc, user)',2,0,'interface'),n('Draft','+ publish(doc, user)',0,2),n('Moderation','+ publish(doc, user)',1,2),n('Published','+ publish(doc, user)',2,2)],[(0,1,'assoc'),(2,1,'real'),(3,1,'real'),(4,1,'real')])

add('Observer','Behavioral','Editor events notify logging and email',
'Notify registered subscribers when a publisher emits an event.',
'Editor logic directly invokes concrete logging and email services.', 'Publish an event; subscribers handle their own reactions.',
'editor.saveFile()\nlogger.write(file.name)\nmailer.send(file.name)\n// client must wire every reaction',
'events.subscribe("save", new LogListener())\nevents.subscribe("save", new EmailListener())\neditor.saveFile() // emits save event',
'// EventManager.notify(type, data)\nfor listener in listeners[type]:\n    listener.update(data)\n// Editor.saveFile(): write(); events.notify("save", name)',
[n('Editor','+ saveFile()',1,0),n('Logger','+ write(name)',0,2),n('Mailer','+ send(name)',2,2)],[(0,1,'dep'),(0,2,'dep')],
[n('Editor','- events: EventManager\n+ saveFile()',0,0),n('EventManager','- listeners: EventListener[0..*]\n+ subscribe(type, listener)\n+ unsubscribe(type, listener)\n+ notify(type, data)',1,1),n('EventListener','+ update(data)',2,0,'interface'),n('LogListener','+ update(data)',0,2),n('EmailListener','+ update(data)',2,2)],[(0,1,'assoc'),(1,2,'assoc'),(3,2,'real'),(4,2,'real')])

add('Command','Behavioral','Undoable text-editor actions',
'Represent a request as an object that can be invoked and undone.',
'Buttons and shortcuts duplicate editing actions without shared undo.', 'Bind both triggers to a command; store successful edits in history.',
'pasteButton.onClick(() => editor.insert(text))\nshortcut.onPress(() => editor.insert(text))\n// duplicated action; no undo record',
'paste = new PasteCommand(editor, text)\npasteButton.bind(() => app.execute(paste))\nshortcut.bind(() => app.execute(paste))\napp.undo()',
'// PasteCommand.execute()\nbackup = editor.text; editor.insert(text)\nreturn true  // app records command in history\n// undo(): editor.text = backup',
[n('PasteButton','+ click()',0,0),n('Shortcut','+ press()',2,0),n('Editor','+ insert(text)',1,2)],[(0,2,'dep'),(1,2,'dep')],
[n('Application','- history: Command[*]\n+ execute(command)\n+ undo()',0,0),n('Command','+ execute(): Boolean\n+ undo()',2,0,'interface'),n('PasteCommand','- editor: Editor\n- backup: String\n+ execute(): Boolean\n+ undo()',2,2),n('Editor','+ text: String\n+ insert(text)',0,2)],[(0,1,'assoc'),(2,1,'real'),(2,3,'assoc')])

# UML rendering: ordinary three-compartment classes, interface stereotypes,
# hollow generalization/realization triangles, open dependencies, navigable
# associations, and hollow aggregation at the whole (Box) end.
INK='#172B4D'; BLUE='#1662C4'; RED='#B14747'; GREEN='#13746A'
def uml(nodes,edges,path):
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(660,270))
    boxes=[]
    for name,members,col,row,kind in nodes:
        x=7+col*220; y=260-row*87
        lines=members.split('\n'); h=30+len(lines)*11
        boxes.append((x,y,206,h))
    def anchor(a,b):
        x,y,w,h=a; X,Y,W,H=b; dx=(X+W/2)-(x+w/2); dy=(Y-H/2)-(y-h/2)
        if abs(dx)>abs(dy)*1.4: return (x+w if dx>0 else x,y-h/2),(X if dx>0 else X+W,Y-H/2)
        return (x+w/2,y-h if dy<0 else y),(X+W/2,Y if dy<0 else Y-H)
    import heapq
    def route(a,b,ai,bi):
        # Orthogonal visibility graph: box exteriors are obstacles, including
        # the endpoint classes. Short outward stubs keep arrowheads clear.
        def stub(point,box):
            x,y,w,h=box; px,py=point
            if px==x:return (px-6,py)
            if px==x+w:return (px+6,py)
            if py==y:return (px,py+6)
            return (px,py-6)
        aa=stub(a,boxes[ai]);bb=stub(b,boxes[bi])
        xs={0,660,a[0],b[0],aa[0],bb[0]};ys={0,270,a[1],b[1],aa[1],bb[1]}
        for x,y,w,h in boxes:
            xs.update((x-6,x+w+6,x+w/2));ys.update((y+6,y-h-6,y-h/2))
        xs=sorted(v for v in xs if 0<=v<=660);ys=sorted(v for v in ys if 0<=v<=270)
        def clear(u,v):
            for x,y,w,h in boxes:
                if u[0]==v[0]:
                    if x-2<u[0]<x+w+2 and max(min(u[1],v[1]),y-h-2)<min(max(u[1],v[1]),y+2):return False
                else:
                    if y-h-2<u[1]<y+2 and max(min(u[0],v[0]),x-2)<min(max(u[0],v[0]),x+w+2):return False
            return True
        initial=(xs.index(aa[0]),ys.index(aa[1]),-1)
        target=(xs.index(bb[0]),ys.index(bb[1]))
        queue=[(0,0,initial)];cost={initial:0};prev={};finish=None
        while queue:
            _,g,state=heapq.heappop(queue)
            if g!=cost[state]:continue
            xi,yi,last=state
            if (xi,yi)==target:finish=state;break
            for dx,dy,direction in [(1,0,0),(-1,0,0),(0,1,1),(0,-1,1)]:
                nx,ny=xi+dx,yi+dy
                if not (0<=nx<len(xs) and 0<=ny<len(ys)):continue
                u=(xs[xi],ys[yi]);v=(xs[nx],ys[ny])
                if not clear(u,v):continue
                ng=g+abs(u[0]-v[0])+abs(u[1]-v[1])+(14 if last not in (-1,direction) else 0)
                nxt=(nx,ny,direction)
                if ng<cost.get(nxt,float('inf')):
                    cost[nxt]=ng;prev[nxt]=state
                    heur=abs(v[0]-bb[0])+abs(v[1]-bb[1])
                    heapq.heappush(queue,(ng+heur,ng,nxt))
        if finish is None:raise RuntimeError('No UML route found')
        path=[];cur=finish
        while cur!=initial:path.append((xs[cur[0]],ys[cur[1]]));cur=prev[cur]
        path=[a,aa]+list(reversed(path))+[b]
        clean=[]
        for pt in path:
            if clean and clean[-1]==pt:continue
            while len(clean)>1 and ((clean[-2][0]==clean[-1][0]==pt[0]) or (clean[-2][1]==clean[-1][1]==pt[1])):clean.pop()
            clean.append(pt)
        assert all(u[0]==v[0] or u[1]==v[1] for u,v in zip(clean,clean[1:])), 'Non-orthogonal edge'
        return clean
    c.setStrokeColor(HexColor('#17212E')); c.setLineWidth(1.9)
    c.setLineJoin(0)
    for ai,bi,t in edges:
        a,b=anchor(boxes[ai],boxes[bi])
        if t=='aggregate':
            ax,ay,aw,ah=boxes[ai];bx,by,bw,bh=boxes[bi]
            a=(ax+aw,ay-ah/2);b=(bx+bw,by-bh/2)
        points=route(a,b,ai,bi)
        dx=b[0]-points[-2][0];dy=b[1]-points[-2][1];length=math.hypot(dx,dy) or 1; ux,uy=dx/length,dy/length; vx,vy=-uy,ux
        c.setDash(6,3) if t in ('dep','real') else c.setDash()
        for pa,pb in zip(points,points[1:]):c.line(*pa,*pb)
        c.setDash()
        if t in ('gen','real'):
            p=c.beginPath();p.moveTo(*b);p.lineTo(b[0]-12*ux+5*vx,b[1]-12*uy+5*vy);p.lineTo(b[0]-12*ux-5*vx,b[1]-12*uy-5*vy);p.close();c.setFillColor(white);c.drawPath(p,fill=1,stroke=1)
        elif t=='aggregate':
            dx=points[1][0]-a[0];dy=points[1][1]-a[1];length=math.hypot(dx,dy) or 1;ux,uy=dx/length,dy/length;vx,vy=-uy,ux
            p=c.beginPath();p.moveTo(*a);p.lineTo(a[0]+6*ux+3*vx,a[1]+6*uy+3*vy);p.lineTo(a[0]+12*ux,a[1]+12*uy);p.lineTo(a[0]+6*ux-3*vx,a[1]+6*uy-3*vy);p.close();c.setFillColor(white);c.drawPath(p,fill=1,stroke=1)
            c.setFont('Helvetica',8);c.drawString(b[0]+5,b[1]-12,'0..*')
        else:
            c.line(*b,b[0]-11*ux+4.5*vx,b[1]-11*uy+4.5*vy);c.line(*b,b[0]-11*ux-4.5*vx,b[1]-11*uy-4.5*vy)
    c.setLineWidth(1.25)
    for (name,members,col,row,kind),(x,y,w,h) in zip(nodes,boxes):
        c.setFillColor(white);c.rect(x,y-h,w,h,fill=1,stroke=1)
        c.setFillColor(HexColor('#DFE5F0' if kind=='interface' else '#EBEEF4'));c.rect(x,y-20,w,20,fill=1,stroke=0)
        c.setFillColor(HexColor(INK));c.setFont('Helvetica-Oblique' if kind=='abstract' else 'Helvetica-Bold',10)
        label=('<<interface>> ' if kind=='interface' else '')+name
        c.setFont('Helvetica-BoldOblique' if kind=='abstract' else 'Helvetica-Bold',min(10,190/(max(len(label),1)*.54)))
        c.drawCentredString(x+w/2,y-13,label);c.line(x,y-20,x+w,y-20)
        attrs=[s for s in members.split('\n') if '(' not in s];ops=[s for s in members.split('\n') if '(' in s]
        yy=y-31;c.setFont('Courier',8.7)
        for s in attrs: c.drawString(x+5,yy,s);yy-=11
        c.line(x,yy+6,x+w,yy+6)
        for s in ops:
            size=min(8.7,195/(len(s)*.6));c.setFont('Courier',size);c.drawString(x+5,yy-4,s)
            if '{static}' in s: c.line(x+5,yy-6,x+5+pdfmetrics.stringWidth(s,'Courier',size),yy-6)
            yy-=11
    c.save(); doc=pymupdf.open(stream=buf.getvalue(),filetype='pdf');doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(path)

def expand_group(nodes,edges):
    # Group labels in compact source become separate concrete UML classes.
    nodes=list(nodes);edges=list(edges)
    for i in range(len(nodes)):
        name,mem,col,row,kind=nodes[i]
        if ' / ' in name:
            a,b=name.split(' / ');nodes[i]=(a,mem,col,row,kind)
            # split within the same visual slot using a half-column offset
            nodes[i]=(a,mem,col,row,kind)
            # Kept as two classes by render-time geometry override below.
    return nodes,edges

# Replace compact grouped nodes with separate classes and roomier layouts.
d=DATA[1];d['snodes']=[n('Logistics','+ planDelivery()\n+ createTransport(): Transport',0,0,'abstract'),n('Transport','+ deliver()',2,0,'interface'),n('RoadLogistics','+ createTransport(): Transport',0,1),n('SeaLogistics','+ createTransport(): Transport',0,2),n('Truck','+ deliver()',2,1),n('Ship','+ deliver()',2,2)];d['sedges']=[(2,0,'gen'),(3,0,'gen'),(0,1,'dep'),(4,1,'real'),(5,1,'real')]
d=DATA[5];d['snodes']=[n('Shape','- color: Color\n+ draw() {abstract}',0,0,'abstract'),n('Color','+ apply()',2,0,'interface'),n('Circle','+ draw()',0,1),n('Square','+ draw()',0,2),n('Red','+ apply()',2,1),n('Blue','+ apply()',2,2)];d['sedges']=[(0,1,'assoc'),(2,0,'gen'),(3,0,'gen'),(4,1,'real'),(5,1,'real')]
d=DATA[2];d['snodes']=[n('FurnitureFactory','+ createChair(): Chair\n+ createSofa(): Sofa',0,0,'interface'),n('ModernFactory','+ createChair(): Chair\n+ createSofa(): Sofa',0,1),n('VictorianFactory','+ createChair(): Chair\n+ createSofa(): Sofa',0,2),n('Chair','+ sitOn()',1,0,'interface'),n('Sofa','+ lieOn()',2,0,'interface'),n('ModernChair','+ sitOn()',1,1),n('VictorianChair','+ sitOn()',1,2),n('ModernSofa','+ lieOn()',2,1),n('VictorianSofa','+ lieOn()',2,2)];d['sedges']=[(1,0,'real'),(2,0,'real'),(5,3,'real'),(6,3,'real'),(7,4,'real'),(8,4,'real')]

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

W,H=1440,810
PDF=canvas.Canvas(str(OUT/'Design Patterns.pdf'),pagesize=(W,H))
SLIDES=[]
for idx,d in enumerate(DATA):
    elements=[]
    def rect(x,y,w,h,fill):
        PDF.setFillColor(HexColor(fill));PDF.rect(x,H-y-h,w,h,fill=1,stroke=0);elements.append(('rect',x,y,w,h,fill))
    def text(s,x,y,w,size=18,color=INK,font='Helvetica',leading=None):
        lines=wrap(s,font,size,w);leading=leading or size*1.2
        PDF.setFillColor(HexColor(color));PDF.setFont(font,size)
        for j,line in enumerate(lines):PDF.drawString(x,H-y-size-j*leading,line)
        elements.append(('text',x,y,w,len(lines)*leading,s,size,color,font,leading))
        return y+len(lines)*leading
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
    for side,x,col,key in [('Problem',24,'#C5222B','problem'),('Solution',732,'#007E78','solution')]:
        rect(x,109,684,82,'#EFA5AA' if key=='problem' else '#94D9D1')
        rect(x+2,111,680,78,'#FFE2E3' if key=='problem' else '#D9F5F0')
        rect(x+10,118,5,24,col)
        text(side,x+23,114,642,25,col,font='Helvetica-Bold')
        text(d[key],x+17,151,650,17,'#192331',leading=20)
        rect(x,200,684,284,'#DFE3EC')
        rect(x+2,202,680,280,'#FFFFFF')
        rect(x+2,202,680,29,'#E4E7F0')
        label='Before (direct coupling)' if key=='problem' else 'After (using '+d['title']+')'
        text(label,x+12,205,660,18,'#151B27',font='Helvetica-Bold')
        imagepath=OUT/f'{idx+1:02d}-{key}.png'
        uml(d['pnodes' if key=='problem' else 'snodes'],d['pedges' if key=='problem' else 'sedges'],str(imagepath))
        PDF.drawImage(str(imagepath),x+11,H-234-247,660,247)
        elements.append(('image',x+11,234,660,247,str(imagepath)))
    for x,label,code in [(24,'Client Code (Before)',d['before']),(732,'Client Code (After)',d['after'])]:
        rect(x,494,684,140,'#DFE3EC')
        rect(x+2,496,680,136,'#F8F9FC')
        rect(x+2,496,680,28,'#E4E7F0')
        text(label,x+12,499,550,17,'#161D2B',font='Helvetica-Bold')
        text('Pseudocode',x+574,502,100,11,'#667085')
        text(code,x+14,533,650,16,'#18356F',font='Courier',leading=21)
    rect(24,645,1392,130,'#DFE3EC')
    rect(26,647,1388,126,'#F8F9FC')
    rect(26,647,1388,27,'#E4E7F0')
    text('Key Implementation / Notable Module',36,650,1200,17,'#161D2B',font='Helvetica-Bold')
    text('Pseudocode',1296,653,105,11,'#667085')
    text(d['module'],38,682,1364,15,'#18356F',font='Courier',leading=17)
    slug=d['title'].lower().replace(' ','-');url='https://refactoring.guru/design-patterns/'+slug;d['url']=url
    text('Source: '+url,24,788,800,10,'#566174')
    text('UML: hollow triangle = inheritance / realization; dashed open arrow = dependency',840,788,580,10,'#566174')
    PDF.showPage();SLIDES.append(elements)
PDF.save()

# Minimal standards-based OOXML. Every title, description, code line and
# caption is a native PowerPoint text run. Only UML is embedded raster media.
NS='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
def emu(v):return str(round(v*12700))
def xfrm(x,y,w,h):return f'<a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
def xmltext(e,i):
    _,x,y,w,h,s,size,color,font,leading=e
    face='Courier New' if font=='Courier' else 'Arial'
    bold=' b="1"' if font.endswith('Bold') else ''
    paragraphs=''.join(f'<a:p><a:pPr><a:lnSpc><a:spcPts val="{round(leading*100)}"/></a:lnSpc></a:pPr><a:r><a:rPr lang="en-US" sz="{round(size*100)}"{bold}><a:solidFill><a:srgbClr val="{color[1:]}"/></a:solidFill><a:latin typeface="{face}"/></a:rPr><a:t xml:space="preserve">{escape(line)}</a:t></a:r><a:endParaRPr sz="{round(size*100)}"/></a:p>' for line in wrap(s,font,size,w))
    return f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h+5)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0"/><a:lstStyle/>{paragraphs}</p:txBody></p:sp>'
def rels(items):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{i}" Type="{R}/{typ}" Target="{target}"/>' for i,typ,target in items)+'</Relationships>'
group='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
with zipfile.ZipFile(OUT/'Design Patterns.pptx','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('_rels/.rels',rels([('rId1','officeDocument','ppt/presentation.xml')]))
    slideids=''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,15))
    z.writestr('ppt/presentation.xml',f'<p:presentation xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId15"/></p:sldMasterIdLst><p:sldIdLst>{slideids}</p:sldIdLst><p:sldSz cx="{emu(W)}" cy="{emu(H)}"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
    z.writestr('ppt/_rels/presentation.xml.rels',rels([(f'rId{i}','slide',f'slides/slide{i}.xml') for i in range(1,15)]+[('rId15','slideMaster','slideMasters/slideMaster1.xml')]))
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
            elif typ=='rect':
                fill=rest[0][1:];shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Panel {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')
            else:
                imageidx+=1;rid=f'rId{imageidx+1}';name=f's{si}_{imageidx}.png';z.write(rest[0],'ppt/media/'+name);relationships.append((rid,'image','../media/'+name))
                shapes.append(f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="UML class diagram"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
        z.writestr(f'ppt/slides/slide{si}.xml',f'<p:sld xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree>{group}{"".join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
        z.writestr(f'ppt/slides/_rels/slide{si}.xml.rels',rels(relationships));overrides.append((f'/ppt/slides/slide{si}.xml','application/vnd.openxmlformats-officedocument.presentationml.slide+xml'))
    z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'+''.join(f'<Override PartName="{part}" ContentType="{ct}"/>' for part,ct in overrides)+'</Types>')

# Self-contained printable HTML, with selectable text and embedded UML only.
import base64
pages=[]
for elements in SLIDES:
    parts=[]
    for e in elements:
        typ,x,y,w,h,*r=e;style=f'position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
        if typ=='rect':parts.append(f'<div style="{style}background:{r[0]}"></div>')
        elif typ=='image':parts.append(f'<img alt="UML class diagram" style="{style}" src="data:image/png;base64,{base64.b64encode(Path(r[0]).read_bytes()).decode()}">')
        else:
            s,size,color,font,leading=r;family='Courier New' if font=='Courier' else 'Arial';weight='bold' if font.endswith('Bold') else 'normal'
            lines=wrap(s,font,size,w);parts.append(f'<div style="{style}font-family:{family};font-size:{size}px;line-height:{leading}px;color:{color};font-weight:{weight};white-space:pre;">{html.escape(chr(10).join(lines))}</div>')
    pages.append('<section>'+''.join(parts)+'</section>')
(OUT/'Design Patterns.html').write_text('<!doctype html><html><head><meta charset="utf-8"><title>Design Patterns</title><style>@page{size:15in 8.4375in;margin:0}*{box-sizing:border-box}body{margin:0;background:#cbd5e1}section{position:relative;width:1440px;height:810px;background:white;break-after:page;margin:20px auto}@media print{body{background:white}section{margin:0}}</style></head><body>'+''.join(pages)+'</body></html>',encoding='utf-8')
(OUT/'content.json').write_text(json.dumps(DATA,indent=2),encoding='utf-8')
print('Created 14-slide PPTX, PDF, and HTML in',OUT)
