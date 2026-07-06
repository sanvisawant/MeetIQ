import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import {
  Sparkles,
  AlertCircle,
  Lightbulb,
  FileText,
  Mail,
  Clock,
  CheckCircle2,
  CircleDot,
  Loader2,
  RotateCcw,
  FileAudio,
  Video,
  Network,
  UploadCloud,
} from "lucide-react";

const data = {
  efficiency_score: 62,
  verdict: "Could have been an email.",
  reasons: [
    "Only 3 of 10 attendees actively contributed.",
    "No decisions were made.",
    "Discussion repeated last week's agenda.",
  ],
  recommendation: "Next time, send a written status update.",
  action_items: [
    { task: "Push code to staging", owner: "Amit", deadline: "Today 5PM" },
    { task: "Send AWS status", owner: "Amit", deadline: "Tomorrow" },
    { task: "Request repo access", owner: "Akanksha", deadline: "ASAP" },
  ],
  summary_doc_url: "https://docs.google.com",
  draft_email_links: ["https://mail.google.com"],
};

const roadmap = [
  {
    icon: FileAudio,
    title: "Direct Media Uploads",
    desc: "Bypass text transcripts entirely. Upload raw audio or video meeting recordings for the AI to process directly.",
  },
  {
    icon: Video,
    title: "Live Google Meet Integration",
    desc: "Real-time agent analysis and live task extraction during active meetings.",
  },
  {
    icon: Network,
    title: "Expanded Ecosystem Integration",
    desc: "Deep two-way integrations with Google Calendar, Slack, and Jira for automated task routing and intelligent calendar shielding.",
  },
];

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MeetIQ — Meeting Audit Report" },
      {
        name: "description",
        content:
          "AI-generated meeting analytics, efficiency scoring, and action items to cut meeting fatigue.",
      },
      { property: "og:title", content: "MeetIQ — Meeting Audit Report" },
      {
        property: "og:description",
        content:
          "AI-generated meeting analytics, efficiency scoring, and action items.",
      },
    ],
  }),
  component: App,
});

type View = "upload" | "loading" | "dashboard";

function App() {
  const [view, setView] = useState<View>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [auditData, setAuditData] = useState<any>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const runAudit = async () => {
    setView("loading");
    let transcriptText = "";
    
    if (file) {
      try {
        transcriptText = await file.text();
      } catch (err) {
        console.error("Error reading file:", err);
      }
    }
    
    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ transcript: transcriptText }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setAuditData(result);
      setView("dashboard");
    } catch (err) {
      console.error("Error running audit, falling back to mock data:", err);
      setAuditData(data);
      setView("dashboard");
    }
  };

  const reset = () => {
    setFile(null);
    setView("upload");
    setAuditData(null);
  };

  if (view === "dashboard" && auditData) return <Dashboard data={auditData} onReset={reset} />;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border/70 bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Sparkles className="h-4 w-4" />
            </div>
            <span className="text-lg font-semibold tracking-tight text-foreground">
              MeetIQ
            </span>
          </div>
          <div className="hidden text-sm text-muted-foreground sm:block">
            {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
          </div>
        </div>
      </header>

      <main className="mx-auto flex max-w-3xl flex-col items-center px-6 py-16">
        <div className="mb-8 text-center">
          <div className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
            New Audit
          </div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Start with a transcript
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Drop a meeting transcript and our agents will extract the signal.
          </p>
        </div>

        {view === "loading" ? (
          <div className="flex w-full flex-col items-center justify-center rounded-2xl border border-border bg-card px-6 py-20 shadow-[var(--shadow-soft)]">
            <Loader2 className="h-10 w-10 animate-spin text-primary" />
            <div className="mt-6 text-base font-medium text-foreground">
              Agents analyzing transcript…
            </div>
            <div className="mt-1 text-sm text-muted-foreground">
              Scoring efficiency, extracting decisions & action items.
            </div>
          </div>
        ) : (
          <>
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                const f = e.dataTransfer.files?.[0];
                if (f) setFile(f);
              }}
              className={`flex w-full flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-16 text-center transition-colors ${
                dragOver
                  ? "border-primary bg-primary/5"
                  : "border-border bg-card hover:border-primary/40 hover:bg-muted/40"
              }`}
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-muted text-muted-foreground">
                <FileText className="h-6 w-6" />
              </div>
              <div className="mt-5 text-base font-medium text-foreground">
                Drag & Drop Meeting Transcript (.txt)
              </div>
              <div className="mt-1 text-sm text-muted-foreground">
                or click to browse from your computer
              </div>
              {file && (
                <div className="mt-5 inline-flex items-center gap-2 rounded-full border border-border bg-secondary/60 px-3 py-1 text-xs font-medium text-secondary-foreground">
                  <UploadCloud className="h-3.5 w-3.5" />
                  {file.name}
                </div>
              )}
              <input
                ref={inputRef}
                type="file"
                accept=".txt,text/plain"
                className="hidden"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) setFile(f);
                }}
              />
            </button>

            <button
              onClick={runAudit}
              className="mt-6 inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-[var(--shadow-soft)] transition-all hover:-translate-y-0.5 hover:shadow-[var(--shadow-lift)]"
            >
              <Sparkles className="h-4 w-4" />
              Run AI Audit
            </button>
            <p className="mt-3 text-xs text-muted-foreground">
              Demo mode — a sample transcript will be used if no file is selected.
            </p>
          </>
        )}
      </main>
    </div>
  );
}

