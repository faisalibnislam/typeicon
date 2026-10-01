import { z } from "zod";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { BUILD_FORMATS } from "@/lib/builds";
import { getSessionUser } from "@/lib/session";
import { queueSubsetBuild } from "@/lib/subset-queue";

const body = z.object({
  name: z.string().trim().min(1).max(60),
  items: z.array(z.object({ designId: uuid, style: styleSlug })).min(1).max(2000),
  formats: z.array(z.enum(BUILD_FORMATS)).min(1).max(BUILD_FORMATS.length),
});

/** Queue a subset build (public catalog assets only). */
export const POST = handle(async (req) => {
  const user = await getSessionUser();
  const input = await readJson(req, body);
  return queueSubsetBuild(req, user, input);
});
