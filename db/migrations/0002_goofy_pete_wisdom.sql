CREATE TABLE "metadata_overrides" (
	"design_name" text PRIMARY KEY NOT NULL,
	"data" jsonb NOT NULL,
	"updated_by" text NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
