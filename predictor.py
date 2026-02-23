import { useState, useEffect, useRef } from "react";

const API_BASE = "http://localhost:8000/api";

// ── Palette & Styles ──────────────────────────────────────────────────────────
const palette = {
  bg: "#080D14",
  surface: "#0E1620",
  card: "#111C2A",
  border: "#1E2F45",
  accent: "#00D4FF",
  accent2: "#00FF88",
  accent3: "#FF6B35",
  warn: "#FFB830",
  danger: "#FF3B5C",
  text: "#E0EAF5",
  muted: "#5A7A96",
};

const MODULES = [
  { id: "space", label: "Space Utilization", icon: "🏛️", color: "#00D4FF" },
  { id: "footfall", label: "Footfall & Clogs", icon: "🚶", color: "#00FF88" },
  { id: "waste", label: "Waste / Biogas", icon: "♻️", color: "#FFB830" },
  { id: "water", label: "Water Quality", icon: "💧", color: "#5B9CF6" },
  { id: "greenery", label: "Greenery AI", icon: "🌿", color: "#4CAF50" },
  { id: "parking", label: "Parking", icon: "🚗", color: "#FF6B35" },
];

// ── Utility Components ────────────────────────────────────────────────────────

function StatusDot({ level }) {
  const colors = { ok: "#00FF88", warn: "#FFB830", crit: "#FF3B5C", muted: "#5A7A96" };
  return (
    <span style={{
      display: "inline-block", width: 8, height: 8, borderRadius: "50%",
      background: colors[level] || colors.muted,
      boxShadow: `0 0 6px ${colors[level] || colors.muted}`,
      marginRight: 6,
    }} />
  );
}

function OccupancyBar({ value, color = palette.accent }) {
  const pct = Math.min(100, Math.round(value * 100));
  const barColor = pct > 85 ? palette.danger : pct > 65 ? palette.warn : color;
  return (
    <div style={{ width: "100%", background: palette.border, borderRadius: 4, height: 8, overflow: "hidden" }}>
      <div style={{
        width: `${pct}%`, height: "100%", borderRadius: 4,
        background: barColor,
        boxShadow: `0 0 8px ${barColor}60`,
        transition: "width 0.5s ease",
      }} />
    </div>
  );
}

