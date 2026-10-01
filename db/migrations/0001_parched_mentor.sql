ALTER TABLE "custom_icons" ALTER COLUMN "svg" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "custom_icons" ALTER COLUMN "svg_sha256" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "custom_icons" ALTER COLUMN "route" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD COLUMN "status" text DEFAULT 'pending' NOT NULL;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD COLUMN "raw_svg" text;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD COLUMN "archived_at" timestamp with time zone;