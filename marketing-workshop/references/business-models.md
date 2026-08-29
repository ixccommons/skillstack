# Business Models

`positioning_input.fields.business_model` gets mapped to one of these nine
values (`pipeline-state.json.business_model`). Every stage of this pipeline —
research, copy, distribution, measurement — should read this table before
making a model-specific recommendation, rather than defaulting to B2B SaaS
patterns for everything.

If a business genuinely spans two rows (a marketplace with a B2B supply
side, a consumer app with a subscription), pick the row that governs the
*objective this pipeline run is built for*, and note the secondary model in
`constraints`.

---

### B2B SaaS

- **Funnel:** awareness → qualified conversation → demo/consultation →
  opportunity → customer
- **Conversion asset:** homepage or landing page driving to a demo request or
  trial signup
- **Channels:** category directories, comparison pages, communities where the
  buyer persona is present, partner/integration listings, trade press
- **Measurement:** MQL/SQL if a sales process exists, else trial-to-paid;
  CAC and payback period are diagnostic, never invented — see
  `references/evidence-policy.md`
- **Buying process:** often multi-stakeholder, evaluation period measured in
  weeks; objections cluster on switching cost and integration
- **Proof:** logos, case studies with numbers, security/compliance posture,
  integration list
- **Retention:** usage-based renewal signals (seat growth, feature adoption),
  not repeat purchase

### B2B service or agency

- **Funnel:** awareness → qualified conversation → proposal → engagement →
  referral/repeat engagement
- **Conversion asset:** one-pager or case-study-driven landing page, often
  paired with a direct outreach-adjacent context (this pipeline does not do
  outreach — see `references/execution-policy.md` scope note)
- **Channels:** referral network, industry associations, speaking/publication
  placements, directories specific to the service category
- **Measurement:** proposal-to-close rate, engagement value, referral rate;
  volume metrics (traffic, impressions) are weak proxies here
- **Buying process:** relationship-driven, trust-gated; objections cluster on
  "too small" and "prove you've done this before"
- **Proof:** named client work, specific outcomes, the founder or lead
  practitioner as a visible person
- **Retention:** repeat engagement and referral rate, not subscription churn

### Ecommerce / D2C

- **Funnel:** discovery → product view → cart → purchase → repeat purchase
- **Conversion asset:** product page or campaign landing page
- **Channels:** marketplaces, social/visual discovery surfaces, comparison
  and review sites, affiliate/creator placements
- **Measurement:** conversion rate by traffic source, AOV, repeat purchase
  rate; cart abandonment is diagnostic
- **Buying process:** often single-session, price and trust sensitive at the
  point of purchase
- **Proof:** reviews, return policy, shipping clarity, visible unit economics
  of the offer (price vs. comparable alternatives)
- **Retention:** repeat purchase rate and time-to-second-purchase are the
  north-star candidates, not just first conversion

### Consumer application

- **Funnel:** discovery → install → activation → retention → paid conversion
- **Conversion asset:** app store listing plus a landing page for
  pre-install context
- **Channels:** app store optimization, creator/influencer placements,
  communities around the problem (not the category), press for launch
  moments
- **Measurement:** activation rate (a defined first-value event, not just
  install), D7/D30 retention, free-to-paid conversion
- **Buying process:** low-friction, often impulsive; objections are more
  about trust and permissions than price
- **Proof:** social proof at scale (ratings, install counts), screenshots
  that show the actual experience
- **Retention:** the north star is usually retention itself, not a purchase
  event

### Local business

- **Funnel:** discovery → call/booking/directions → visit → review → repeat
  visit
- **Conversion asset:** a local listing plus a booking/contact page; the
  listing often out-converts the website
- **Channels:** local search and map listings, local directories and
  associations, neighborhood community platforms, review platforms
- **Measurement:** calls/bookings/direction requests, review volume and
  rating, repeat-visit rate
- **Buying process:** proximity and immediacy driven; objections cluster on
  trust signals (reviews, hours, responsiveness)
- **Proof:** reviews, photos of the actual place/work, response time to
  inquiries
- **Retention:** repeat-visit and referral rate within the local area

### Creator or personal brand

- **Funnel:** discovery → subscription/registration → attendance/
  participation → return → purchase/support
- **Conversion asset:** a bio/landing page driving to a single next action
  (subscribe, follow, buy)
- **Channels:** the creator's existing platform plus adjacent creator
  communities, guest appearances, newsletters in the niche
- **Measurement:** follow/subscribe rate, return-visit or repeat-listen/watch
  rate, conversion to paid support where applicable
- **Buying process:** parasocial trust built over repeated exposure, not a
  single-session decision
- **Proof:** consistency of output, audience engagement (not just size),
  testimonials from the audience itself
- **Retention:** the north star is usually returning audience share, not a
  single transaction

### Event or community

- **Funnel:** discovery → registration → attendance/participation → return
- **Conversion asset:** an event or membership landing page with a clear
  date/commitment and a single registration action
- **Channels:** partner communities, relevant newsletters, directories of
  events/communities, past-attendee referral
- **Measurement:** registration-to-attendance rate, return/renewal rate,
  referral source of attendees
- **Buying process:** time- and commitment-sensitive; objections cluster on
  "will this be worth the time"
- **Proof:** past attendee names/quotes, concrete agenda or format detail,
  photos or recordings from prior instances
- **Retention:** return rate for recurring events, renewal rate for ongoing
  communities

### Marketplace

- **Funnel:** qualified supply + qualified demand → match → transaction →
  repeat liquidity
- **Conversion asset:** two conversion assets, one per side (supply
  onboarding, demand-side listing/search page) — treat them as separate
  components in `pipeline-state.json`
- **Channels:** side-specific — supply-side channels (industry
  communities, directories for the supplier type) differ from demand-side
  channels (where buyers already look)
- **Measurement:** liquidity (successful match rate), time-to-first-match,
  repeat-transaction rate per side
- **Buying process:** both sides must clear trust and volume thresholds
  independently before a transaction is likely
- **Proof:** side-specific — supply needs proof demand exists and vice versa;
  a marketplace with only demand-side proof is missing half its argument
- **Retention:** repeat liquidity on both sides, not just first transaction

### Nonprofit

- **Funnel:** awareness → engagement (subscribe/volunteer/attend) →
  contribution → repeat contribution/advocacy
- **Conversion asset:** a donation or engagement landing page with a single
  clear ask
- **Channels:** partner organizations, relevant press and directories,
  community and advocacy networks, donor/volunteer referral
- **Measurement:** contribution conversion rate, donor/volunteer retention,
  average gift size where applicable — never inflate impact numbers past what
  is actually measured (see `references/evidence-policy.md`)
- **Buying process:** mission and trust driven; objections cluster on
  "where does the money/time actually go"
- **Proof:** specific, verifiable impact statements, financial transparency,
  named beneficiaries or programs where consent allows
- **Retention:** repeat-donor or repeat-volunteer rate, not a single gift
