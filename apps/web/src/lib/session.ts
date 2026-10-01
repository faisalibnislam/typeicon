import "server-only";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "./auth";

export type SessionUser = { id: string; email: string; name: string; role: string };

export async function getSessionUser(): Promise<SessionUser | null> {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) return null;
  const u = session.user as typeof session.user & { role?: string | null };
  return { id: u.id, email: u.email, name: u.name, role: u.role ?? "user" };
}

/** For pages: redirect anonymous visitors to sign-in. */
export async function requireUser(next = "/account"): Promise<SessionUser> {
  const user = await getSessionUser();
  if (!user) redirect(`/sign-in?next=${encodeURIComponent(next)}`);
  return user;
}

/** For pages: only admins. Everyone else gets a 404, which avoids advertising the route. */
export async function requireAdmin(): Promise<SessionUser> {
  const user = await getSessionUser();
  if (!user) redirect("/sign-in?next=/admin");
  if (user.role !== "admin") {
    const { notFound } = await import("next/navigation");
    notFound();
  }
  return user;
}

export class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

/** For route handlers: server-side ownership/role checks. */
export async function apiUser(opts: { admin?: boolean } = {}): Promise<SessionUser> {
  const user = await getSessionUser();
  if (!user) throw new HttpError(401, "Sign in required");
  if (opts.admin && user.role !== "admin") throw new HttpError(403, "Admin role required");
  return user;
}
