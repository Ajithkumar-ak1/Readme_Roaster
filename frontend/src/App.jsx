import { useMemo, useState } from "react";

const MODES = ["funny", "professional", "savage"];
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/roast";

function isValidGitHubUrl(url) {
  const pattern = /^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\/?$/i;
  return pattern.test(url.trim());
}

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [mode, setMode] = useState("funny");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [result, setResult] = useState(null);

  const canSubmit = useMemo(() => isValidGitHubUrl(repoUrl) && !loading, [repoUrl, loading]);

  const showToast = (message) => {
    setToast(message);
    window.clearTimeout(window.__toastTimer);
    window.__toastTimer = window.setTimeout(() => setToast(""), 1800);
  };

  const roastReadme = async () => {
    if (!isValidGitHubUrl(repoUrl)) {
      setError("Please enter a valid GitHub repository URL.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl.trim(), mode }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to roast README.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const copyImprovedReadme = async () => {
    if (!result?.improved_readme) {
      return;
    }

    try {
      await navigator.clipboard.writeText(result.improved_readme);
      showToast("Improved README copied.");
    } catch {
      showToast("Copy failed. Try again.");
    }
  };

  return (
    <main className="card-grid flex min-h-screen items-center justify-center p-4 sm:p-8">
      <section className="w-full max-w-4xl rounded-2xl border border-white/10 bg-panel/90 p-5 shadow-glow backdrop-blur sm:p-8">
        <div className="mb-6 fade-in">
          <p className="mb-2 text-xs uppercase tracking-[0.24em] text-ember">AI GitHub Critic</p>
          <h1 className="text-3xl font-extrabold leading-tight sm:text-4xl">README Roaster</h1>
          <p className="mt-2 text-sm text-smoke sm:text-base">
            Roast your README, uncover weak spots, and get a polished rewrite in one click.
          </p>
        </div>

        <div className="mb-5 grid gap-3 sm:grid-cols-[1fr_180px] fade-in">
          <input
            type="url"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/owner/repo"
            className="w-full rounded-lg border border-white/15 bg-black/30 px-4 py-3 text-sm outline-none ring-0 transition focus:border-ember"
          />

          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="rounded-lg border border-white/15 bg-black/30 px-4 py-3 text-sm outline-none transition focus:border-ember"
          >
            {MODES.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={roastReadme}
          disabled={!canSubmit}
          className="mb-5 inline-flex w-full items-center justify-center rounded-lg bg-ember px-6 py-3 text-sm font-semibold text-black transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-55 sm:w-auto"
        >
          {loading ? (
            <span className="inline-flex items-center gap-2">
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-black border-t-transparent" />
              Roasting...
            </span>
          ) : (
            "Roast My README 🔥"
          )}
        </button>

        {error && <div className="mb-5 rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-200">{error}</div>}

        {result && (
          <div className="space-y-5 fade-in">
            <article className="rounded-xl border border-ember/40 bg-black/30 p-4">
              <h2 className="mb-2 text-sm uppercase tracking-wide text-ember">Roast</h2>
              <p className="whitespace-pre-line text-base leading-relaxed">{result.roast}</p>
            </article>

            <article className="rounded-xl border border-white/10 bg-black/25 p-4">
              <h2 className="mb-2 text-sm uppercase tracking-wide text-ember">Issues</h2>
              <ul className="list-disc space-y-1 pl-5 text-sm text-slate-200">
                {result.issues?.map((issue, idx) => (
                  <li key={`issue-${idx}`}>{issue}</li>
                ))}
              </ul>
            </article>

            <article className="rounded-xl border border-white/10 bg-black/25 p-4">
              <h2 className="mb-2 text-sm uppercase tracking-wide text-ember">Suggestions</h2>
              <ul className="list-disc space-y-1 pl-5 text-sm text-slate-200">
                {result.suggestions?.map((suggestion, idx) => (
                  <li key={`suggestion-${idx}`}>{suggestion}</li>
                ))}
              </ul>
            </article>

            <article className="rounded-xl border border-white/10 bg-black/25 p-4">
              <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-sm uppercase tracking-wide text-ember">Improved README</h2>
                <button
                  onClick={copyImprovedReadme}
                  className="rounded-md border border-white/20 bg-white/5 px-3 py-1 text-xs text-white transition hover:border-ember"
                >
                  Copy
                </button>
              </div>
              <pre className="max-h-80 overflow-auto rounded-lg border border-white/10 bg-black/50 p-4 text-xs text-slate-200">
                <code>{result.improved_readme}</code>
              </pre>
            </article>
          </div>
        )}

        {toast && (
          <div className="fixed bottom-4 right-4 rounded-md border border-emerald-400/40 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-200 fade-in">
            {toast}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