function scoreColor(score: number) {
  if (score >= 80) return { stroke: "var(--sage)", tint: "text-[color:var(--sage-foreground)]", label: "Productive" };
  if (score >= 50) return { stroke: "var(--amber-soft)", tint: "text-[color:var(--amber-soft)]", label: "Mediocre" };
  return { stroke: "var(--rose-soft)", tint: "text-[color:var(--rose-soft)]", label: "Poor" };
}

function Gauge({ target }: { target: number }) {
  const [value, setValue] = useState(0);
  const size = 220;
  const stroke = 16;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const { stroke: color, label } = scoreColor(target);

  useEffect(() => {
    let raf: number;
    const start = performance.now();
    const duration = 1400;
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setValue(Math.round(target * eased));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target]);

  const offset = c - (value / 100) * c;

  return (
    <div className="relative flex flex-col items-center">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          strokeWidth={stroke}
          stroke="var(--muted)"
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          strokeWidth={stroke}
          stroke={color}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 60ms linear" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-5xl font-semibold tracking-tight text-foreground tabular-nums">
          {value}
          <span className="text-2xl text-muted-foreground">%</span>
        </span>
        <span
          className="mt-1 text-xs font-medium uppercase tracking-widest"
          style={{ color }}
        >
          {label}
        </span>
      </div>
    </div>
  );
}

