import { useState, useEffect } from "react";

const INTENT_COLORS = {
  meeting_request: { bg: "bg-green-100", text: "text-green-800", dot: "bg-green-500" },
  pricing_question: { bg: "bg-blue-100", text: "text-blue-800", dot: "bg-blue-500" },
  objection: { bg: "bg-red-100", text: "text-red-800", dot: "bg-red-500" },
  positive_interest: { bg: "bg-emerald-100", text: "text-emerald-800", dot: "bg-emerald-500" },
  unsubscribe: { bg: "bg-gray-100", text: "text-gray-600", dot: "bg-gray-400" },
  out_of_office: { bg: "bg-yellow-100", text: "text-yellow-800", dot: "bg-yellow-500" },
  unknown: { bg: "bg-purple-100", text: "text-purple-800", dot: "bg-purple-500" },
};

const SAMPLE_LEADS = [
  { id: 1, name: "Sarah Johnson", company: "Acme Logistics", intent: "meeting_request", sentiment: "positive", urgency: "high", action: "schedule_meeting", time: "2 min ago", reply: "Hi Sarah, I'd love to show you what we've built! Here's my calendar to grab a 30-min slot: [CALENDLY_LINK]. Looking forward to connecting!" },
  { id: 2, name: "James Park", company: "TechFlow", intent: "pricing_question", sentiment: "neutral", urgency: "medium", action: "send_info", time: "15 min ago", reply: "Hi James, great question! I'll send over our pricing overview shortly. Would a quick call help tailor a plan for TechFlow?" },
  { id: 3, name: "Maria Santos", company: "SwiftDeliver", intent: "objection", sentiment: "negative", urgency: "medium", action: "handle_objection", time: "1 hr ago", reply: "Hi Maria, totally understand — budget is always a consideration. Many teams like yours saw ROI within the first month. Worth a 15-min chat?" },
  { id: 4, name: "Tom Wright", company: "LogiCore", intent: "positive_interest", sentiment: "positive", urgency: "low", action: "nurture", time: "3 hr ago", reply: "Hi Tom, glad it resonates! We've helped logistics teams cut costs by up to 30%. Want to see it in action?" },
  { id: 5, name: "Amy Chen", company: "FastFreight", intent: "unsubscribe", sentiment: "negative", urgency: "low", action: "stop", time: "5 hr ago", reply: null },
  { id: 6, name: "Daniel Reeves", company: "SupplyPro", intent: "out_of_office", sentiment: "neutral", urgency: "low", action: "schedule_followup", time: "1 day ago", reply: "Hi Daniel, no worries at all! I'll check back in when you're back. Hope you enjoy the time off!" },
];

