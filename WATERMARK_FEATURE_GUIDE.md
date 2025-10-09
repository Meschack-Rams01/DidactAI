# Watermark Feature - User Guide

## Overview
The DidactAI platform now supports watermarks in exported documents. This feature allows you to add text overlays (like "CONFIDENTIAL", "DRAFT", "SAMPLE") to your exported quizzes and exams for document security and identification purposes.

## How to Use Watermarks

### Step 1: Access the Export Form
1. Generate a quiz or exam using the AI Generator
2. Click on "Export" from the generation view
3. Fill in the export form details

### Step 2: Add Watermark Text
In the "Additional Customization" section of the export form:
1. Find the "Watermark Text" field
2. Enter your desired watermark text (e.g., "CONFIDENTIAL", "DRAFT", "SAMPLE")
3. Leave blank if you don't want a watermark

### Step 3: Export Your Document
Choose your preferred format and click "Create Export". The watermark will be applied automatically.

## Watermark Implementation by Format

### PDF Documents
- **Style**: Large diagonal watermark across the page
- **Properties**: 
  - 45-degree rotation
  - Semi-transparent gray color (30% opacity)
  - Large font size (48pt)
  - Positioned behind content (non-intrusive)
- **Visibility**: Visible in both digital viewing and printing

### DOCX Documents  
- **Style**: Small watermark text in document footer
- **Properties**:
  - Centered in footer
  - Small font size (8pt)
  - Light gray color
  - Format: `[WATERMARK_TEXT]`
- **Visibility**: Appears on every page in the footer

### HTML Documents
- **Style**: Large diagonal overlay watermark
- **Properties**:
  - CSS-based implementation
  - 45-degree rotation
  - Semi-transparent (20% opacity)
  - Fixed position overlay
  - Visible in both screen and print view
- **Visibility**: Always visible but non-intrusive

## Example Use Cases

### Academic Security
- **"CONFIDENTIAL"** - For sensitive exam materials
- **"DRAFT"** - For preliminary versions requiring review
- **"SAMPLE"** - For demonstration or training purposes

### Version Control
- **"VERSION 1.0"** - For document versioning
- **"PRELIMINARY"** - For early drafts
- **"FINAL EXAM"** - For official exam versions

### Institution Branding
- **"UNIVERSITY OF XYZ"** - For institutional identification
- **"DEPARTMENT COPY"** - For internal distribution
- **"INSTRUCTOR USE ONLY"** - For access restriction

## Technical Details

### Implementation
The watermark feature is implemented across all export formats:
- **PDF**: Uses ReportLab canvas drawing with transparency
- **DOCX**: Uses python-docx footer formatting
- **HTML**: Uses CSS positioning and transparency

### Performance Impact
- Minimal impact on export speed
- No significant increase in file sizes
- Compatible with all existing features

### Limitations
- Watermark text should be kept reasonably short (1-3 words work best)
- Very long watermark text may not display optimally
- Watermark appearance may vary slightly between formats

## Troubleshooting

### Watermark Not Appearing
1. **Check the form field**: Ensure you entered text in the "Watermark Text" field
2. **Verify export format**: All formats (PDF, DOCX, HTML) support watermarks
3. **Check browser/viewer**: Some PDF viewers may not show transparency properly

### Watermark Too Visible/Not Visible Enough
The watermark opacity and styling are optimized for readability while maintaining document usability. If adjustments are needed, contact your system administrator.

### Format-Specific Issues
- **PDF**: Watermark uses transparency, ensure your PDF viewer supports it
- **DOCX**: Watermark appears in footer - check document footer settings
- **HTML**: Watermark uses CSS - ensure CSS is enabled in your browser

## Best Practices

### Text Selection
- Use UPPERCASE for better visibility
- Keep text short and meaningful
- Common examples: "CONFIDENTIAL", "DRAFT", "SAMPLE"

### Document Security
- Watermarks provide visual indication but are not security features
- For true document security, use additional measures like password protection
- Watermarks can be helpful for document identification and tracking

### Professional Use
- Choose watermark text that aligns with your institution's standards
- Be consistent across similar document types
- Consider using watermarks for version control

## Integration with Other Features

### University Branding
- Watermarks work alongside university logos and branding
- Both features can be used simultaneously
- Watermarks complement rather than replace institutional branding

### Multi-Version Exports
- When creating multiple versions (A, B, C), watermarks apply to all versions
- Consider adding version information to watermark text if needed
- ZIP exports include watermarks in all contained formats

### Answer Keys
- Answer key exports also include watermarks when specified
- Helps maintain consistency across related documents
- Useful for distinguishing student and instructor versions

---

**Note**: This feature was implemented to enhance document identification and security. For technical support or feature requests, contact your DidactAI administrator.
