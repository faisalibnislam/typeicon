"use client";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { signIn, signUp } from "@/lib/auth-client";

function safeNext(next: string | null): string {
  // Only same-site relative paths: prevents open redirects via ?next=
  return next && next.startsWith("/") && !next.startsWith("//") ? next : "/account";
}

export function AuthForm({ mode }: { mode: "sign-in" | "sign-up" }) {
  const router = useRouter();
  const params = useSearchParams();
  const next = safeNext(params.get("next"));
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const email = String(f.get("email") ?? "").trim();
    const password = String(f.get("password") ?? "");
    setBusy(true);
    setError(null);
    const res =
      mode === "sign-in"
        ? await signIn.email({ email, password })
        : await signUp.email({ email, password, name: String(f.get("name") ?? "").trim() || email.split("@")[0] });
    setBusy(false);
    if (res.error) {
      setError(res.error.message ?? "Something went wrong");
      return;
    }
    router.push(next);
    router.refresh();
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4" noValidate>
      {mode === "sign-up" && (
        <div>
          <label htmlFor="name" className="mb-1 block text-sm text-text-2">Name</label>
          <input id="name" name="name" autoComplete="name" maxLength={80} className="h-10 w-full rounded-xl border border-border bg-surface px-3 text-sm" />
        </div>
      )}
      <div>
        <label htmlFor="email" className="mb-1 block text-sm text-text-2">Email</label>
        <input id="email" name="email" type="email" required autoComplete="email" className="h-10 w-full rounded-xl border border-border bg-surface px-3 text-sm" />
      </div>
      <div>
        <label htmlFor="password" className="mb-1 block text-sm text-text-2">Password</label>
        <input id="password" name="password" type="password" required minLength={10} autoComplete={mode === "sign-in" ? "current-password" : "new-password"} className="h-10 w-full rounded-xl border border-border bg-surface px-3 text-sm" aria-describedby={mode === "sign-up" ? "pw-hint" : undefined} />
        {mode === "sign-up" && <p id="pw-hint" className="mt-1 text-xs text-muted">At least 10 characters.</p>}
      </div>
      {error && <p role="alert" className="text-sm text-danger">{error}</p>}
      <button type="submit" disabled={busy} className="h-10 w-full rounded-xl bg-accent text-sm font-semibold text-accent-contrast hover:bg-accent-hover disabled:opacity-60">
        {busy ? "Please wait…" : mode === "sign-in" ? "Sign in" : "Create account"}
      </button>
      <p className="text-center text-sm text-muted">
        {mode === "sign-in" ? (
          <>No account? <Link href={`/sign-up?next=${encodeURIComponent(next)}`} className="text-accent underline underline-offset-2">Create one</Link></>
        ) : (
          <>Already have an account? <Link href={`/sign-in?next=${encodeURIComponent(next)}`} className="text-accent underline underline-offset-2">Sign in</Link></>
        )}
      </p>
    </form>
  );
}