function Badge({ intent }) {
  const c = INTENT_COLORS[intent] || INTENT_COLORS.unknown;
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${c.bg} ${c.text}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${c.dot}`} />
      {intent.replace(/_/g, " ")}
    </span>
  );
}

function UrgencyDot({ urgency }) {
  const map = { high: "bg-red-500", medium: "bg-yellow-400", low: "bg-green-400" };
  return <span className={`inline-block w-2 h-2 rounded-full ${map[urgency] || "bg-gray-300"}`} title={urgency} />;
}

function StatCard({ label, value, sub, color }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex flex-col gap-1">
      <p className="text-sm text-gray-500">{label}</p>
      <p className={`text-3xl font-bold ${color || "text-gray-900"}`}>{value}</p>
      {sub && <p className="text-xs text-gray-400">{sub}</p>}
    </div>
  );
}

function LeadRow({ lead, onSelect, selected }) {
  return (
    <tr
      onClick={() => onSelect(lead)}
      className={`cursor-pointer transition-colors ${selected ? "bg-indigo-50" : "hover:bg-gray-50"}`}
    >
      <td className="px-4 py-3">
        <div className="font-medium text-gray-900 text-sm">{lead.name}</div>
        <div className="text-xs text-gray-400">{lead.company}</div>
      </td>
      <td className="px-4 py-3"><Badge intent={lead.intent} /></td>
      <td className="px-4 py-3">
        <span className={`text-xs font-medium ${lead.sentiment === "positive" ? "text-green-600" : lead.sentiment === "negative" ? "text-red-500" : "text-gray-500"}`}>
          {lead.sentiment}
        </span>
      </td>
      <td className="px-4 py-3"><UrgencyDot urgency={lead.urgency} /></td>
      <td className="px-4 py-3">
        <span className={`text-xs px-2 py-1 rounded-md font-mono ${lead.action === "stop" ? "bg-red-50 text-red-600" : "bg-gray-100 text-gray-700"}`}>
          {lead.action}
        </span>
      </td>
      <td className="px-4 py-3 text-xs text-gray-400">{lead.time}</td>
    </tr>
  );
}

function Sidebar({ lead, onClose }) {
  if (!lead) return null;
  return (
    <div className="w-80 flex-shrink-0 bg-white border-l border-gray-100 flex flex-col">
      <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Lead Detail</h3>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg leading-none">✕</button>
      </div>
      <div className="p-5 flex flex-col gap-4 overflow-y-auto">
        <div>
          <p className="text-lg font-bold text-gray-900">{lead.name}</p>
          <p className="text-sm text-gray-500">{lead.company}</p>
        </div>
        <div className="flex flex-col gap-2 text-sm">
          <div className="flex justify-between"><span className="text-gray-500">Intent</span><Badge intent={lead.intent} /></div>
          <div className="flex justify-between"><span className="text-gray-500">Sentiment</span><span className="font-medium">{lead.sentiment}</span></div>
          <div className="flex justify-between items-center"><span className="text-gray-500">Urgency</span><span className="flex items-center gap-1.5"><UrgencyDot urgency={lead.urgency} />{lead.urgency}</span></div>
          <div className="flex justify-between"><span className="text-gray-500">Action</span><span className="font-mono text-xs bg-gray-100 px-2 py-0.5 rounded">{lead.action}</span></div>
          <div className="flex justify-between"><span className="text-gray-500">Time</span><span>{lead.time}</span></div>
        </div>
        {lead.reply ? (
          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Auto-generated Reply</p>
            <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-3 text-sm text-gray-800 leading-relaxed">
              {lead.reply}
            </div>
          </div>
        ) : (
          <div className="bg-red-50 border border-red-100 rounded-xl p-3 text-sm text-red-600">
            No reply sent — lead unsubscribed.
          </div>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [leads] = useState(SAMPLE_LEADS);
  const [selected, setSelected] = useState(null);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  const intents = ["all", ...Object.keys(INTENT_COLORS)];

  const filtered = leads.filter(l => {
    const matchIntent = filter === "all" || l.intent === filter;
    const matchSearch = l.name.toLowerCase().includes(search.toLowerCase()) ||
      l.company.toLowerCase().includes(search.toLowerCase());
    return matchIntent && matchSearch;
  });

  const stats = {
    total: leads.length,
    highUrgency: leads.filter(l => l.urgency === "high").length,
    meetings: leads.filter(l => l.intent === "meeting_request").length,
    unsubscribed: leads.filter(l => l.intent === "unsubscribe").length,
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">L</div>
          <span className="font-bold text-gray-900 text-lg">LeadMind</span>
          <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-medium">Dashboard</span>
        </div>
        <div className="text-xs text-gray-400">Powered by Claude AI</div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6 flex flex-col gap-6">
        {/* Stats */}
        <div className="grid grid-cols-4 gap-4">
          <StatCard label="Total Leads" value={stats.total} sub="last 24 hours" />
          <StatCard label="High Urgency" value={stats.highUrgency} sub="need attention" color="text-red-500" />
          <StatCard label="Meeting Requests" value={stats.meetings} sub="ready to book" color="text-green-600" />
          <StatCard label="Unsubscribed" value={stats.unsubscribed} sub="removed from pipeline" color="text-gray-400" />
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm flex overflow-hidden">
          <div className="flex-1 flex flex-col min-w-0">
            {/* Filters */}
            <div className="px-5 py-4 border-b border-gray-100 flex items-center gap-3 flex-wrap">
              <input
                type="text"
                placeholder="Search leads..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-300 w-48"
              />
              <div className="flex gap-1.5 flex-wrap">
                {intents.map(i => (
                  <button
                    key={i}
                    onClick={() => setFilter(i)}
                    className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${filter === i ? "bg-indigo-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}
                  >
                    {i === "all" ? "All" : i.replace(/_/g, " ")}
                  </button>
                ))}
              </div>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-xs text-gray-400 uppercase tracking-wider border-b border-gray-100">
                    <th className="text-left px-4 py-3 font-medium">Lead</th>
                    <th className="text-left px-4 py-3 font-medium">Intent</th>
                    <th className="text-left px-4 py-3 font-medium">Sentiment</th>
                    <th className="text-left px-4 py-3 font-medium">Urgency</th>
                    <th className="text-left px-4 py-3 font-medium">Action</th>
                    <th className="text-left px-4 py-3 font-medium">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {filtered.length ? filtered.map(lead => (
                    <LeadRow
                      key={lead.id}
                      lead={lead}
                      onSelect={setSelected}
                      selected={selected?.id === lead.id}
                    />
                  )) : (
                    <tr><td colSpan={6} className="text-center py-10 text-gray-400 text-sm">No leads match your filter.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Sidebar */}
          <Sidebar lead={selected} onClose={() => setSelected(null)} />
        </div>
      </main>
    </div>
  );
}
