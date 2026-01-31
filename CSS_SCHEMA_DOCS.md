# CSS and Schema Documentation

## Overview
This document describes the CSS styling and Schema.org NewsArticle structured data added to the Auto News site.

## Features Added

### 1. CSS Styling (`assets/css/style.css`)

#### Post Styling
- **Clean, modern design** with a card-based layout
- **Responsive typography** that scales on mobile devices
- **Professional color scheme** with blue accent (#0066cc)
- **Readable font** using system font stack
- **Shadow and border effects** for visual hierarchy

#### Key CSS Classes:
- `.post` - Main article container
- `.post-header` - Post header with title and metadata
- `.post-title` - Article headline (2.2rem, bold)
- `.post-meta` - Date and source information
- `.post-content` - Main article body text
- `.post-list` - Home page post listing
- `.home-header` - Home page header section

#### Responsive Breakpoints:
- Desktop: 800px max-width container
- Tablet: 768px and below
- Mobile: 480px and below

### 2. NewsArticle Schema (`_layouts/post.html`)

#### Schema.org Structured Data
Each post includes both **Microdata** and **JSON-LD** formats for maximum compatibility:

**Microdata Attributes:**
```html
<article itemscope itemtype="http://schema.org/NewsArticle">
  <h1 itemprop="headline">...</h1>
  <time itemprop="datePublished">...</time>
  <div itemprop="articleBody">...</div>
</article>
```

**JSON-LD Structured Data:**
```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "...",
  "datePublished": "...",
  "dateModified": "...",
  "author": {...},
  "publisher": {...},
  "description": "..."
}
```

### 3. Layout Structure

#### Post Layout (`_layouts/post.html`)
- Extends default layout
- Includes NewsArticle schema markup
- Displays title, date, source link
- Structured content area
- SEO-optimized metadata

#### Home Layout (`_layouts/home.html`)
- Lists all posts chronologically
- Shows post title, date, and source
- Displays post excerpt (first 200 characters)
- Styled with post-list classes

#### Default Layout (`_layouts/default.html`)
- Base HTML structure
- Includes custom CSS
- Bot tracker integration
- Responsive viewport meta tag

## Benefits

### SEO & Rich Snippets
- **Google Rich Results**: Posts can appear with enhanced snippets in search
- **Structured Data**: Helps search engines understand content
- **Social Sharing**: Better previews when shared on social media

### User Experience
- **Readable Typography**: Optimized for reading long-form content
- **Mobile-Friendly**: Responsive design works on all devices
- **Professional Appearance**: Clean, modern design builds trust
- **Fast Loading**: Minimal CSS, no external dependencies

### Accessibility
- **Semantic HTML**: Proper use of article, header, time elements
- **ARIA Compatible**: Schema markup supports assistive technologies
- **High Contrast**: Good color contrast ratios for readability

## Testing Schema Markup

Use these tools to validate the schema implementation:

1. **Google Rich Results Test**: https://search.google.com/test/rich-results
2. **Schema Markup Validator**: https://validator.schema.org/
3. **Google Search Console**: Monitor rich results performance

## Customization

### Changing Colors
Edit `assets/css/style.css`:
- Main accent: `#0066cc` (blue)
- Text: `#333` (dark gray)
- Background: `#f5f5f5` (light gray)
- Links: `#0066cc` / `#004499` (hover)

### Adjusting Typography
- Base font size: `1.1rem` for content
- Line height: `1.8` for readability
- Heading sizes: Scale from `1.5rem` to `2.5rem`

### Layout Width
- Max width: `800px` (centered)
- Padding: `40px` desktop, `20px` mobile

## Browser Support
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support
- Internet Explorer 11: Partial support (basic layout works)