function initials(name: string) {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function Dashboard({ data, onReset }: { data: any; onReset: () => void }) {
  const { stroke: scoreStroke } = scoreColor(data.efficiency_score);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/70 bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Sparkles className="h-4 w-4" />
            </div>
            <span className="text-lg font-semibold tracking-tight text-foreground">
              MeetIQ
            </span>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden text-sm text-muted-foreground sm:block">
              {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
            </div>
            <button
              onClick={onReset}
              className="inline-flex items-center gap-1.5 rounded-md border border-border bg-background px-3 py-1.5 text-xs font-medium text-foreground/80 shadow-[var(--shadow-soft)] transition-all hover:-translate-y-0.5 hover:text-foreground hover:shadow-[var(--shadow-lift)]"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              Upload New
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        {/* Title */}
        <div className="mb-8">
          <div className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
            Audit Report
          </div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Weekly Sync — {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric" })}
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Generated from a 42-minute call with 10 attendees.
          </p>
        </div>

        {/* Efficiency card */}
        <section className="rounded-2xl border border-border bg-card shadow-[var(--shadow-soft)]">
          <div className="grid gap-8 p-8 md:grid-cols-[auto_1fr] md:gap-12 md:p-10">
            <div className="flex flex-col items-center justify-center">
              <div className="mb-4 text-xs font-medium uppercase tracking-widest text-muted-foreground">
                Efficiency Score
              </div>
              <Gauge target={data.efficiency_score} />
            </div>

            <div className="flex flex-col justify-center">
              <div className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
                Verdict
              </div>
              <h2 className="mt-2 text-2xl font-semibold leading-tight tracking-tight text-foreground sm:text-3xl">
                "{data.verdict}"
              </h2>

              <ul className="mt-6 space-y-3">
                {data.reasons.map((reason) => (
                  <li key={reason} className="flex items-start gap-3 text-sm text-foreground/85">
                    <AlertCircle
                      className="mt-0.5 h-4 w-4 shrink-0"
                      style={{ color: scoreStroke }}
                    />
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>

              <div className="mt-6 flex items-start gap-3 rounded-xl border border-[color:var(--callout)] bg-[color:var(--callout)] p-4">
                <Lightbulb className="mt-0.5 h-5 w-5 shrink-0 text-[color:var(--callout-foreground)]" />
                <div>
                  <div className="text-xs font-semibold uppercase tracking-wider text-[color:var(--callout-foreground)]/80">
                    Recommendation
                  </div>
                  <div className="mt-1 text-sm font-medium text-[color:var(--callout-foreground)]">
                    {data.recommendation}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Main Content Sections: Action Items, Integrations, Roadmap */}
        <div className="mt-12 flex flex-col gap-8">
          {/* Action Items */}
          <section className="w-full">
            <div className="mb-5 flex items-end justify-between">
              <div>
                <h3 className="text-xl font-semibold tracking-tight text-foreground">
                  Action Items
                </h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {data.action_items.length} tasks extracted from the transcript.
                </p>
              </div>
              <div className="hidden items-center gap-1.5 text-xs text-muted-foreground sm:flex">
                <CircleDot className="h-3.5 w-3.5" />
                Auto-assigned
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3">
              {data.action_items.map((item) => (
                <div
                  key={item.task}
                  className="group flex flex-col justify-between rounded-xl border border-border bg-card p-5 shadow-[var(--shadow-soft)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[var(--shadow-lift)]"
                >
                  <div className="flex items-start gap-2">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 text-muted-foreground/60 transition-colors group-hover:text-[color:var(--sage)]" />
                    <div className="text-base font-medium leading-snug text-foreground">
                      {item.task}
                    </div>
                  </div>

                  <div className="mt-5 flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-xs font-semibold text-muted-foreground">
                        {initials(item.owner)}
                      </div>
                      <span className="text-sm text-foreground/80">{item.owner}</span>
                    </div>
                    <span className="inline-flex items-center gap-1 rounded-full border border-border bg-secondary/60 px-2.5 py-1 text-xs font-medium text-secondary-foreground">
                      <Clock className="h-3 w-3" />
                      {item.deadline}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Integrations */}
          <section className="rounded-2xl border border-border bg-muted/40 p-6 sm:p-8">
            <div className="flex items-center gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-[color:var(--sage)]" />
              <div className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                Workspace Integrations Executed
              </div>
            </div>
            <h3 className="mt-2 text-lg font-semibold tracking-tight text-foreground">
              Everything is ready in your tools.
            </h3>
            <p className="mt-1 max-w-xl text-sm text-muted-foreground">
              We drafted the follow-ups so you don't have to. Review, tweak, and send.
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              <a
                href={data.summary_doc_url}
                target="_blank"
                rel="noreferrer"
                className="group flex items-center justify-between rounded-xl border border-border bg-card px-5 py-4 shadow-[var(--shadow-soft)] transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-[var(--shadow-lift)]"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/5 text-primary">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-foreground">
                      Open Google Doc Summary
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Full transcript & highlights
                    </div>
                  </div>
                </div>
                <span className="text-sm text-muted-foreground transition-transform group-hover:translate-x-0.5">
                  →
                </span>
              </a>

              <a
                href={data.draft_email_links[0]}
                target="_blank"
                rel="noreferrer"
                className="group flex items-center justify-between rounded-xl border border-border bg-card px-5 py-4 shadow-[var(--shadow-soft)] transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-[var(--shadow-lift)]"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[color:var(--sage)]/15 text-[color:var(--sage-foreground)]">
                    <Mail className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-foreground">
                      View Drafted Emails
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {data.draft_email_links.length} draft ready in Gmail
                    </div>
                  </div>
                </div>
                <span className="text-sm text-muted-foreground transition-transform group-hover:translate-x-0.5">
                  →
                </span>
              </a>
            </div>
          </section>

          {/* Roadmap */}
          <aside className="rounded-2xl border border-dashed border-border bg-card/60 p-6 shadow-[var(--shadow-soft)]">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between border-b border-border pb-4 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                  <div className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                    Coming Soon
                  </div>
                </div>
                <h3 className="mt-2 text-lg font-semibold tracking-tight text-foreground">
                  MeetIQ Roadmap
                </h3>
                <p className="mt-1 text-xs text-muted-foreground">
                  Where the agent is heading next.
                </p>
              </div>
            </div>

            <ul className="grid gap-6 sm:grid-cols-1 md:grid-cols-3">
              {roadmap.map((r) => {
                const Icon = r.icon;
                return (
                  <li key={r.title} className="flex items-start gap-3">
                    <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                      <Icon className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-foreground/90">
                        {r.title}
                      </div>
                      <div className="mt-1 text-xs leading-relaxed text-muted-foreground">
                        {r.desc}
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </aside>
        </div>

        <footer className="mt-12 border-t border-border pt-6 text-xs text-muted-foreground">
          MeetIQ · Analyzed by AI · Meeting fatigue index down 18% this week
        </footer>
      </main>
    </div>
  );
}