function MetricCard({ label, value, unit, icon, color = palette.accent, sub }) {
  return (
    <div style={{
      background: palette.card, border: `1px solid ${palette.border}`,
      borderRadius: 12, padding: "16px 20px",
      borderLeft: `3px solid ${color}`,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div style={{ color: palette.muted, fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
          <div style={{ color: palette.text, fontSize: 24, fontWeight: 700, marginTop: 4, fontFamily: "'DM Mono', monospace" }}>
            {value}<span style={{ fontSize: 13, color: palette.muted, marginLeft: 4 }}>{unit}</span>
          </div>
          {sub && <div style={{ color: palette.muted, fontSize: 11, marginTop: 4 }}>{sub}</div>}
        </div>
        <span style={{ fontSize: 24 }}>{icon}</span>
      </div>
    </div>
  );
}

function SectionHeader({ title, badge }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
      <h2 style={{ color: palette.text, fontSize: 15, fontWeight: 600, margin: 0, fontFamily: "'DM Mono', monospace" }}>{title}</h2>
      {badge && (
        <span style={{ background: `${palette.accent}22`, color: palette.accent, fontSize: 11, padding: "2px 8px", borderRadius: 20, border: `1px solid ${palette.accent}44` }}>
          {badge}
        </span>
      )}
    </div>
  );
}

// ── Chat Panel ────────────────────────────────────────────────────────────────

function ChatPanel() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I'm UrbanAI, your city & campus planning assistant. Ask me about space utilization, footfall patterns, water quality, waste management, or greenery recommendations.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  const QUICK_PROMPTS = [
    "Where are the clog points on campus?",
    "Predict parking availability this afternoon",
    "Recommend plants for Block A courtyard",
    "Is water quality OK in the hostels?",
  ];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg) return;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: msg }]);
    setLoading(true);

    // Simulate API call (replace with real fetch to /api/chat/stream)
    await new Promise(r => setTimeout(r, 1200 + Math.random() * 800));
    
    const responses = {
      "clog": "🚨 **3 clog points detected:**\n\n1. **Main Gate** (CRITICAL - 105% capacity) — Mixed pedestrian-vehicle conflict at peak hours 8-9 AM.\n2. **Cafeteria Junction** (HIGH - 88%) — Converging flows from 4 directions at lunch.\n3. **Hostel Road** (MEDIUM - 72%) — Delivery vehicles blocking pedestrian path.\n\n**Recommendations:** Install pedestrian skybridge at Main Gate, stagger lunch timings by 15 min, add bollards on Hostel Road.",
      "parking": "🚗 **Parking Forecast (Next 4 hrs):**\n\n- P1 Main Gate: 92% full → Will reach 100% by 2 PM ⛔\n- P2 Academic Block: 55% → Stable ✅\n- P3 Sports: 28% → Available ✅\n\n**Recommend:** Display P3 availability at main gate. EV zones can free up 40 slots in P1.",
      "plant": "🌿 **Top 3 Plants for Block A Courtyard:**\n\n1. **Neem** (Suitability: 94%) — Best for soil pH 7.2 detected. 22 kg CO₂/yr, natural shade.\n2. **Areca Palm** (87%) — NASA-rated air purifier, suits clay loam texture.\n3. **Bougainvillea** (81%) — Low water, covers walls, ornamental.\n\n**Soil amendment needed:** Add compost to raise organic matter from 1.2% → 3%.",
      "water": "💧 **Hostel Water Quality (Zone Z2):**\n\n- pH: 7.4 ✅\n- Turbidity: 5.2 NTU ⚠️ (Above 4.0 limit)\n- TDS: 680 ppm ❌ (Above 500 limit)\n- Chlorine: 0.38 ppm ✅\n\n**Risk Level: MEDIUM** | Quality Grade: C\n\n**Recommendations:**\n1. Install multimedia sand filter for turbidity\n2. Add RO system (120 LPM) for TDS reduction\n3. IoT auto-dosing for consistent chlorination",
    };

    let reply = "I've analyzed the campus data. Based on current sensor readings from our AMD Instinct MI300X-powered models, here's what I found:\n\nAll systems are operating within acceptable parameters. Space utilization is at 68% average across campus. Would you like detailed analysis for any specific area?";
    
    const lower = msg.toLowerCase();
    if (lower.includes("clog") || lower.includes("footfall")) reply = responses.clog;
    else if (lower.includes("park")) reply = responses.parking;
    else if (lower.includes("plant") || lower.includes("green")) reply = responses.plant;
    else if (lower.includes("water")) reply = responses.water;

    setMessages(prev => [...prev, { role: "assistant", content: reply }]);
    setLoading(false);
  };

  return (
    <div style={{
      display: "flex", flexDirection: "column", height: "100%",
      background: palette.card, borderRadius: 16, border: `1px solid ${palette.border}`,
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{
        padding: "14px 20px", borderBottom: `1px solid ${palette.border}`,
        display: "flex", alignItems: "center", gap: 10,
        background: `linear-gradient(135deg, ${palette.surface}, ${palette.card})`,
      }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8,
          background: `linear-gradient(135deg, ${palette.accent}, ${palette.accent2})`,
          display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
        }}>🏙️</div>
        <div>
          <div style={{ color: palette.text, fontWeight: 600, fontSize: 14 }}>UrbanAI Assistant</div>
          <div style={{ color: palette.accent2, fontSize: 11 }}>
            <StatusDot level="ok" />AMD MI300X · ROCm 7
          </div>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", display: "flex", flexDirection: "column", gap: 12 }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            display: "flex",
            justifyContent: m.role === "user" ? "flex-end" : "flex-start",
          }}>
            <div style={{
              maxWidth: "82%",
              background: m.role === "user"
                ? `linear-gradient(135deg, ${palette.accent}33, ${palette.accent}22)`
                : palette.surface,
              border: `1px solid ${m.role === "user" ? palette.accent + "44" : palette.border}`,
              borderRadius: m.role === "user" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
              padding: "10px 14px",
              color: palette.text,
              fontSize: 13,
              lineHeight: 1.6,
              whiteSpace: "pre-wrap",
            }}>
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: "flex", gap: 4, alignItems: "center", paddingLeft: 4 }}>
            {[0, 1, 2].map(i => (
              <div key={i} style={{
                width: 6, height: 6, borderRadius: "50%", background: palette.accent,
                animation: `bounce 1s ${i * 0.2}s infinite`,
              }} />
            ))}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick Prompts */}
      <div style={{ padding: "8px 16px", display: "flex", gap: 6, flexWrap: "wrap" }}>
        {QUICK_PROMPTS.map((p, i) => (
          <button key={i} onClick={() => sendMessage(p)} style={{
            background: `${palette.accent}15`, border: `1px solid ${palette.accent}33`,
            color: palette.accent, borderRadius: 20, padding: "4px 10px",
            fontSize: 11, cursor: "pointer", whiteSpace: "nowrap",
          }}>{p}</button>
        ))}
      </div>

      {/* Input */}
      <div style={{
        padding: "12px 16px", borderTop: `1px solid ${palette.border}`,
        display: "flex", gap: 8,
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Ask about any campus or city planning topic..."
          style={{
            flex: 1, background: palette.surface, border: `1px solid ${palette.border}`,
            borderRadius: 10, padding: "10px 14px", color: palette.text,
            fontSize: 13, outline: "none",
          }}
        />
        <button onClick={() => sendMessage()} style={{
          background: `linear-gradient(135deg, ${palette.accent}, ${palette.accent2})`,
          border: "none", borderRadius: 10, padding: "10px 16px",
          color: "#000", fontWeight: 700, cursor: "pointer", fontSize: 14,
        }}>→</button>
      </div>

      <style>{`
        @keyframes bounce {
          0%, 100% { transform: translateY(0); opacity: 0.4; }
          50% { transform: translateY(-6px); opacity: 1; }
        }
      `}</style>
    </div>
  );
}

