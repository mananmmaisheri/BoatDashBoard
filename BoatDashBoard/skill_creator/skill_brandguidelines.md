---
name: brand-extractor
description: Use this skill whenever you need to build a new website inspired by an existing one, extract brand guidelines from a URL, pull typography, fonts, colors, and header images, or analyze a company's styling. Make sure to trigger this skill if the user asks you to match a website's look and feel, or pull down its visual identity for a new project.
---

# Brand Extractor Skill

This skill allows you to extract comprehensive visual identity and branding information from any website using Firecrawl's brand extraction format. 

## When to use this skill
- The user wants to build a new web app or website that matches an existing brand's style.
- You need to know the primary colors, typography, fonts, or UI styling of a specific URL.
- The user asks you to grab the header images or hero images from a site.
- You are reverse-engineering a design system from a live webpage.

## Dependencies
This skill relies on the `firecrawl-py` Python package.
The user must have `FIRECRAWL_API_KEY` set in their `.env` file at the root of the workspace.

## Execution

To extract the brand data, you will use the bundled Python script `scripts/extract_brand.py`.

Run it from the terminal:
```bash
python brand-extractor/scripts/extract_brand.py <URL>
```
Wait for the command to finish.

## Processing the Output

The script will scrape the target URL and save the raw extracted JSON data in the workspace `.tmp/` directory as `<domain>_branding.json`. It will also automatically generate a Markdown reference file in `brand_guidelines/<domain>_guidelines.md`.

1. **Read the Guidelines file**: You can open `brand_guidelines/<domain>_guidelines.md` to quickly see a nicely formatted version of the brand's colors, typography, components, and image URLs.
2. **Analyze the Raw Data**: If you need more structure, look inside the `branding` key of the JSON object in `.tmp/`. The data structure contains:
   - `colorScheme`: Usually `"light"` or `"dark"`.
   - `colors`: Includes `primary`, `secondary`, `accent`, `background`, `textPrimary`, etc.
   - `typography`: Font families (e.g., primary, heading), font sizes (e.g., h1, body), and weights.
   - `spacing`: Base units and border radius.
   - `components`: Styles for buttons and inputs (backgrounds, text colors, borders).
   - `images`: Logo, favicon, ogImage, and other header/hero images extracted from the page.

## Presenting to the User

Once you have the brand profile:
1. **Summarize**: Give the user a quick rundown of the color palette (using hex codes), the font families, and the general vibe (e.g., dark mode, minimalist).
2. **Apply**: Use the extracted tokens (colors, fonts, border radii) when you write CSS or Tailwind classes to build the new website the user requested. Don't just list the colors—actually use them in the code you write next!
3. **Images**: Share the URLs of the logo and hero images so the user knows what assets are available.

If the user is asking you to build a website, immediately proceed to use the extracted information to generate their HTML/CSS/JS or framework code. Ensure the final result deeply reflects the brand identity you just extracted!
