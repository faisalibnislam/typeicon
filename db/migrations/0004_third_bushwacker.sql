ALTER TABLE "designs" ADD COLUMN "keywords" text[] DEFAULT '{}'::text[] NOT NULL;--> statement-breakpoint
ALTER TABLE "designs" ADD COLUMN "context" text;--> statement-breakpoint
ALTER TABLE "designs" drop column "search";--> statement-breakpoint
ALTER TABLE "designs" ADD COLUMN "search" "tsvector" GENERATED ALWAYS AS (setweight(to_tsvector('simple'::regconfig, coalesce(search_names, '')), 'A') || setweight(to_tsvector('simple'::regconfig, coalesce(search_tags, '')), 'B') || setweight(to_tsvector('english'::regconfig, coalesce(description, '') || ' ' || coalesce(context, '')), 'C') || setweight(to_tsvector('simple'::regconfig, coalesce(description, '') || ' ' || coalesce(context, '')), 'D')) STORED;--> statement-breakpoint
CREATE INDEX IF NOT EXISTS "designs_search_gin" ON "designs" USING gin ("search");
