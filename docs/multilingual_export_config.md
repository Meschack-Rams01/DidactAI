
# Export configuration recommendations for multilingual support

## ReportLab PDF Configuration:
- Use built-in fonts that support Unicode
- For advanced scripts, register custom fonts
- Set proper encoding in canvas

## python-docx Configuration:  
- UTF-8 encoding is default and works well
- Supports all Unicode characters
- No additional configuration needed

## HTML Export Configuration:
- Use CSS font-family with fallbacks
- Include proper charset meta tag
- Use system fonts as fallbacks

## Recommended CSS for multilingual content:
font-family: 
  'Noto Sans', 
  'Arial Unicode MS', 
  'Times New Roman', 
  'SimSun',           /* Chinese */
  'MS Gothic',        /* Japanese */
  'Malgun Gothic',    /* Korean */ 
  'Tahoma',           /* Arabic */
  'Mangal',           /* Hindi */
  Arial, 
  sans-serif;
