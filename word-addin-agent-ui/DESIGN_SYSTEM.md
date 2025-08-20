# Novitai Word Add-in Design System

## Overview
This document outlines the design system implemented for the Novitai Word Add-in, which is an **exact copy** of the professional design from the existing `myword-addin`. The design follows Microsoft Fluent UI principles and maintains the same layout, spacing, and styling that was proven to work well.

## Design Philosophy

**"If it ain't broke, don't fix it"** - We've copied the exact design from your working Word add-in to ensure the same professional appearance and user experience.

## Brand Colors

### Primary Colors
- **Novitai Blue**: `#0078d4` - Primary brand color, used for buttons, links, and accents
- **Novitai Blue Dark**: `#005a9e` - Hover states and secondary actions
- **Microsoft Fluent UI**: Exact color scheme from the original add-in

### Surface Colors
- **Surface**: `#ffffff` - Primary background for cards and content areas
- **Background**: `#f9f9f9` - Main application background (exact from old add-in)
- **Border**: `#e1e1e1` - Subtle borders and dividers

### Text Colors
- **Primary Text**: `#242424` - Main text color for headings (exact from old add-in)
- **Secondary Text**: `#323130` - Secondary information and labels
- **Muted Text**: `#605e5c` - Timestamps and less important text

## Typography

### Font Family
- **Primary**: `'Segoe UI', sans-serif` - Microsoft's professional system font (exact from old add-in)
- **Fallback**: `-apple-system, BlinkMacSystemFont, 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif`

### Font Sizes (Exact from Old Add-in)
- **Small**: `12px` - Footer text
- **Body**: `14px` - Standard text content
- **Large**: `18px` - Section headings
- **XL**: `24px` - Main headers

## Layout & Spacing (Exact from Old Add-in)

### Container Spacing
- **Padding**: `24px` - Standard container padding
- **Margin**: `20px` - Standard element spacing
- **Gap**: `16px` - Standard spacing between elements

### Border Radius
- **Small**: `4px` - Input fields
- **Medium**: `6px` - Standard elements
- **Large**: `8px** - Buttons
- **XL**: `12px` - Cards and panels

### Shadows
- **Subtle**: `0 2px 8px rgba(0,0,0,0.05)` - Cards and content areas (exact from old add-in)

## Component Design (Exact Copy from Old Add-in)

### Buttons
- **Primary**: Blue background (`#0078d4`) with white text, 8px border radius
- **Hover Effects**: Darker blue (`#005a9e`) with slight upward movement
- **Padding**: `10px 16px` - Exact from old add-in

### Cards & Panels
- **Background**: White surface with subtle borders
- **Shadows**: `0 2px 8px rgba(0,0,0,0.05)` - Exact from old add-in
- **Padding**: `20px` - Exact from old add-in

### Input Fields
- **Border**: `1px solid #c8c6c4` - Exact from old add-in
- **Focus Ring**: Blue focus indicator with subtle shadow
- **Padding**: `10px` - Exact from old add-in

### Login Form
- **Layout**: Full-width container with left-aligned text (exact from old add-in)
- **Header**: 24px font with bottom border (exact from old add-in)
- **Description**: White card with 20px padding (exact from old add-in)
- **Button**: Full-width blue button (exact from old add-in)

## Implementation Notes

### Why This Design Works
1. **Proven**: This exact design was already working perfectly in your old add-in
2. **Familiar**: Users expect this Microsoft Office-style interface
3. **Professional**: Clean, enterprise-grade appearance
4. **Consistent**: Follows Microsoft Fluent UI design principles

### CSS Structure
- **LoginForm.css**: Exact copy of the old add-in styling
- **App.css**: Simplified layout matching the old add-in
- **Global.css**: Microsoft Fluent UI button styles

## File Structure

```
src/styles/
├── global.css          # Microsoft Fluent UI button styles
├── App.css            # Simplified layout (exact from old add-in)
└── components/
    ├── ChatBot.css    # Chat interface styling
    ├── MessageBubble.css # Message display styling
    ├── LoginForm.css  # EXACT COPY from old add-in
    ├── InsertButton.css # Action button styling
    └── DocumentPanel.css # Document info styling
```

## Design Principles

1. **Exact Copy**: Replicate the working design from your old add-in
2. **Microsoft Office**: Follow Fluent UI design patterns
3. **Professional**: Enterprise-grade appearance
4. **Consistent**: Unified design language across components
5. **Proven**: Use what already works well
