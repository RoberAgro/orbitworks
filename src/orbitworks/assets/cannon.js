/* One browser-owned launch state drives native sliders, numeric inputs and the
 * canvas. Dash receives an immutable snapshot only when Fire is pressed.
 */
(function () {
    "use strict";
    const TAU = 2 * Math.PI;
    const colors = ["#70d0ff", "#ffc579", "#ade6a2", "#cdb2ff", "#ff969e", "#78dfcf"];
    const el = (id) => document.getElementById(id);
    const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
    const mod = (value, period) => ((value % period) + period) % period;
    const wrapAngle = (angle) => mod(angle + 180, 360) - 180;
    const durationLabel = (seconds) => seconds < 60 ? `${seconds.toFixed(1)} s` :
        seconds < 3600 ? `${(seconds / 60).toFixed(1)} min` :
        seconds < 86400 ? `${(seconds / 3600).toFixed(2)} h` : seconds < 31557600 ? `${(seconds / 86400).toFixed(2)} d` : `${(seconds / 31557600).toFixed(2)} yr`;

    function elapsedTimeLabel(seconds) {
        const [value, abbreviation] = durationLabel(seconds).split(" ");
        const units = {s: "second", min: "minute", h: "hour", d: "day", yr: "year"};
        return `${value} ${units[abbreviation]}${Number(value) === 1 ? "" : "s"}`;
    }

    function preview(launch, outerRadius) {
        /* In R, sqrt(R^3/GM) units, GM=1. Infer ell, energy and eccentricity
         * vector from the launch state, then sample r=p/(1+e*cos(nu)) in the
         * direction of motion. Solve radius crossings analytically before
         * sampling, including shallow impacts a sampled sign test could miss.
         * This is geometry only; it never integrates the time-dependent ODE.
         */
        const {x, y, ratio, angle} = launch;
        const radius = Math.hypot(x, y), phi = Math.atan2(y, x);
        const alpha = angle * Math.PI / 180;
        const speed = ratio / Math.sqrt(radius);
        // The launch angle is counterclockwise from the fixed positive x-axis.
        const vx = speed * Math.cos(alpha), vy = speed * Math.sin(alpha);
        const vr = (x * vx + y * vy) / radius;
        const vt = (x * vy - y * vx) / radius;
        const energy = speed * speed / 2 - 1 / radius;
        const ell = radius * vt;
        const dot = x * vx + y * vy;
        const ex = (speed * speed - 1 / radius) * x - dot * vx;
        const ey = (speed * speed - 1 / radius) * y - dot * vy;
        const e = Math.hypot(ex, ey);
        const parabolic = Math.abs(energy) < 1e-12 / radius;
        const bound = energy < 0 && !parabolic;
        const type = Math.abs(ell) < 1e-8 ? "Radial" : parabolic ? "Parabolic" :
            bound ? (e < 1e-8 ? "Circular" : "Elliptical") : "Hyperbolic";

        if (Math.abs(ell) < 1e-8) {
            const points = [[x, y]];
            const atRadius = (r) => [r * Math.cos(phi), r * Math.sin(phi)];
            let outcome = "impact";
            if (vr > 0) {
                const turn = bound ? -1 / energy : Infinity;
                points.push(atRadius(Math.min(turn, outerRadius)));
                if (turn >= outerRadius) outcome = "out of range";
                else points.push(atRadius(1));
            } else points.push(atRadius(1));
            return {points, type, outcome, eccentricity: e};
        }

        const direction = Math.sign(ell);
        const periAngle = e > 1e-12 ? Math.atan2(ey, ex) : phi;
        const start = Math.atan2(Math.sin(phi - periAngle), Math.cos(phi - periAngle));
        const p = ell * ell;
        let end = TAU, outcome = "complete orbit";
        function limitAtRadius(target, outward, label) {
            if (e < 1e-12) return;
            const cosine = (p / target - 1) / e;
            if (cosine < -1 || cosine > 1) return;
            const root = Math.acos(clamp(cosine, -1, 1));
            for (const nu of [root, -root]) {
                // dr/dt has the sign of ell*e*sin(nu).
                if ((direction * Math.sin(nu) > 0) !== outward) continue;
                const travel = mod(direction * (nu - start), TAU);
                if (travel > 1e-12 && travel < end) { end = travel; outcome = label; }
            }
        }
        limitAtRadius(1, false, "impact");
        limitAtRadius(outerRadius, true, "out of range");
        const points = [];
        const count = 700;
        for (let i = 0; i <= count; i++) {
            const nu = start + direction * end * i / count;
            const denominator = 1 + e * Math.cos(nu);
            if (denominator <= 0) break;
            const r = p / denominator;
            points.push([r * Math.cos(nu + periAngle), r * Math.sin(nu + periAngle)]);
        }
        // Preserve the specified muzzle exactly despite roundoff in the conic.
        points[0] = [x, y];
        return {points, type, outcome, eccentricity: e};
    }

    function sample(flight, time) {
        // Cubic Hermite interpolation uses the computed positions AND
        // velocities; it preserves smooth motion between adaptive samples.
        const t = flight.time;
        if (time <= 0) return {x: flight.x[0], y: flight.y[0], index: 0};
        if (time >= flight.duration) {
            const i = t.length - 1;
            return {x: flight.x[i], y: flight.y[i], index: i};
        }
        let low = 0, high = t.length - 1;
        while (high - low > 1) {
            const middle = (low + high) >> 1;
            if (t[middle] <= time) low = middle; else high = middle;
        }
        const dt = t[high] - t[low], u = (time - t[low]) / dt;
        const a = 2*u**3 - 3*u**2 + 1, b = u**3 - 2*u**2 + u;
        const c = -2*u**3 + 3*u**2, d = u**3 - u**2;
        return {
            x: a*flight.x[low] + b*dt*flight.vx[low] + c*flight.x[high] + d*dt*flight.vx[high],
            y: a*flight.y[low] + b*dt*flight.vy[low] + c*flight.y[high] + d*dt*flight.vy[high], index: low,
        };
    }

    class CannonScene {
        constructor(canvas, config) {
            this.canvas = canvas; this.ctx = canvas.getContext("2d"); this.config = config;
            this.fontFamily = getComputedStyle(canvas).fontFamily;
            this.launch = { ...config.defaults }; this.controls = {};
            this.camera = {x: 0, y: 0, radius: 3.0}; this.follow = null;
            this.clock = 0; this.paused = false; this.epoch = 0;
            this.connection = "connecting";
            this.flights = []; this.seen = new Set(); this.selected = null; this.nextNumber = 1;
            this.expanded = null; this.doubleEligible = false;
            this.pending = null; this.lastFrame = performance.now(); this.lastStatus = 0;
            this.drag = null; this.preview = null;
            this.buildControls(); this.bindEvents(); this.resize(); this.refreshLaunch();
            this.observer = new ResizeObserver(() => this.resize());
            this.observer.observe(canvas.parentElement);
            this.checkConnection();
            requestAnimationFrame((now) => this.tick(now));
        }

        makeControl(key, title, minimum, maximum, step, hint, ticks, logarithmic=false) {
            const container=el(key+"-control");
            const heading=document.createElement("div");heading.className="control-heading";
            const label=document.createElement("label");label.textContent=title;label.htmlFor=key+"-number";label.tabIndex=0;
            const tooltip=document.createElement("span");tooltip.className="control-tooltip";tooltip.id=key+"-tooltip";tooltip.setAttribute("role","tooltip");tooltip.textContent=hint;
            label.setAttribute("aria-describedby",tooltip.id);heading.append(label,tooltip);
            const row=document.createElement("div");row.className="control-row";
            const track=document.createElement("div");track.className="slider-track";
            const number=document.createElement("input");number.type="number";number.id=key+"-number";
            number.min=minimum;number.max=maximum;number.step="any";number.title=hint;number.className="control-value";
            number.setAttribute("aria-describedby",tooltip.id);
            const range=document.createElement("input");range.type="range";range.id=key+"-slider";
            const localPosition=key==="x" || key==="y";
            range.min=localPosition ? -this.config.positionSliderLimit : logarithmic ? Math.log10(minimum) : minimum;
            range.max=localPosition ? this.config.positionSliderLimit : logarithmic ? Math.log10(maximum) : maximum;
            range.step=step;range.setAttribute("aria-label",title);range.title=hint;
            const marks=document.createElement("div");marks.className="slider-ticks";
            for(const [value,text] of ticks) {
                const mark=document.createElement("span");mark.textContent=text;
                const displayValue=logarithmic ? Math.log10(value) : value;
                mark.style.left=((displayValue-Number(range.min))/(Number(range.max)-Number(range.min))*100)+"%";
                marks.append(mark);
            }
            track.append(range,marks);row.append(track,number);container.append(heading,row);
            this.controls[key]={number,range,logarithmic,hint};
            range.addEventListener("input",()=>{
                const value=logarithmic ? 10**Number(range.value) : Number(range.value);
                this.setLaunch({[key]:value});
            });
            number.addEventListener("input",()=>{
                if(number.value==="" || !number.validity.valid) {
                    number.setAttribute("aria-invalid","true");this.refreshLaunch();return;
                }
                number.removeAttribute("aria-invalid");
                this.setLaunch({[key]:Number(number.value)},key);
            });
            const finishEditing=()=>{
                if(number.value!=="" && number.validity.valid && number.getAttribute("aria-invalid")!=="true") this.syncControl(key);
                this.refreshLaunch();
            };
            number.addEventListener("blur",finishEditing);
            number.addEventListener("keydown",(event)=>{if(event.key==="Enter"){finishEditing();number.blur();}});
            range.addEventListener("keydown",(event)=>event.stopPropagation());
        }

        buildControls() {
            const limit=this.config.positionSliderLimit;
            const positionTicks=[[-limit,"−"+limit],[0,"0"],[limit,String(limit)]];
            this.makeControl("x","Horizontal position",-this.config.positionLimit,this.config.positionLimit,0.001,
                "Horizontal distance from Earth's centre, measured in Earth radii. Negative is left; positive is right. This slider spans −10 to +10; the number box and scene accept ±10,000.",positionTicks);
            this.makeControl("y","Vertical position",-this.config.positionLimit,this.config.positionLimit,0.001,
                "Vertical distance from Earth's centre, measured in Earth radii. Negative is down; positive is up. The slider spans −10 to +10, independently of the wider number-box and scene range. Launch positions must be above the surface.",positionTicks);
            this.makeControl("ratio","Launch speed",0,this.config.maxRatio,0.001,
                "Speed divided by the local circular speed vc = √(GM/r). A tangential launch (sideways around Earth) at 1 is circular; √2 ≈ 1.4142 is escape speed. Direction can still lead to impact. Moving the launcher preserves this ratio and updates the actual km/s.",[[0,"0"],[1,"1"],[2,"2"],[3,"3"]]);
            const reference=document.createElement("span");reference.id="speed-reference";reference.className="inline-reference";
            el("ratio-control").querySelector(".control-heading").append(reference);
            this.makeControl("angle","Launch angle",-180,180,0.1,
                "Angle in degrees, measured counterclockwise from the right: 0° points right and 90° points up.",[[-180,"−180"],[0,"0"],[180,"180"]]);
            this.makeControl("rate","Time multiplier",1,this.config.maxRate,0.01,
                "Simulated seconds per real second, shared by every flight. 1 is real time; 2,000 makes a low Earth orbit take about 3 seconds. The slider is logarithmic. Very high rates can make short orbits appear to jump between frames.",[[1,"1"],[1e5,"10⁵"],[1e10,"10¹⁰"]],true);
            for(const key of Object.keys(this.controls)) this.syncControl(key);
        }

        syncControl(key, keepTyped) {
            const {number,range,logarithmic,hint}=this.controls[key],value=this.launch[key];
            // Four decimals are a presentation choice; never round the state
            // used by preview, simulation or an in-progress drag.
            if(!keepTyped) {number.value=value.toFixed(4);number.removeAttribute("aria-invalid");}
            number.style.fontSize=number.value.length>12 ? "9px" : "";
            const displayValue=logarithmic ? Math.log10(value) : value;
            range.value=clamp(displayValue,Number(range.min),Number(range.max));
            const outside=displayValue<Number(range.min) || displayValue>Number(range.max);
            range.title=outside ? "Actual value "+value.toFixed(4)+" is outside this slider's range. It is retained for the simulation. Moving this slider chooses a new value within its displayed range." : hint;
        }

        setLaunch(changes, keepTyped) {
            if (Object.hasOwn(changes, "rate")) this.advance(performance.now());
            Object.assign(this.launch, changes);
            for (const key of Object.keys(changes)) this.syncControl(key, key === keepTyped);
            this.refreshLaunch();
        }

        refreshLaunch() {
            const {x,y,ratio}=this.launch;
            const r=Math.hypot(x,y);
            const invalidField=Object.values(this.controls).some(({number})=>number.getAttribute("aria-invalid")==="true");
            this.valid=!invalidField && r>=this.config.minRadius && Math.abs(x)<=this.config.positionLimit && Math.abs(y)<=this.config.positionLimit;
            const message=invalidField ? "Complete the highlighted input." :
                r<this.config.minRadius ? "Place the launcher above Earth’s surface." :
                Math.abs(x)>this.config.positionLimit || Math.abs(y)>this.config.positionLimit ? "Coordinates must stay within ±10,000 R⊕." : "";
            el("launch-validity").textContent=message;
            el("fire").disabled=!this.valid || this.pending!==null || this.connection!=="connected";
            for (const key of ["x","y"]) this.controls[key].number.title=this.controls[key].hint+" Current value: "+(this.launch[key]*this.config.radiusKm).toLocaleString(undefined,{maximumFractionDigits:1})+" km.";
            const vc=r>0 ? Math.sqrt(this.config.gm/(r*this.config.radiusKm*1000))/1000 : NaN;
            el("speed-reference").textContent=Number.isFinite(vc) ? (ratio*vc).toFixed(3)+" km/s" : "—";
            el("speed-reference").title="Local circular speed: "+vc.toFixed(3)+" km/s. Position changes preserve v/vc.";
            this.preview=this.valid ? preview(this.launch,this.config.outerRadius) : null;
            el("preview-label").textContent=this.preview ?
                "Preview · "+this.preview.type+" · "+this.preview.outcome : "Invalid launch position";
        }

        bindEvents() {
            const onClick = (id, callback) => el(id).addEventListener("click", callback);
            onClick("fire", () => this.fire());
            onClick("clear", () => this.clear());
            onClick("pause", () => this.pause());
            onClick("centre", () => { this.follow = null; this.camera = {x: 0, y: 0, radius: 3}; });
            onClick("fit", () => this.fit());
            onClick("follow", () => {
                this.follow = this.follow ? null : this.selected;
                if (!this.selected) el("launch-message").textContent = "Select a flight in the log first.";
            });
            onClick("zoom-in", () => this.zoom(1/1.4, this.width/2, this.height/2));
            onClick("zoom-out", () => this.zoom(1.4, this.width/2, this.height/2));
            onClick("controls-help", () => el("controls-dialog").showModal());
            onClick("close-help", () => el("controls-dialog").close());
            this.canvas.addEventListener("contextmenu", (event) => event.preventDefault());
            this.canvas.addEventListener("wheel", (event) => {
                event.preventDefault();
                if (event.shiftKey) {
                    this.setLaunch({angle: wrapAngle(this.launch.angle - 2*Math.sign(event.deltaY))});
                    return;
                }
                const p = this.pointer(event);
                this.zoom(Math.exp(clamp(event.deltaY, -200, 200)*0.002), p.x, p.y);
            }, {passive: false});
            this.canvas.addEventListener("click", (event) => {
                // PointerEvent.detail is zero in browsers; click events carry
                // the click count. Remember where each press actually began.
                this.doubleEligible=event.detail===1 ? this.clickOnBase : this.doubleEligible && this.clickOnBase;
            });
            this.canvas.addEventListener("dblclick", (event) => {
                const p=this.pointer(event), base=this.handles().base;
                if (this.doubleEligible && Math.hypot(p.x-base.x,p.y-base.y)<13) {
                    event.preventDefault();this.fire();
                }
                this.doubleEligible=false;
            });
            this.canvas.addEventListener("pointerdown", (event) => this.pointerDown(event));
            this.canvas.addEventListener("pointermove", (event) => this.pointerMove(event));
            const endDrag = (event) => {
                this.drag = null;
                if (this.canvas.hasPointerCapture(event.pointerId)) this.canvas.releasePointerCapture(event.pointerId);
                this.canvas.style.cursor = "crosshair";
            };
            this.canvas.addEventListener("pointerup", endDrag);
            this.canvas.addEventListener("pointercancel", endDrag);
            document.addEventListener("visibilitychange", () => { this.lastFrame = performance.now(); this.renderStatus(); });
            document.addEventListener("keydown", (event) => {
                if (el("controls-dialog").open || event.repeat || event.ctrlKey || event.altKey || event.metaKey) return;
                if (event.target.closest("input, textarea, select, [contenteditable=true]")) return;
                if (event.key.toLowerCase() === "f") { event.preventDefault(); this.fire(); }
                else if (event.code === "Space") { event.preventDefault(); this.pause(); }
                else if (event.key === "Home") { event.preventDefault(); el("centre").click(); }
                else if (event.key.toLowerCase() === "h") { event.preventDefault(); el("controls-dialog").showModal(); }
            });
        }

        pointer(event) {
            const rect = this.canvas.getBoundingClientRect();
            return {x: event.clientX - rect.left, y: event.clientY - rect.top};
        }

        scale() { return Math.min(this.width, this.height) / (2*this.camera.radius); }
        screen(x, y) { const s = this.scale(); return {x: this.width/2+(x-this.camera.x)*s, y: this.height/2-(y-this.camera.y)*s}; }
        world(x, y) { const s = this.scale(); return {x: this.camera.x+(x-this.width/2)/s, y: this.camera.y-(y-this.height/2)/s}; }

        handles() {
            const base = this.screen(this.launch.x, this.launch.y);
            const heading = this.launch.angle*Math.PI/180;
            const length=20+44*this.launch.ratio;
            return {base, tip: {x: base.x+length*Math.cos(heading), y: base.y-length*Math.sin(heading)}};
        }

        pointerDown(event) {
            if (event.button !== 0 && event.button !== 2) return;
            this.clickOnBase=false;
            event.preventDefault(); this.canvas.focus();
            const p = this.pointer(event), {base, tip} = this.handles();
            if (event.button === 2) {
                this.follow = null;
                this.drag = {mode: "pan", p, camera: {...this.camera}};
                this.canvas.style.cursor = "grabbing";
            } else if (Math.hypot(p.x-tip.x, p.y-tip.y) < 13) {
                this.doubleEligible=false;
                this.drag = {mode: "aim", offset: {x:p.x-tip.x,y:p.y-tip.y}};
            } else {
                const onBase = Math.hypot(p.x-base.x, p.y-base.y) < 13;
                this.clickOnBase=onBase;
                this.drag = {mode: "position", start: p, offset: onBase ? {x: p.x-base.x, y: p.y-base.y} : {x: 0, y: 0}};
                this.follow = null;
                this.pointerMove(event);
            }
            this.canvas.setPointerCapture(event.pointerId);
        }

        pointerMove(event) {
            const p = this.pointer(event);
            if (!this.drag) {
                const {base, tip} = this.handles();
                this.canvas.style.cursor = Math.hypot(p.x-tip.x,p.y-tip.y)<13 ? "grab" :
                    Math.hypot(p.x-base.x,p.y-base.y)<13 ? "move" : "crosshair";
                return;
            }
            if (this.drag.mode === "pan") {
                this.camera.x = this.drag.camera.x - (p.x-this.drag.p.x)/this.scale();
                this.camera.y = this.drag.camera.y + (p.y-this.drag.p.y)/this.scale();
            } else if (this.drag.mode === "aim") {
                const base = this.handles().base;
                const dx=p.x-this.drag.offset.x-base.x, dy=p.y-this.drag.offset.y-base.y;
                const distance=Math.hypot(dx,dy);
                const heading=Math.atan2(-dy,dx);
                const angle=distance>2 ? wrapAngle(heading*180/Math.PI) : this.launch.angle;
                this.setLaunch({angle, ratio:clamp((distance-20)/44,0,this.config.maxRatio)});
            } else {
                if(Math.hypot(p.x-this.drag.start.x,p.y-this.drag.start.y)>4) { this.doubleEligible=false; this.clickOnBase=false; }
                const point = this.world(p.x-this.drag.offset.x, p.y-this.drag.offset.y);
                // Keep invalid interior positions visible and disable firing;
                // do not silently snap to a different physical launch point.
                this.setLaunch({x: point.x, y: point.y});
            }
        }

        zoom(factor, x, y) {
            const anchor = this.world(x, y);
            this.camera.radius = clamp(this.camera.radius*factor, 0.02, this.config.outerRadius*2);
            if (!this.follow) {
                const after = this.world(x, y);
                this.camera.x += anchor.x-after.x; this.camera.y += anchor.y-after.y;
            }
        }

        fire() {
            if (!this.valid || this.pending !== null || this.connection!=="connected") return;
            const request = {id: crypto.randomUUID(), epoch: this.epoch, ...this.launch};
            this.pending = request.id;
            el("fire").disabled = true; el("fire").textContent = "Computing flight…";
            el("launch-message").textContent = "Other flights keep moving while this shot is calculated.";
            window.dash_clientside.set_props("launch-request", {data: request});
        }

        receive(result) {
            if (!result || this.seen.has(result.request_id)) return;
            this.seen.add(result.request_id);
            if (result.request_id === this.pending) {
                this.pending = null; el("fire").textContent = "Launch";
            }
            this.refreshLaunch();
            if (result.epoch !== this.epoch) return;
            if (result.error) { el("launch-message").textContent = result.error; return; }
            this.advance(performance.now());
            this.add(result.flight);
            el("launch-message").textContent = "";
        }

        add(flight) {
            flight.start=this.clock;flight.number=this.nextNumber++;
            flight.color=colors[(flight.number-1)%colors.length];flight.visible=true;
            flight.point=sample(flight,0);flight.trailIndex=0;
            const card=document.createElement("div");card.className="flight-card";card.style.setProperty("--flight-color",flight.color);
            const select=document.createElement("button");select.className="flight-select";
            const identity=document.createElement("span");identity.className="flight-identity";
            const dot=document.createElement("span");dot.className="flight-dot";identity.append(dot);
            const name=document.createElement("strong");name.textContent="Flight "+flight.number;identity.append(name);
            const status=document.createElement("span");status.className="status-pill";status.textContent="Flying";
            select.append(identity,status);select.addEventListener("click",()=>this.select(flight));
            const summary=document.createElement("div");summary.className="flight-summary";
            summary.textContent=flight.orbit_type+" · e "+flight.eccentricity.toFixed(3);
            const tools=document.createElement("div");tools.className="flight-tools";
            const details=document.createElement("button");details.textContent="Details";details.setAttribute("aria-expanded","false");
            const body=document.createElement("div");body.className="flight-metrics";body.hidden=true;
            const metric=(label,value,id)=>{
                const tile=document.createElement("div");tile.className="metric";
                const heading=document.createElement("span");heading.textContent=label;
                const content=document.createElement("strong");content.textContent=value;tile.append(heading,content);body.append(tile);
                if(id) flight[id]=content;
            };
            metric("Current distance","—","distanceMetric");
            metric("Flight age","—","ageMetric");
            metric("Launch speed",flight.speed.toFixed(3)+" km/s");
            metric("Speed / vc",flight.speed_ratio.toFixed(3));
            metric("Launch angle",flight.angle.toFixed(1)+"°");
            metric("Period",flight.period ? durationLabel(flight.period) : "Unbound");
            metric("Launch x",flight.launch_x.toLocaleString(undefined,{maximumFractionDigits:3})+" R⊕");
            metric("Launch y",flight.launch_y.toLocaleString(undefined,{maximumFractionDigits:3})+" R⊕");
            metric("Periapsis",flight.periapsis.toLocaleString(undefined,{maximumFractionDigits:3})+" R⊕");
            metric("Apoapsis",flight.apoapsis!==null ? flight.apoapsis.toLocaleString(undefined,{maximumFractionDigits:3})+" R⊕" : "Unbounded");
            metric("Max energy drift",flight.energy_error.toExponential(2)+"%");
            metric("Computed duration",durationLabel(flight.duration));
            const note=document.createElement("p");note.className="metrics-note";
            note.textContent="Energy drift relative to "+flight.energy_normalization+". "+
                (flight.repeat ? "One numerical period, replayed after the first lap." : "Geometric periapsis may be inside Earth; the flight stops at contact.");
            body.append(note);
            details.addEventListener("click",()=>{
                this.select(flight);
                const opening=body.hidden;
                for(const shot of this.flights) {shot.detailBody.hidden=true;shot.detailButton.setAttribute("aria-expanded","false");shot.detailButton.textContent="Details";}
                body.hidden=!opening;details.setAttribute("aria-expanded",String(opening));details.textContent=opening ? "Less" : "Details";
            });
            const visibility=document.createElement("button");visibility.textContent="Hide";visibility.title="Hide this flight";
            visibility.addEventListener("click",()=>{
                flight.visible=!flight.visible;visibility.textContent=flight.visible ? "Hide" : "Show";
                if(!flight.visible && this.follow===flight.id)this.follow=null;
            });
            const remove=document.createElement("button");remove.textContent="×";remove.className="remove-flight";remove.title="Remove flight";remove.setAttribute("aria-label","Remove flight "+flight.number);
            remove.addEventListener("click",()=>{
                this.flights=this.flights.filter(shot=>shot!==flight);card.remove();
                if(this.follow===flight.id)this.follow=null;
                if(this.selected===flight.id)this.selected=null;
                el("flight-count").textContent=this.flights.length;el("empty-log").hidden=this.flights.length>0;
            });
            tools.append(details,visibility,remove);card.append(select,summary,tools,body);el("flight-log").append(card);
            flight.card=card;flight.statusElement=status;flight.detailBody=body;flight.detailButton=details;
            this.flights.push(flight);this.select(flight);el("flight-count").textContent=this.flights.length;el("empty-log").hidden=true;
        }

        select(flight) {
            this.selected=flight.id;
            this.flights.forEach(shot=>shot.card.classList.toggle("selected",shot.id===flight.id));
        }

        clear() {
            this.epoch++; this.flights = []; this.selected = null; this.follow = null;
            this.nextNumber = 1;
            this.clock = 0; this.lastFrame = performance.now();
            el("flight-log").replaceChildren(); el("flight-count").textContent = "0";
            el("empty-log").hidden=false;
            el("launch-message").textContent = this.pending ? "Cleared. The pending shot will be discarded." : "";
        }

        pause() {
            this.advance(performance.now()); this.paused = !this.paused;
            el("pause").textContent = this.paused ? "Resume" : "Pause";
            this.renderStatus();
        }

        advance(now) {
            if (!this.paused && !document.hidden && this.connection==="connected" && this.hasMovingFlights()) this.clock += Math.max(0, now-this.lastFrame)/1000*this.launch.rate;
            this.lastFrame = now;
        }

        hasMovingFlights() {
            return this.flights.some(flight=>flight.repeat || this.clock-flight.start<flight.duration);
        }

        renderStatus() {
            let state, label;
            if(this.connection==="connecting") {state="connecting";label="Connecting";}
            else if(this.connection!=="connected") {state="disconnected";label="Stopped · disconnected";}
            else if(this.paused || document.hidden) {state="paused";label="Paused";}
            else if(!this.hasMovingFlights()) {state="stopped";label="Stopped";}
            else {state="running";label="Running";}
            el("simulation-status").dataset.state=state;
            el("simulation-status-label").textContent=label;
            el("simulation-status").title=this.connection==="connected" ? "Connected to the local app server" : "Checking the local app connection";
        }

        async checkConnection() {
            // Heartbeats are independent of numerical flight requests and RAF.
            // A timeout ensures an unreachable server cannot leave a green light.
            const controller=new AbortController();
            const timeout=setTimeout(()=>controller.abort(),1500);
            try {
                const response=await fetch("/health",{cache:"no-store",signal:controller.signal});
                if(!response.ok || (await response.json()).app!=="orbitworks") throw Error("Server unavailable");
                this.advance(performance.now());
                const reconnecting=this.connection==="disconnected";
                this.connection="connected";
                if(reconnecting) {
                    this.paused=true;el("pause").textContent="Resume";
                    el("launch-message").textContent="Reconnected. Resume when you are ready.";
                }
            } catch(error) {
                this.advance(performance.now());
                this.connection="disconnected";
                if(this.pending) {this.seen.add(this.pending);this.pending=null;el("fire").textContent="Launch";}
                el("launch-message").textContent="Server disconnected. Restart the app to continue.";
            } finally {
                clearTimeout(timeout);
                this.refreshLaunch();this.renderStatus();
                this.heartbeat=setTimeout(()=>this.checkConnection(),2000);
            }
        }

        fit() {
            let xmin = -1, xmax = 1, ymin = -1, ymax = 1;
            const include = (x,y) => { xmin=Math.min(xmin,x); xmax=Math.max(xmax,x); ymin=Math.min(ymin,y); ymax=Math.max(ymax,y); };
            include(this.launch.x,this.launch.y);
            for (const flight of this.flights.filter((shot) => shot.visible)) {
                for (let i=0; i<=flight.trailIndex; i++) include(flight.x[i],flight.y[i]);
                include(flight.point.x,flight.point.y);
            }
            this.follow = null; this.camera.x=(xmin+xmax)/2; this.camera.y=(ymin+ymax)/2;
            this.camera.radius = Math.max(1.2, Math.max((xmax-xmin)/this.width,(ymax-ymin)/this.height)*Math.min(this.width,this.height)/2*1.15);
        }

        resize() {
            const rect = this.canvas.parentElement.getBoundingClientRect();
            this.width = rect.width; this.height = rect.height;
            this.dpr = Math.min(window.devicePixelRatio || 1, 2);
            this.canvas.width = Math.round(rect.width*this.dpr); this.canvas.height = Math.round(rect.height*this.dpr);
        }

        tick(now) {
            this.advance(now);
            for (const flight of this.flights) {
                const age = Math.max(0,this.clock-flight.start);
                flight.point = sample(flight, flight.repeat ? age%flight.duration : Math.min(age,flight.duration));
                flight.trailIndex = age>=flight.duration ? flight.time.length-1 : flight.point.index;
            }
            if (this.follow) {
                const shot = this.flights.find((flight) => flight.id===this.follow);
                if (shot) { this.camera.x=shot.point.x; this.camera.y=shot.point.y; }
            }
            this.draw();
            if (now-this.lastStatus>120) {
                el("simulation-clock").textContent = `Time elapsed: ${elapsedTimeLabel(this.clock)}`;
                this.renderStatus();
                for (const flight of this.flights) {
                    const age = this.clock-flight.start;
                    const status=age<flight.duration ? "Flying" : flight.repeat ? "Lap "+(Math.floor(age/flight.duration)+1) : flight.outcome;
                    flight.statusElement.textContent=status;
                    flight.statusElement.dataset.state=age<flight.duration || flight.repeat ? "flying" : flight.outcome;
                    if(!flight.detailBody.hidden) {
                        flight.distanceMetric.textContent=Math.hypot(flight.point.x,flight.point.y).toLocaleString(undefined,{maximumFractionDigits:3})+" R⊕";
                        flight.ageMetric.textContent=durationLabel(flight.repeat ? age : Math.min(age,flight.duration));
                    }
                }
                el("follow").classList.toggle("active", Boolean(this.follow));
                el("follow").textContent = this.follow ? "Release follow" : "Follow selected";
                el("camera-status").textContent = `${this.follow ? "Following projectile" : "Free camera"} · centre (${this.camera.x.toFixed(2)}, ${this.camera.y.toFixed(2)}) R⊕`;
                this.lastStatus=now;
            }
            requestAnimationFrame((next) => this.tick(next));
        }

        strokePath(points, color, dashed, width) {
            const ctx=this.ctx;
            ctx.beginPath();
            points.forEach(([x,y],i) => { const p=this.screen(x,y); if(i===0)ctx.moveTo(p.x,p.y); else ctx.lineTo(p.x,p.y); });
            ctx.strokeStyle=color; ctx.lineWidth=width; ctx.setLineDash(dashed ? [4,5] : []); ctx.stroke(); ctx.setLineDash([]);
        }

        draw() {
            const ctx=this.ctx, w=this.width, h=this.height, scale=this.scale();
            ctx.setTransform(this.dpr,0,0,this.dpr,0,0); ctx.clearRect(0,0,w,h);
            // Grid follows the camera; powers of 2 remain useful at every zoom.
            const spacing=2**Math.floor(Math.log2(this.camera.radius/2));
            const low=this.world(0,h), high=this.world(w,0);
            ctx.beginPath(); ctx.strokeStyle="#203147"; ctx.lineWidth=1;
            for(let x=Math.ceil(low.x/spacing)*spacing; x<=high.x; x+=spacing) { const p=this.screen(x,0); ctx.moveTo(p.x,0); ctx.lineTo(p.x,h); }
            for(let y=Math.ceil(low.y/spacing)*spacing; y<=high.y; y+=spacing) { const p=this.screen(0,y); ctx.moveTo(0,p.y); ctx.lineTo(w,p.y); }
            ctx.stroke();
            el("view-scale").textContent=`Grid ${Number(spacing.toPrecision(3))} R⊕`;
            if(this.preview) this.strokePath(this.preview.points,"#b9c7da99",true,1);

            for(const flight of this.flights.filter((shot)=>shot.visible)) {
                ctx.beginPath();
                for(let i=0;i<=flight.trailIndex;i++) { const p=this.screen(flight.x[i],flight.y[i]); if(i===0)ctx.moveTo(p.x,p.y); else ctx.lineTo(p.x,p.y); }
                if(this.clock-flight.start<flight.duration) { const p=this.screen(flight.point.x,flight.point.y); ctx.lineTo(p.x,p.y); }
                ctx.strokeStyle=flight.color; ctx.globalAlpha=flight.id===this.selected ? 0.95 : 0.55;
                ctx.lineWidth=flight.id===this.selected ? 1.8 : 1.2; ctx.stroke(); ctx.globalAlpha=1;
            }

            const earth=this.screen(0,0), light=this.screen(-0.35,0.4);
            const gradient=ctx.createRadialGradient(light.x,light.y,0,earth.x,earth.y,scale);
            gradient.addColorStop(0,"#497ea4"); gradient.addColorStop(1,"#213f5d");
            ctx.beginPath(); ctx.arc(earth.x,earth.y,scale,0,TAU); ctx.fillStyle=gradient; ctx.fill();
            ctx.strokeStyle="#6fa1c377"; ctx.lineWidth=1.5; ctx.stroke();
            if(scale>25) { ctx.fillStyle="#bed5e6"; ctx.font=`11px ${this.fontFamily}`; ctx.textAlign="center"; ctx.fillText("EARTH",earth.x,earth.y+4); }

            const {base,tip}=this.handles();
            ctx.strokeStyle=this.valid ? "#f0f5ff" : "#ff797d"; ctx.fillStyle=ctx.strokeStyle; ctx.lineWidth=2;
            ctx.beginPath(); ctx.moveTo(base.x,base.y); ctx.lineTo(tip.x,tip.y); ctx.stroke();
            ctx.beginPath(); ctx.arc(base.x,base.y,7,0,TAU); ctx.fill();
            const heading=Math.atan2(tip.y-base.y,tip.x-base.x);
            ctx.beginPath(); ctx.moveTo(tip.x,tip.y);
            ctx.lineTo(tip.x-12*Math.cos(heading-0.45),tip.y-12*Math.sin(heading-0.45));
            ctx.lineTo(tip.x-12*Math.cos(heading+0.45),tip.y-12*Math.sin(heading+0.45)); ctx.closePath(); ctx.fill();
            ctx.beginPath(); ctx.arc(tip.x,tip.y,10,0,TAU); ctx.strokeStyle="#a1b5d077"; ctx.lineWidth=1; ctx.stroke();

            for(const flight of this.flights.filter((shot)=>shot.visible)) {
                const p=this.screen(flight.point.x,flight.point.y);
                ctx.strokeStyle=flight.color; ctx.fillStyle=flight.color;
                if(!flight.repeat && this.clock-flight.start>=flight.duration && flight.outcome==="impact") {
                    ctx.beginPath(); ctx.moveTo(p.x-4,p.y-4);ctx.lineTo(p.x+4,p.y+4);ctx.moveTo(p.x+4,p.y-4);ctx.lineTo(p.x-4,p.y+4);ctx.lineWidth=2;ctx.stroke();
                } else { ctx.beginPath();ctx.arc(p.x,p.y,4,0,TAU);ctx.fill(); }
            }
        }
    }

    // Public pure geometry helpers also make the preview independently testable.
    window.cannonV5 = {preview, sample, scene: null};
    function update(config, result) {
        const canvas=el("orbit-canvas");
        if(!canvas) return new Promise((resolve)=>setTimeout(()=>resolve(update(config,result)),25));
        if(!window.cannonV5.scene) window.cannonV5.scene=new CannonScene(canvas,config);
        window.cannonV5.scene.receive(result);
        return "ready";
    }
    window.dash_clientside=Object.assign({},window.dash_clientside,{cannonV5:{update}});
})();