// ── Space Utilization Panel ───────────────────────────────────────────────────

function SpacePanel() {
  const zones = [
    { name: "Block A — Classrooms", occ: 0.85, type: "classroom" },
    { name: "Research Labs (B-Wing)", occ: 0.45, type: "lab" },
    { name: "Central Library", occ: 0.72, type: "library" },
    { name: "Cafeteria", occ: 0.96, type: "cafeteria" },
    { name: "Sports Complex", occ: 0.31, type: "sports" },
    { name: "Admin Block", occ: 0.58, type: "admin" },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Space Utilization" badge="LIVE" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="Avg Occupancy" value="64" unit="%" icon="📊" color={palette.accent} sub="Across 24 zones" />
        <MetricCard label="At Capacity" value="3" unit="zones" icon="⚠️" color={palette.danger} sub="Needs immediate action" />
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {zones.map((z, i) => (
          <div key={i} style={{
            background: palette.surface, borderRadius: 10, padding: "12px 14px",
            border: `1px solid ${palette.border}`,
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span style={{ color: palette.text, fontSize: 13 }}>{z.name}</span>
              <span style={{
                color: z.occ > 0.85 ? palette.danger : z.occ > 0.65 ? palette.warn : palette.accent2,
                fontSize: 13, fontWeight: 600, fontFamily: "'DM Mono', monospace",
              }}>{Math.round(z.occ * 100)}%</span>
            </div>
            <OccupancyBar value={z.occ} />
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Footfall Panel ────────────────────────────────────────────────────────────

function FootfallPanel() {
  const clogs = [
    { name: "Main Gate", severity: "CRITICAL", util: 1.05, conflict: "Pedestrian-vehicle" },
    { name: "Cafeteria Junction", severity: "HIGH", util: 0.88, conflict: "Converging flow" },
    { name: "Hostel Road", severity: "MEDIUM", util: 0.72, conflict: "Delivery blocking" },
  ];

  const sevColor = { CRITICAL: palette.danger, HIGH: palette.warn, MEDIUM: "#FFB830" };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Footfall & Clog Points" badge="AI DETECTED" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="Active Clogs" value="3" unit="" icon="🚨" color={palette.danger} sub="2 with vehicle conflict" />
        <MetricCard label="Peak Flow" value="847" unit="pph" icon="🚶" color={palette.accent2} sub="Main Gate (current)" />
      </div>
      {clogs.map((c, i) => (
        <div key={i} style={{
          background: palette.surface, border: `1px solid ${sevColor[c.severity]}44`,
          borderLeft: `3px solid ${sevColor[c.severity]}`,
          borderRadius: 10, padding: "12px 14px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <span style={{ color: palette.text, fontSize: 13, fontWeight: 600 }}>{c.name}</span>
              <div style={{ color: palette.muted, fontSize: 11, marginTop: 2 }}>{c.conflict}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{
                background: `${sevColor[c.severity]}22`, color: sevColor[c.severity],
                fontSize: 10, padding: "2px 8px", borderRadius: 10, display: "block",
              }}>{c.severity}</span>
              <span style={{ color: sevColor[c.severity], fontSize: 13, fontFamily: "'DM Mono', monospace", fontWeight: 700 }}>
                {Math.round(c.util * 100)}%
              </span>
            </div>
          </div>
          <OccupancyBar value={c.util} color={sevColor[c.severity]} />
        </div>
      ))}
      <div style={{ background: `${palette.accent2}11`, border: `1px solid ${palette.accent2}33`, borderRadius: 10, padding: 12 }}>
        <div style={{ color: palette.accent2, fontSize: 12, fontWeight: 600, marginBottom: 6 }}>💡 AI Recommendation</div>
        <div style={{ color: palette.text, fontSize: 12, lineHeight: 1.6 }}>
          Stagger class timings by 15 min to reduce Main Gate load by ~35%. Install pedestrian skywalk — projected ROI: 18 months.
        </div>
      </div>
    </div>
  );
}

// ── Water Panel ───────────────────────────────────────────────────────────────

function WaterPanel() {
  const zones = [
    { id: "Z1", name: "Academic Block", score: 94, grade: "A", status: "ok" },
    { id: "Z2", name: "Hostels", score: 68, grade: "C", status: "warn", issue: "High TDS (680 ppm)" },
    { id: "Z3", name: "Sports Complex", score: 88, grade: "B", status: "ok" },
    { id: "Z4", name: "Irrigation Network", score: 41, grade: "D", status: "crit", issue: "High turbidity + TDS" },
    { id: "Z5", name: "Greywater Loop", score: 55, grade: "C", status: "warn" },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Water Quality Monitor" badge="SENSOR LIVE" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="Zones OK" value="3" unit="/5" icon="✅" color={palette.accent2} />
        <MetricCard label="Anomalies" value="7" unit="params" icon="⚗️" color={palette.warn} sub="Across 2 zones" />
      </div>
      {zones.map((z, i) => (
        <div key={i} style={{
          background: palette.surface, borderRadius: 10, padding: "12px 14px",
          border: `1px solid ${z.status === "crit" ? palette.danger + "44" : z.status === "warn" ? palette.warn + "44" : palette.border}`,
          display: "flex", alignItems: "center", justifyContent: "space-between",
        }}>
          <div>
            <div style={{ display: "flex", alignItems: "center" }}>
              <StatusDot level={z.status} />
              <span style={{ color: palette.text, fontSize: 13 }}>{z.name}</span>
              <span style={{ color: palette.muted, fontSize: 11, marginLeft: 8 }}>({z.id})</span>
            </div>
            {z.issue && <div style={{ color: palette.warn, fontSize: 11, marginTop: 2, paddingLeft: 14 }}>{z.issue}</div>}
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{
              color: z.score > 80 ? palette.accent2 : z.score > 60 ? palette.warn : palette.danger,
              fontSize: 18, fontWeight: 700, fontFamily: "'DM Mono', monospace",
            }}>{z.score}</div>
            <div style={{ color: palette.muted, fontSize: 11 }}>Grade {z.grade}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Greenery Panel ────────────────────────────────────────────────────────────

function GreeneryPanel() {
  const plants = [
    { name: "Neem", score: 0.94, co2: 22, water: "Low", type: "Tree" },
    { name: "Areca Palm", score: 0.87, co2: 6, water: "Medium", type: "Palm" },
    { name: "Bougainvillea", score: 0.81, co2: 5, water: "Very Low", type: "Climber" },
    { name: "Bamboo", score: 0.76, co2: 35, water: "Medium", type: "Screen" },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Greenery AI Recommender" badge="SOIL ANALYZED" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="CO₂ Offset" value="62" unit="kg/yr" icon="🌳" color={palette.accent2} sub="Per 100 sq m planted" />
        <MetricCard label="Soil Quality" value="Good" unit="" icon="🌱" color="#4CAF50" sub="pH 7.2 · Loam texture" />
      </div>
      {plants.map((p, i) => (
        <div key={i} style={{
          background: palette.surface, borderRadius: 10, padding: "12px 14px",
          border: `1px solid ${palette.border}`,
          borderLeft: i === 0 ? `3px solid #4CAF50` : `1px solid ${palette.border}`,
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <div>
              <span style={{ color: palette.text, fontSize: 13, fontWeight: i === 0 ? 600 : 400 }}>{p.name}</span>
              <span style={{ color: palette.muted, fontSize: 11, marginLeft: 8 }}>{p.type}</span>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{ color: "#4CAF50", fontFamily: "'DM Mono', monospace", fontSize: 13, fontWeight: 700 }}>
                {Math.round(p.score * 100)}%
              </span>
            </div>
          </div>
          <OccupancyBar value={p.score} color="#4CAF50" />
          <div style={{ display: "flex", gap: 12, marginTop: 6 }}>
            <span style={{ color: palette.muted, fontSize: 11 }}>🌬️ {p.co2} kg CO₂/yr</span>
            <span style={{ color: palette.muted, fontSize: 11 }}>💧 {p.water} water</span>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Parking Panel ─────────────────────────────────────────────────────────────

function ParkingPanel() {
  const lots = [
    { id: "P1", name: "Main Gate", capacity: 500, available: 42, status: "BUSY" },
    { id: "P2", name: "Academic Block", capacity: 300, available: 138, status: "AVAILABLE" },
    { id: "P3", name: "Sports Complex", capacity: 200, available: 145, status: "AVAILABLE" },
    { id: "P4", name: "Staff Quarters", capacity: 150, available: 3, status: "FULL" },
  ];

  const statusColor = { FULL: palette.danger, BUSY: palette.warn, AVAILABLE: palette.accent2 };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Parking Management" badge="REAL-TIME" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="Total Available" value="328" unit="slots" icon="🅿️" color={palette.accent} />
        <MetricCard label="Lots Full" value="1" unit="/4" icon="🚫" color={palette.danger} />
      </div>
      {lots.map((lot, i) => {
        const occ = 1 - (lot.available / lot.capacity);
        return (
          <div key={i} style={{
            background: palette.surface, borderRadius: 10, padding: "12px 14px",
            border: `1px solid ${statusColor[lot.status]}44`,
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <div>
                <span style={{ color: palette.text, fontSize: 13 }}>{lot.id} — {lot.name}</span>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ color: palette.text, fontFamily: "'DM Mono', monospace", fontSize: 13 }}>
                  {lot.available}<span style={{ color: palette.muted }}>/{lot.capacity}</span>
                </span>
                <span style={{
                  background: `${statusColor[lot.status]}22`, color: statusColor[lot.status],
                  fontSize: 10, padding: "2px 8px", borderRadius: 10,
                }}>{lot.status}</span>
              </div>
            </div>
            <OccupancyBar value={occ} color={statusColor[lot.status]} />
          </div>
        );
      })}
    </div>
  );
}

// ── Waste Panel ───────────────────────────────────────────────────────────────

function WastePanel() {
  const forecast = [
    { day: "Mon", total: 580, bio: 394, biogas: 157 },
    { day: "Tue", total: 612, bio: 416, biogas: 166 },
    { day: "Wed", total: 598, bio: 407, biogas: 163 },
    { day: "Thu", total: 543, bio: 369, biogas: 148 },
    { day: "Fri", total: 624, bio: 424, biogas: 170 },
    { day: "Sat", total: 352, bio: 239, biogas: 96 },
    { day: "Sun", total: 298, bio: 203, biogas: 81 },
  ];
  const maxVal = Math.max(...forecast.map(f => f.total));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <SectionHeader title="Waste & Biogas Forecast" badge="7-DAY" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <MetricCard label="Weekly Biogas" value="981" unit="m³" icon="⚡" color={palette.warn} sub="≈ 5,396 kWh recoverable" />
        <MetricCard label="CO₂ Offset" value="1.86" unit="tonnes" icon="🌍" color={palette.accent2} sub="This week" />
      </div>
      
      {/* Bar chart */}
      <div style={{ background: palette.surface, borderRadius: 10, padding: "14px", border: `1px solid ${palette.border}` }}>
        <div style={{ color: palette.muted, fontSize: 11, marginBottom: 10 }}>Daily waste forecast (kg)</div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 6, height: 80 }}>
          {forecast.map((f, i) => (
            <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
              <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: 1, height: 70, justifyContent: "flex-end" }}>
                <div style={{
                  width: "100%", borderRadius: "3px 3px 0 0",
                  height: `${(f.bio / maxVal) * 70}px`,
                  background: palette.warn,
                  opacity: 0.8,
                }} title={`Biodegradable: ${f.bio}kg`} />
                <div style={{
                  width: "100%",
                  height: `${((f.total - f.bio) / maxVal) * 70}px`,
                  background: palette.muted,
                  opacity: 0.4,
                }} title={`Other: ${f.total - f.bio}kg`} />
              </div>
              <span style={{ color: palette.muted, fontSize: 10 }}>{f.day}</span>
            </div>
          ))}
        </div>
        <div style={{ display: "flex", gap: 16, marginTop: 8 }}>
          <span style={{ color: palette.muted, fontSize: 10 }}>
            <span style={{ display: "inline-block", width: 8, height: 8, background: palette.warn, borderRadius: 2, marginRight: 4 }} />
            Biodegradable
          </span>
          <span style={{ color: palette.muted, fontSize: 10 }}>
            <span style={{ display: "inline-block", width: 8, height: 8, background: palette.muted, opacity: 0.4, borderRadius: 2, marginRight: 4 }} />
            Other
          </span>
        </div>
      </div>
    </div>
  );
}

// ── Main App ──────────────────────────────────────────────────────────────────

export default function App() {
  const [activeModule, setActiveModule] = useState("space");
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const panels = {
    space: <SpacePanel />,
    footfall: <FootfallPanel />,
    waste: <WastePanel />,
    water: <WaterPanel />,
    greenery: <GreeneryPanel />,
    parking: <ParkingPanel />,
  };

  return (
    <div style={{
      minHeight: "100vh", background: palette.bg, color: palette.text,
      fontFamily: "'DM Sans', 'Segoe UI', sans-serif",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;600;700&family=DM+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1E2F45; border-radius: 4px; }
        input::placeholder { color: #5A7A96; }
      `}</style>

      {/* Top Bar */}
      <div style={{
        background: palette.surface, borderBottom: `1px solid ${palette.border}`,
        padding: "0 24px", display: "flex", alignItems: "center",
        justifyContent: "space-between", height: 56,
        position: "sticky", top: 0, zIndex: 100,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: `linear-gradient(135deg, ${palette.accent}, ${palette.accent2})`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 16,
          }}>🏙️</div>
          <div>
            <span style={{ fontWeight: 700, fontSize: 15, letterSpacing: "-0.5px" }}>Urban</span>
            <span style={{ fontWeight: 700, fontSize: 15, color: palette.accent }}>AI</span>
            <span style={{ color: palette.muted, fontSize: 12, marginLeft: 12 }}>City & Campus Planning Platform</span>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ display: "flex", gap: 16 }}>
            {[
              { label: "AMD MI300X", color: palette.accent2, dot: "ok" },
              { label: "ROCm 7", color: palette.accent, dot: "ok" },
              { label: "Sensors: 47", color: palette.warn, dot: "ok" },
            ].map((s, i) => (
              <span key={i} style={{ fontSize: 11, color: s.color }}>
                <StatusDot level={s.dot} />{s.label}
              </span>
            ))}
          </div>
          <span style={{ color: palette.muted, fontSize: 12, fontFamily: "'DM Mono', monospace" }}>
            {time.toLocaleTimeString()}
          </span>
        </div>
      </div>

      <div style={{ display: "flex", height: "calc(100vh - 56px)" }}>
        {/* Left Sidebar — Module Nav */}
        <div style={{
          width: 64, background: palette.surface, borderRight: `1px solid ${palette.border}`,
          display: "flex", flexDirection: "column", alignItems: "center",
          paddingTop: 16, gap: 4,
        }}>
          {MODULES.map(m => (
            <button key={m.id} onClick={() => setActiveModule(m.id)} title={m.label}
              style={{
                width: 44, height: 44, borderRadius: 10, border: "none",
                background: activeModule === m.id ? `${m.color}22` : "transparent",
                cursor: "pointer", fontSize: 20,
                outline: activeModule === m.id ? `1px solid ${m.color}66` : "none",
                transition: "all 0.15s",
              }}>
              {m.icon}
            </button>
          ))}
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, display: "flex", gap: 0, overflow: "hidden" }}>
          {/* Analytics Panel */}
          <div style={{
            width: 380, borderRight: `1px solid ${palette.border}`,
            overflow: "auto", padding: "20px 16px",
            background: palette.surface,
          }}>
            {panels[activeModule]}
          </div>

          {/* Map Placeholder */}
          <div style={{ flex: 1, position: "relative", overflow: "hidden", background: "#060B11" }}>
            {/* Grid pattern background */}
            <div style={{
              position: "absolute", inset: 0,
              backgroundImage: `
                linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px)
              `,
              backgroundSize: "40px 40px",
            }} />
            
            {/* Campus map mockup */}
            <div style={{
              position: "absolute", inset: 0, display: "flex",
              alignItems: "center", justifyContent: "center",
              flexDirection: "column", gap: 16,
            }}>
              <div style={{ position: "relative", width: 500, height: 380 }}>
                {/* Campus buildings */}
                {[
                  { label: "Block A", x: 160, y: 80, w: 100, h: 70, occ: 0.85, color: palette.accent },
                  { label: "Labs B", x: 290, y: 80, w: 80, h: 60, occ: 0.45, color: palette.accent2 },
                  { label: "Library", x: 360, y: 170, w: 90, h: 60, occ: 0.72, color: palette.accent },
                  { label: "Cafeteria", x: 210, y: 180, w: 80, h: 60, occ: 0.96, color: palette.danger },
                  { label: "Sports", x: 80, y: 220, w: 110, h: 80, occ: 0.31, color: palette.accent2 },
                  { label: "Admin", x: 310, y: 270, w: 100, h: 60, occ: 0.58, color: palette.warn },
                ].map((b, i) => (
                  <div key={i} style={{
                    position: "absolute", left: b.x, top: b.y,
                    width: b.w, height: b.h,
                    background: `${b.color}${Math.round(b.occ * 30 + 8).toString(16).padStart(2,"0")}`,
                    border: `1px solid ${b.color}66`,
                    borderRadius: 6,
                    display: "flex", flexDirection: "column",
                    alignItems: "center", justifyContent: "center",
                    cursor: "pointer",
                    transition: "all 0.2s",
                  }}>
                    <div style={{ color: b.color, fontSize: 11, fontWeight: 600 }}>{b.label}</div>
                    <div style={{ color: palette.text, fontSize: 13, fontFamily: "'DM Mono', monospace", fontWeight: 700 }}>
                      {Math.round(b.occ * 100)}%
                    </div>
                    {b.occ > 0.85 && (
                      <div style={{
                        position: "absolute", top: -6, right: -6,
                        width: 14, height: 14, borderRadius: "50%",
                        background: palette.danger,
                        boxShadow: `0 0 8px ${palette.danger}`,
                        animation: "pulse 1.5s infinite",
                      }} />
                    )}
                  </div>
                ))}
                
                {/* Clog indicators */}
                {[
                  { x: 130, y: 155, label: "CLOG", severity: "crit" },
                  { x: 245, y: 240, label: "CLOG", severity: "warn" },
                ].map((c, i) => (
                  <div key={i} style={{
                    position: "absolute", left: c.x, top: c.y,
                    background: c.severity === "crit" ? `${palette.danger}22` : `${palette.warn}22`,
                    border: `1px solid ${c.severity === "crit" ? palette.danger : palette.warn}`,
                    borderRadius: 20, padding: "2px 8px",
                    color: c.severity === "crit" ? palette.danger : palette.warn,
                    fontSize: 10, fontWeight: 700,
                    animation: "pulse 2s infinite",
                  }}>⚠ {c.label}</div>
                ))}
              </div>
              
              <div style={{ color: palette.muted, fontSize: 12 }}>
                Interactive GIS map — connect Leaflet.js / MapboxGL for full geospatial view
              </div>
            </div>

            {/* Overlay legend */}
            <div style={{
              position: "absolute", bottom: 20, right: 20,
              background: `${palette.card}ee`, border: `1px solid ${palette.border}`,
              borderRadius: 10, padding: "12px 16px",
            }}>
              <div style={{ color: palette.muted, fontSize: 11, marginBottom: 8 }}>Map Layer</div>
              {[
                { label: "Occupancy Heatmap", color: palette.accent },
                { label: "Clog Points", color: palette.danger },
                { label: "Water Zones", color: "#5B9CF6" },
                { label: "Greenery Coverage", color: "#4CAF50" },
              ].map((l, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <div style={{ width: 10, height: 10, borderRadius: 3, background: l.color }} />
                  <span style={{ color: palette.text, fontSize: 11 }}>{l.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Chat Sidebar */}
          <div style={{ width: 380, borderLeft: `1px solid ${palette.border}`, padding: 16 }}>
            <ChatPanel />
          </div>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
}
