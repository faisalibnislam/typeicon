import type { BetterAuthOptions } from "better-auth";

/** Options shared by the runtime auth instance and the schema generator. */
export const authOptions = {
  appName: "TypeIcon",
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 10,
    maxPasswordLength: 128,
    autoSignIn: true,
  },
  user: {
    additionalFields: {
      // Roles are assigned server-side only (see scripts/grant-admin.ts); never from input.
      role: { type: "string", required: false, defaultValue: "user", input: false },
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 14,
    updateAge: 60 * 60 * 24,
  },
  rateLimit: {
    enabled: true,
    window: 60,
    max: 60,
  },
  advanced: {
    database: { generateId: () => crypto.randomUUID() },
  },
} satisfies Omit<BetterAuthOptions, "database">;
