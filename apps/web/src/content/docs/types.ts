export interface DocMeta {
  slug: string;
  title: string;
  description: string;
  section: "Start" | "Desktop" | "Web" | "Reference";
  order: number;
}
