// Used only by `@better-auth/cli generate` to emit src/db/auth-schema.ts.
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { authOptions } from "../src/lib/auth-options";

export const auth = betterAuth({
  ...authOptions,
  database: drizzleAdapter({} as never, { provider: "pg" }),
});
