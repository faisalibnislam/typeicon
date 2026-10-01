import "server-only";
import { createReadStream, promises as fs } from "node:fs";
import path from "node:path";
import { Readable } from "node:stream";
import { GetObjectCommand, HeadObjectCommand, PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { repoRoot } from "./paths";

const KEY_RE = /^[A-Za-z0-9._-]+(?:\/[A-Za-z0-9._-]+)*$/;

export function checkKey(key: string): string {
  if (!KEY_RE.test(key) || key.split("/").includes("..")) throw new Error(`invalid storage key ${key}`);
  return key;
}

export interface StoredObject {
  body: ReadableStream<Uint8Array>;
  size: number;
}

interface StorageDriver {
  get(key: string): Promise<StoredObject | null>;
  put(key: string, data: Uint8Array, contentType: string): Promise<void>;
  exists(key: string): Promise<boolean>;
  /** Direct URL for public objects (CDN), or null when downloads must stream through the app. */
  publicUrl(key: string): string | null;
  signedUrl(key: string, fileName: string, seconds?: number): Promise<string | null>;
}

class FsDriver implements StorageDriver {
  constructor(private root: string) {}
  private file(key: string) {
    const p = path.resolve(this.root, checkKey(key));
    if (!p.startsWith(path.resolve(this.root) + path.sep)) throw new Error("storage key escapes root");
    return p;
  }
  async get(key: string) {
    const p = this.file(key);
    try {
      const st = await fs.stat(p);
      const stream = Readable.toWeb(createReadStream(p)) as ReadableStream<Uint8Array>;
      return { body: stream, size: st.size };
    } catch {
      return null;
    }
  }
  async put(key: string, data: Uint8Array) {
    const p = this.file(key);
    await fs.mkdir(path.dirname(p), { recursive: true });
    await fs.writeFile(p + ".tmp", data);
    await fs.rename(p + ".tmp", p);
  }
  async exists(key: string) {
    try {
      await fs.access(this.file(key));
      return true;
    } catch {
      return false;
    }
  }
  publicUrl() {
    return null;
  }
  async signedUrl() {
    return null;
  }
}

class S3Driver implements StorageDriver {
  private client = new S3Client({
    endpoint: process.env.S3_ENDPOINT || undefined,
    region: process.env.S3_REGION || "auto",
    forcePathStyle: Boolean(process.env.S3_ENDPOINT),
    credentials: process.env.S3_ACCESS_KEY_ID
      ? { accessKeyId: process.env.S3_ACCESS_KEY_ID, secretAccessKey: process.env.S3_SECRET_ACCESS_KEY ?? "" }
      : undefined,
  });
  private bucket = process.env.S3_BUCKET ?? "typeicon";
  async get(key: string) {
    try {
      const r = await this.client.send(new GetObjectCommand({ Bucket: this.bucket, Key: checkKey(key) }));
      return { body: r.Body!.transformToWebStream() as ReadableStream<Uint8Array>, size: Number(r.ContentLength ?? 0) };
    } catch {
      return null;
    }
  }
  async put(key: string, data: Uint8Array, contentType: string) {
    await this.client.send(new PutObjectCommand({ Bucket: this.bucket, Key: checkKey(key), Body: data, ContentType: contentType }));
  }
  async exists(key: string) {
    try {
      await this.client.send(new HeadObjectCommand({ Bucket: this.bucket, Key: checkKey(key) }));
      return true;
    } catch {
      return false;
    }
  }
  publicUrl(key: string) {
    const base = process.env.S3_PUBLIC_BASE_URL;
    return base && key.startsWith("releases/") ? `${base.replace(/\/$/, "")}/${checkKey(key)}` : null;
  }
  async signedUrl(key: string, fileName: string, seconds = 300) {
    return getSignedUrl(
      this.client,
      new GetObjectCommand({
        Bucket: this.bucket,
        Key: checkKey(key),
        ResponseContentDisposition: `attachment; filename="${fileName.replace(/[^\w.-]/g, "_")}"`,
      }),
      { expiresIn: seconds },
    );
  }
}

let driver: StorageDriver | undefined;
export function storage(): StorageDriver {
  if (driver) return driver;
  if (process.env.STORAGE_DRIVER === "s3") return (driver = new S3Driver());
  const root = process.env.STORAGE_FS_ROOT ?? ".data/storage";
  return (driver = new FsDriver(path.isAbsolute(root) ? root : path.join(repoRoot(), root)));
}

export const CONTENT_TYPES: Record<string, string> = {
  ".zip": "application/zip",
  ".json": "application/json",
  ".otf": "font/otf",
  ".ttf": "font/ttf",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
};
export function contentTypeFor(name: string) {
  return CONTENT_TYPES[path.extname(name)] ?? "application/octet-stream";
}
