import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Try to import firecrawl; if missing, print helpful error
try:
    from firecrawl import Firecrawl
except ImportError:
    print("Error: firecrawl package is not installed.")
    print("Please run: pip install firecrawl-py")
    exit(1)

def extract_brand_info(url):
    # Load .env variables
    workspace_root = Path(__file__).parent.parent.parent
    env_path = workspace_root / ".env"
    load_dotenv(dotenv_path=env_path)
    
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key or api_key == "fc-YOUR-API-KEY-HERE":
        print("Error: FIRECRAWL_API_KEY is missing or not set in .env file.")
        exit(1)
        
    try:
        app = Firecrawl(api_key=api_key)
        
        print(f"Scraping {url} for branding information...")
        # According to docs, formats can include branding, markdown, images
        result = app.scrape(
            url,
            formats=["branding", "markdown", "images"]
        )
        
        # Make sure .tmp/ directory exists
        tmp_dir = workspace_root / ".tmp"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        
        # Save output
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        output_file = tmp_dir / f"{domain}_branding.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            
        print(f"Success! Extracted data saved to {output_file.absolute()}")
        
        if 'branding' in result:
            print("\nExtracted Branding Profile Overview:")
            brand = result['branding']
            print(f"- Logo: {brand.get('logo')}")
            print(f"- Colors: {json.dumps(brand.get('colors', {}))}")
            fonts = [f.get('family') for f in brand.get('fonts', [])] if brand.get('fonts') else []
            print(f"- Fonts: {', '.join(fonts)}")
            
            # Generate Markdown Guidelines
            md_lines = [f"# Brand Guidelines: {domain}", ""]
            
            if brand.get('logo'):
                md_lines.extend([f"![Logo]({brand.get('logo')})", ""])
            
            md_lines.extend(["## Colors", ""])
            colors = brand.get('colors', {})
            for name, hex_val in colors.items():
                md_lines.append(f"- **{name.capitalize()}**: `{hex_val}`")
            md_lines.append("")
            
            md_lines.extend(["## Typography", ""])
            if fonts:
                md_lines.append(f"**Font Families**: {', '.join(fonts)}")
                md_lines.append("")
                
            typography = brand.get('typography', {})
            if typography:
                if 'fontSizes' in typography:
                    md_lines.append("### Font Sizes")
                    for tag, size in typography['fontSizes'].items():
                        md_lines.append(f"- **{tag}**: `{size}`")
                    md_lines.append("")
                
            md_lines.extend(["## Components", ""])
            components = brand.get('components', {})
            for comp_name, comp_styles in components.items():
                md_lines.append(f"### {comp_name.capitalize()}")
                for style_key, style_val in comp_styles.items():
                    md_lines.append(f"- **{style_key}**: `{style_val}`")
                md_lines.append("")
                
            md_lines.extend(["## Images", ""])
            images = brand.get('images', {})
            for img_name, img_url in images.items():
                md_lines.append(f"- **{img_name.capitalize()}**: {img_url}")
            md_lines.append("")
            
            ref_dir = workspace_root / "brand_guidelines"
            ref_dir.mkdir(parents=True, exist_ok=True)
            
            md_file = ref_dir / f"{domain}_guidelines.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_lines))
                
            print(f"Generated Markdown Guidelines saved to {md_file.absolute()}")

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract brand identity from a website.")
    parser.add_argument("url", help="The URL to scrape for branding info")
    args = parser.parse_args()
    
    extract_brand_info(args.url)
