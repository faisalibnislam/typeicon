CREATE TABLE "aliases" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"design_id" uuid NOT NULL,
	"namespace" text NOT NULL,
	"name" text NOT NULL,
	"kind" text DEFAULT 'alias' NOT NULL,
	"compile_to_font" boolean DEFAULT true NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "audit_events" (
	"id" bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "audit_events_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 CACHE 1),
	"actor_id" text,
	"action" text NOT NULL,
	"subject_type" text NOT NULL,
	"subject_id" text,
	"data" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "build_artifacts" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"scope" text NOT NULL,
	"cache_key" text NOT NULL,
	"storage_key" text NOT NULL,
	"file_name" text NOT NULL,
	"bytes" bigint NOT NULL,
	"sha256" text NOT NULL,
	"manifest" jsonb NOT NULL,
	"job_id" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"last_used_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "catalog_stats" (
	"id" text PRIMARY KEY NOT NULL,
	"data" jsonb NOT NULL,
	"computed_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "categories" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"slug" text NOT NULL,
	"name" text NOT NULL,
	"description" text,
	CONSTRAINT "categories_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "codepoint_assignments" (
	"namespace" text NOT NULL,
	"subject" text NOT NULL,
	"codepoint" integer NOT NULL,
	"bmp_codepoint" integer,
	"assigned_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "codepoint_assignments_namespace_subject_pk" PRIMARY KEY("namespace","subject")
);
--> statement-breakpoint
CREATE TABLE "collection_items" (
	"collection_id" uuid NOT NULL,
	"design_id" uuid NOT NULL,
	"style" text NOT NULL,
	"position" integer DEFAULT 0 NOT NULL,
	"added_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "collection_items_collection_id_design_id_style_pk" PRIMARY KEY("collection_id","design_id","style")
);
--> statement-breakpoint
CREATE TABLE "collections" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"owner_id" text NOT NULL,
	"name" text NOT NULL,
	"description" text,
	"is_public" boolean DEFAULT false NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "concepts" (
	"id" uuid PRIMARY KEY NOT NULL,
	"slug" text NOT NULL,
	"name" text NOT NULL,
	"description" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "concepts_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "custom_icons" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"owner_id" text NOT NULL,
	"kit_id" uuid NOT NULL,
	"name" text NOT NULL,
	"style" text DEFAULT 'line' NOT NULL,
	"svg" text NOT NULL,
	"svg_sha256" text NOT NULL,
	"route" text NOT NULL,
	"reasons" text[] DEFAULT '{}'::text[] NOT NULL,
	"outline_d" text,
	"outline_advance" integer,
	"codepoint" integer NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "design_categories" (
	"design_id" uuid NOT NULL,
	"category_id" uuid NOT NULL,
	CONSTRAINT "design_categories_design_id_category_id_pk" PRIMARY KEY("design_id","category_id")
);
--> statement-breakpoint
CREATE TABLE "design_tags" (
	"design_id" uuid NOT NULL,
	"tag_id" uuid NOT NULL,
	CONSTRAINT "design_tags_design_id_tag_id_pk" PRIMARY KEY("design_id","tag_id")
);
--> statement-breakpoint
CREATE TABLE "designs" (
	"id" uuid PRIMARY KEY NOT NULL,
	"concept_id" uuid NOT NULL,
	"source_pack_id" uuid NOT NULL,
	"name" text NOT NULL,
	"local_name" text NOT NULL,
	"native_name" text NOT NULL,
	"namespace" text NOT NULL,
	"area" text NOT NULL,
	"description" text,
	"tags" text[] DEFAULT '{}'::text[] NOT NULL,
	"category_slugs" text[] DEFAULT '{}'::text[] NOT NULL,
	"alias_names" text[] DEFAULT '{}'::text[] NOT NULL,
	"published_styles" text[] DEFAULT '{}'::text[] NOT NULL,
	"is_brand" boolean DEFAULT false NOT NULL,
	"derived_from" jsonb,
	"status" text DEFAULT 'pending' NOT NULL,
	"deprecated_by" text,
	"codepoint" integer,
	"bmp_codepoint" integer,
	"license_id" text NOT NULL,
	"first_release_id" uuid,
	"search_names" text DEFAULT '' NOT NULL,
	"search_tags" text DEFAULT '' NOT NULL,
	"search" "tsvector" GENERATED ALWAYS AS (setweight(to_tsvector('simple'::regconfig, coalesce(search_names, '')), 'A') || setweight(to_tsvector('simple'::regconfig, coalesce(search_tags, '')), 'B') || setweight(to_tsvector('english'::regconfig, coalesce(description, '')), 'C')) STORED,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "designs_name_unique" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "font_bundles" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"release_id" uuid NOT NULL,
	"slug" text NOT NULL,
	"family" text NOT NULL,
	"postscript_name" text NOT NULL,
	"source_pack_id" uuid NOT NULL,
	"style" text NOT NULL,
	"part" integer,
	"css_class" text NOT NULL,
	"glyph_count" integer NOT NULL,
	"keyword_count" integer NOT NULL,
	"files" jsonb NOT NULL,
	"validation" jsonb NOT NULL,
	"raster" jsonb,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "glyph_assignments" (
	"font_bundle_id" uuid NOT NULL,
	"variant_id" uuid NOT NULL,
	"codepoint" integer NOT NULL,
	"keywords" text[] NOT NULL,
	CONSTRAINT "glyph_assignments_font_bundle_id_variant_id_pk" PRIMARY KEY("font_bundle_id","variant_id")
);
--> statement-breakpoint
CREATE TABLE "jobs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"kind" text NOT NULL,
	"status" text DEFAULT 'queued' NOT NULL,
	"owner_id" text,
	"scope" text DEFAULT 'public' NOT NULL,
	"cache_key" text,
	"payload" jsonb NOT NULL,
	"result" jsonb,
	"error" text,
	"attempts" integer DEFAULT 0 NOT NULL,
	"max_attempts" integer DEFAULT 3 NOT NULL,
	"run_after" timestamp with time zone DEFAULT now() NOT NULL,
	"locked_by" text,
	"locked_at" timestamp with time zone,
	"heartbeat_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"started_at" timestamp with time zone,
	"finished_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "kit_versions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"kit_id" uuid NOT NULL,
	"version" integer NOT NULL,
	"selection" jsonb NOT NULL,
	"formats" text[] NOT NULL,
	"content_hash" text NOT NULL,
	"created_by" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "kits" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"owner_id" text NOT NULL,
	"team_id" uuid,
	"name" text NOT NULL,
	"slug" text NOT NULL,
	"embed_id" text NOT NULL,
	"pinned_release_id" uuid,
	"allowed_domains" text[] DEFAULT '{}'::text[] NOT NULL,
	"current_version" integer DEFAULT 0 NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "kits_embedId_unique" UNIQUE("embed_id")
);
--> statement-breakpoint
CREATE TABLE "licenses" (
	"id" text PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"url" text,
	"text" text NOT NULL,
	"osi_approved" boolean DEFAULT false NOT NULL,
	"notes" text,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "memberships" (
	"team_id" uuid NOT NULL,
	"user_id" text NOT NULL,
	"role" text DEFAULT 'member' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "memberships_team_id_user_id_pk" PRIMARY KEY("team_id","user_id")
);
--> statement-breakpoint
CREATE TABLE "name_registry" (
	"namespace" text NOT NULL,
	"name" text NOT NULL,
	"design_id" uuid NOT NULL,
	"kind" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "name_registry_namespace_name_pk" PRIMARY KEY("namespace","name")
);
--> statement-breakpoint
CREATE TABLE "outbox" (
	"id" bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "outbox_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 CACHE 1),
	"topic" text NOT NULL,
	"payload" jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"processed_at" timestamp with time zone,
	"attempts" integer DEFAULT 0 NOT NULL,
	"last_error" text
);
--> statement-breakpoint
CREATE TABLE "plans" (
	"slug" text PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"capabilities" jsonb NOT NULL,
	"is_default" boolean DEFAULT false NOT NULL
);
--> statement-breakpoint
CREATE TABLE "rate_limits" (
	"key" text NOT NULL,
	"window_start" timestamp with time zone NOT NULL,
	"count" integer DEFAULT 0 NOT NULL,
	CONSTRAINT "rate_limits_key_window_start_pk" PRIMARY KEY("key","window_start")
);
--> statement-breakpoint
CREATE TABLE "release_archives" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"release_id" uuid NOT NULL,
	"kind" text NOT NULL,
	"label" text NOT NULL,
	"file" text NOT NULL,
	"storage_key" text NOT NULL,
	"bytes" bigint NOT NULL,
	"sha256" text NOT NULL,
	"meta" jsonb DEFAULT '{}'::jsonb NOT NULL
);
--> statement-breakpoint
CREATE TABLE "releases" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"version" text NOT NULL,
	"release_date" date NOT NULL,
	"status" text DEFAULT 'draft' NOT NULL,
	"toolchain" text,
	"counts" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"manifest" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"archive_index" jsonb,
	"approved_by" text,
	"approved_at" timestamp with time zone,
	"published_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "releases_version_unique" UNIQUE("version")
);
--> statement-breakpoint
CREATE TABLE "search_metrics" (
	"id" bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "search_metrics_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 CACHE 1),
	"query_length" integer NOT NULL,
	"result_count" integer NOT NULL,
	"duration_ms" double precision NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "source_packs" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"slug" text NOT NULL,
	"area" text NOT NULL,
	"display_name" text NOT NULL,
	"namespace" text NOT NULL,
	"name_prefix" text DEFAULT '' NOT NULL,
	"upstream_url" text,
	"author" text,
	"copyright" text,
	"version" text NOT NULL,
	"distribution" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"retrieved_at" date,
	"license_id" text NOT NULL,
	"notices" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"attribution_required" boolean DEFAULT false NOT NULL,
	"attribution_text" text,
	"reserved_font_names" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"permissions" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"style_mapping" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"style_mapping_note" text,
	"trademark_note" text,
	"review_status" text DEFAULT 'pending' NOT NULL,
	"reviewed_by" text,
	"reviewed_at" date,
	"review_note" text,
	"modification_history" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "source_packs_slug_unique" UNIQUE("slug"),
	CONSTRAINT "source_packs_namespace_unique" UNIQUE("namespace")
);
--> statement-breakpoint
CREATE TABLE "styles" (
	"slug" text PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"description" text NOT NULL,
	"sort_order" integer DEFAULT 0 NOT NULL,
	"is_core" boolean DEFAULT true NOT NULL
);
--> statement-breakpoint
CREATE TABLE "tags" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"slug" text NOT NULL,
	CONSTRAINT "tags_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "teams" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"slug" text NOT NULL,
	"name" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "teams_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "user_entitlements" (
	"user_id" text NOT NULL,
	"plan_slug" text NOT NULL,
	"source" text NOT NULL,
	"starts_at" timestamp with time zone DEFAULT now() NOT NULL,
	"ends_at" timestamp with time zone,
	CONSTRAINT "user_entitlements_user_id_plan_slug_pk" PRIMARY KEY("user_id","plan_slug")
);
--> statement-breakpoint
CREATE TABLE "variants" (
	"id" uuid PRIMARY KEY NOT NULL,
	"design_id" uuid NOT NULL,
	"style" text NOT NULL,
	"native_style" text NOT NULL,
	"native_label" text NOT NULL,
	"status" text NOT NULL,
	"review_status" text DEFAULT 'approved' NOT NULL,
	"route" text NOT NULL,
	"reasons" text[] DEFAULT '{}'::text[] NOT NULL,
	"duplicate_of_style" text,
	"svg" text,
	"svg_sha256" text,
	"view_box" real[],
	"source_path" text NOT NULL,
	"source_sha256" text NOT NULL,
	"outline_key" text,
	"outline_d" text,
	"outline_advance" integer,
	"font_supported" boolean DEFAULT false NOT NULL,
	"first_release_id" uuid,
	"updated_release_id" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "account" (
	"id" text PRIMARY KEY NOT NULL,
	"account_id" text NOT NULL,
	"provider_id" text NOT NULL,
	"user_id" text NOT NULL,
	"access_token" text,
	"refresh_token" text,
	"id_token" text,
	"access_token_expires_at" timestamp,
	"refresh_token_expires_at" timestamp,
	"scope" text,
	"password" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp NOT NULL
);
--> statement-breakpoint
CREATE TABLE "session" (
	"id" text PRIMARY KEY NOT NULL,
	"expires_at" timestamp NOT NULL,
	"token" text NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp NOT NULL,
	"ip_address" text,
	"user_agent" text,
	"user_id" text NOT NULL,
	CONSTRAINT "session_token_unique" UNIQUE("token")
);
--> statement-breakpoint
CREATE TABLE "user" (
	"id" text PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"email" text NOT NULL,
	"email_verified" boolean DEFAULT false NOT NULL,
	"image" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	"role" text DEFAULT 'user',
	CONSTRAINT "user_email_unique" UNIQUE("email")
);
--> statement-breakpoint
CREATE TABLE "verification" (
	"id" text PRIMARY KEY NOT NULL,
	"identifier" text NOT NULL,
	"value" text NOT NULL,
	"expires_at" timestamp NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "aliases" ADD CONSTRAINT "aliases_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "build_artifacts" ADD CONSTRAINT "build_artifacts_job_id_jobs_id_fk" FOREIGN KEY ("job_id") REFERENCES "public"."jobs"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "collection_items" ADD CONSTRAINT "collection_items_collection_id_collections_id_fk" FOREIGN KEY ("collection_id") REFERENCES "public"."collections"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "collection_items" ADD CONSTRAINT "collection_items_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "collection_items" ADD CONSTRAINT "collection_items_style_styles_slug_fk" FOREIGN KEY ("style") REFERENCES "public"."styles"("slug") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "collections" ADD CONSTRAINT "collections_owner_id_user_id_fk" FOREIGN KEY ("owner_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD CONSTRAINT "custom_icons_owner_id_user_id_fk" FOREIGN KEY ("owner_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD CONSTRAINT "custom_icons_kit_id_kits_id_fk" FOREIGN KEY ("kit_id") REFERENCES "public"."kits"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "custom_icons" ADD CONSTRAINT "custom_icons_style_styles_slug_fk" FOREIGN KEY ("style") REFERENCES "public"."styles"("slug") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "design_categories" ADD CONSTRAINT "design_categories_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "design_categories" ADD CONSTRAINT "design_categories_category_id_categories_id_fk" FOREIGN KEY ("category_id") REFERENCES "public"."categories"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "design_tags" ADD CONSTRAINT "design_tags_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "design_tags" ADD CONSTRAINT "design_tags_tag_id_tags_id_fk" FOREIGN KEY ("tag_id") REFERENCES "public"."tags"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "designs" ADD CONSTRAINT "designs_concept_id_concepts_id_fk" FOREIGN KEY ("concept_id") REFERENCES "public"."concepts"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "designs" ADD CONSTRAINT "designs_source_pack_id_source_packs_id_fk" FOREIGN KEY ("source_pack_id") REFERENCES "public"."source_packs"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "designs" ADD CONSTRAINT "designs_license_id_licenses_id_fk" FOREIGN KEY ("license_id") REFERENCES "public"."licenses"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "designs" ADD CONSTRAINT "designs_first_release_id_releases_id_fk" FOREIGN KEY ("first_release_id") REFERENCES "public"."releases"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "font_bundles" ADD CONSTRAINT "font_bundles_release_id_releases_id_fk" FOREIGN KEY ("release_id") REFERENCES "public"."releases"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "font_bundles" ADD CONSTRAINT "font_bundles_source_pack_id_source_packs_id_fk" FOREIGN KEY ("source_pack_id") REFERENCES "public"."source_packs"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "font_bundles" ADD CONSTRAINT "font_bundles_style_styles_slug_fk" FOREIGN KEY ("style") REFERENCES "public"."styles"("slug") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "glyph_assignments" ADD CONSTRAINT "glyph_assignments_font_bundle_id_font_bundles_id_fk" FOREIGN KEY ("font_bundle_id") REFERENCES "public"."font_bundles"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "glyph_assignments" ADD CONSTRAINT "glyph_assignments_variant_id_variants_id_fk" FOREIGN KEY ("variant_id") REFERENCES "public"."variants"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "jobs" ADD CONSTRAINT "jobs_owner_id_user_id_fk" FOREIGN KEY ("owner_id") REFERENCES "public"."user"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "kit_versions" ADD CONSTRAINT "kit_versions_kit_id_kits_id_fk" FOREIGN KEY ("kit_id") REFERENCES "public"."kits"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "kit_versions" ADD CONSTRAINT "kit_versions_created_by_user_id_fk" FOREIGN KEY ("created_by") REFERENCES "public"."user"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "kits" ADD CONSTRAINT "kits_owner_id_user_id_fk" FOREIGN KEY ("owner_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "kits" ADD CONSTRAINT "kits_team_id_teams_id_fk" FOREIGN KEY ("team_id") REFERENCES "public"."teams"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "kits" ADD CONSTRAINT "kits_pinned_release_id_releases_id_fk" FOREIGN KEY ("pinned_release_id") REFERENCES "public"."releases"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "memberships" ADD CONSTRAINT "memberships_team_id_teams_id_fk" FOREIGN KEY ("team_id") REFERENCES "public"."teams"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "memberships" ADD CONSTRAINT "memberships_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "name_registry" ADD CONSTRAINT "name_registry_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "release_archives" ADD CONSTRAINT "release_archives_release_id_releases_id_fk" FOREIGN KEY ("release_id") REFERENCES "public"."releases"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "source_packs" ADD CONSTRAINT "source_packs_license_id_licenses_id_fk" FOREIGN KEY ("license_id") REFERENCES "public"."licenses"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_entitlements" ADD CONSTRAINT "user_entitlements_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_entitlements" ADD CONSTRAINT "user_entitlements_plan_slug_plans_slug_fk" FOREIGN KEY ("plan_slug") REFERENCES "public"."plans"("slug") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "variants" ADD CONSTRAINT "variants_design_id_designs_id_fk" FOREIGN KEY ("design_id") REFERENCES "public"."designs"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "variants" ADD CONSTRAINT "variants_style_styles_slug_fk" FOREIGN KEY ("style") REFERENCES "public"."styles"("slug") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "variants" ADD CONSTRAINT "variants_first_release_id_releases_id_fk" FOREIGN KEY ("first_release_id") REFERENCES "public"."releases"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "variants" ADD CONSTRAINT "variants_updated_release_id_releases_id_fk" FOREIGN KEY ("updated_release_id") REFERENCES "public"."releases"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "account" ADD CONSTRAINT "account_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "session" ADD CONSTRAINT "session_user_id_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."user"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE UNIQUE INDEX "aliases_ns_name_uq" ON "aliases" USING btree ("namespace","name");--> statement-breakpoint
CREATE INDEX "audit_events_subject_idx" ON "audit_events" USING btree ("subject_type","subject_id");--> statement-breakpoint
CREATE INDEX "audit_events_created_idx" ON "audit_events" USING btree ("created_at");--> statement-breakpoint
CREATE UNIQUE INDEX "build_artifacts_scope_key_uq" ON "build_artifacts" USING btree ("scope","cache_key");--> statement-breakpoint
CREATE UNIQUE INDEX "codepoints_ns_cp_uq" ON "codepoint_assignments" USING btree ("namespace","codepoint");--> statement-breakpoint
CREATE UNIQUE INDEX "codepoints_ns_bmp_uq" ON "codepoint_assignments" USING btree ("namespace","bmp_codepoint");--> statement-breakpoint
CREATE INDEX "collections_owner_idx" ON "collections" USING btree ("owner_id");--> statement-breakpoint
CREATE UNIQUE INDEX "custom_icons_kit_name_style_uq" ON "custom_icons" USING btree ("kit_id","name","style");--> statement-breakpoint
CREATE UNIQUE INDEX "custom_icons_kit_cp_style_uq" ON "custom_icons" USING btree ("kit_id","codepoint","style");--> statement-breakpoint
CREATE INDEX "design_tags_tag_idx" ON "design_tags" USING btree ("tag_id");--> statement-breakpoint
CREATE UNIQUE INDEX "designs_source_native_uq" ON "designs" USING btree ("source_pack_id","native_name");--> statement-breakpoint
CREATE INDEX "designs_search_gin" ON "designs" USING gin ("search");--> statement-breakpoint
CREATE INDEX "designs_local_trgm" ON "designs" USING gin ("local_name" gin_trgm_ops);--> statement-breakpoint
CREATE INDEX "designs_name_trgm" ON "designs" USING gin ("name" gin_trgm_ops);--> statement-breakpoint
CREATE INDEX "designs_categories_gin" ON "designs" USING gin ("category_slugs");--> statement-breakpoint
CREATE INDEX "designs_aliases_gin" ON "designs" USING gin ("alias_names");--> statement-breakpoint
CREATE INDEX "designs_styles_gin" ON "designs" USING gin ("published_styles");--> statement-breakpoint
CREATE INDEX "designs_area_status_idx" ON "designs" USING btree ("area","status");--> statement-breakpoint
CREATE INDEX "designs_concept_idx" ON "designs" USING btree ("concept_id");--> statement-breakpoint
CREATE UNIQUE INDEX "font_bundles_release_slug_uq" ON "font_bundles" USING btree ("release_id","slug");--> statement-breakpoint
CREATE INDEX "glyph_assignments_variant_idx" ON "glyph_assignments" USING btree ("variant_id");--> statement-breakpoint
CREATE INDEX "jobs_claim_idx" ON "jobs" USING btree ("status","run_after");--> statement-breakpoint
CREATE INDEX "jobs_owner_idx" ON "jobs" USING btree ("owner_id","created_at");--> statement-breakpoint
CREATE INDEX "jobs_cache_idx" ON "jobs" USING btree ("scope","cache_key");--> statement-breakpoint
CREATE UNIQUE INDEX "kit_versions_kit_version_uq" ON "kit_versions" USING btree ("kit_id","version");--> statement-breakpoint
CREATE UNIQUE INDEX "kits_owner_slug_uq" ON "kits" USING btree ("owner_id","slug");--> statement-breakpoint
CREATE INDEX "name_registry_design_idx" ON "name_registry" USING btree ("design_id");--> statement-breakpoint
CREATE INDEX "outbox_pending_idx" ON "outbox" USING btree ("processed_at","id");--> statement-breakpoint
CREATE UNIQUE INDEX "release_archives_release_file_uq" ON "release_archives" USING btree ("release_id","file");--> statement-breakpoint
CREATE INDEX "search_metrics_created_idx" ON "search_metrics" USING btree ("created_at");--> statement-breakpoint
CREATE UNIQUE INDEX "variants_design_style_uq" ON "variants" USING btree ("design_id","style");--> statement-breakpoint
CREATE INDEX "variants_style_status_idx" ON "variants" USING btree ("style","status");--> statement-breakpoint
CREATE INDEX "variants_svg_sha_idx" ON "variants" USING btree ("svg_sha256");--> statement-breakpoint
CREATE INDEX "account_userId_idx" ON "account" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "session_userId_idx" ON "session" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "verification_identifier_idx" ON "verification" USING btree ("identifier");