# UI/UX QA Notes — Premium Landing Redesign

## Current prototype problems found
- Overbuilt information architecture: separate brochure, inventory, and order pages made the experience feel unfinished instead of premium.
- Visual jank: heavy deadwood background, large rounded panels, 3D objects, and generated-food imagery competed with the core sales message.
- Copy was too implementation-focused: “mocked AI”, “3D transition concept”, and internal caveats should not lead a customer-facing site.
- Too many equal-weight sections: every block looked similarly important, so the page had no controlled conversion path.
- Motion dependency: Three.js added load risk and visual noise without helping customers order meat or seafood.

## Redesign direction
Surface archetype: **Decide / Learn** landing page.

The revised UX is a single premium landing page with one clear conversion path: understand the offer, see the selection categories, then request an order. It removes the 3D model, removes the mocked chatbot from the customer journey, and turns the order flow into a concierge request form.

## Slop diagnostic after redesign
Score: **1 / 10**
- Default type risk remains partly because we use a CDN substitute, but the type system is intentionally premium and controlled.
- No tech gradients, generic feature tiles, icon toppers, glassmorphism-as-decoration, monument stats, or wrong-surface dashboard content.

## Remaining content gaps
- Real logo asset.
- Official menu/brochure/pricing.
- Real photography if available.
- Backend destination for form submissions.
