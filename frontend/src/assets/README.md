# Assets Directory

## Images

This directory is reserved for static assets such as:
- Product images
- Icons
- Logos
- Backgrounds
- Other media files

## Current Setup

The application currently uses external image URLs for product images. 

### To Add Local Images:

1. **Create subdirectories**:
   ```
   assets/
   ├── images/
   │   ├── products/      # Product photos
   │   ├── icons/         # UI icons
   │   └── logo/          # Brand logo
   └── styles/            # Already contains global styles
   ```

2. **Import in components**:
   ```javascript
   import productImage from '../assets/images/products/headphones.jpg'
   
   <img src={productImage} alt="Product name" />
   ```

3. **Or use public folder** (for static references):
   ```
   frontend/public/images/logo.png
   ```
   
   Then reference directly:
   ```jsx
   <img src="/images/logo.png" alt="Logo" />
   ```

## Recommended Image Sizes

### Product Images
- **Grid View**: 500x500px (1:1 aspect ratio)
- **Card View**: 300x300px
- **Thumbnail**: 100x100px
- **Format**: WebP or JPEG
- **Max Size**: 200KB per image

### Icons
- **Standard**: 24x24px, 48x48px
- **Format**: SVG (preferred) or PNG
- **Style**: Consistent line weight and design language

## Optimization Tips

1. **Compress images** before adding:
   - Use tools like TinyPNG, Squoosh
   - Aim for < 200KB per product image

2. **Use responsive images**:
   ```html
   <img 
     src="product-small.jpg" 
     srcset="product-large.jpg 2x"
     alt="Product"
   />
   ```

3. **Lazy loading** for better performance:
   ```jsx
   <img loading="lazy" src={image} alt="Product" />
   ```

## Placeholder Images

For development, you can use placeholder services:
- `https://via.placeholder.com/500x500`
- `https://picsum.photos/500/500`
- `https://source.unsplash.com/random/500x500?product`

---

**Note**: The current implementation uses Unsplash source URLs for demo purposes. Replace with actual product images for production.
