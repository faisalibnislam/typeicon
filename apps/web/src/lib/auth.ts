import "server-only";
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { nextCookies } from "better-auth/next-js";
import { db } from "@/db";
import * as authSchema from "@/db/auth-schema";
import { authOptions } from "./auth-options";

export const auth = betterAuth({
  ...authOptions,
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL ?? "http://localhost:3107",
  database: drizzleAdapter(db, { provider: "pg", schema: authSchema }),
  plugins: [nextCookies()],
});

export type Session = typeof auth.$Infer.Session;
