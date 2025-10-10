# Ultimate Template Corruption Fixer
Write-Host "🚀 ULTIMATE Template Corruption Fixer for DidactAI" -ForegroundColor Green
Write-Host "=" * 60
Write-Host "Fixing ALL character corruption issues in templates..." -ForegroundColor Yellow
Write-Host ""

$totalFiles = 0
$fixedFiles = 0

# Get all HTML files in templates directory
$templateFiles = Get-ChildItem -Path ".\templates" -Filter "*.html" -Recurse

Write-Host "📋 Found $($templateFiles.Count) template files to check" -ForegroundColor Cyan
Write-Host ""

foreach ($file in $templateFiles) {
    $totalFiles++
    $changed = $false
    $changes = @()
    
    Write-Progress -Activity "Fixing Templates" -Status "Processing $($file.Name)" -PercentComplete (($totalFiles / $templateFiles.Count) * 100)
    
    try {
        # Read file content
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Fix specific corruptions
        $replacements = @{
            'â†' = '←'                    # Left arrow corruption
            'à¤' = '←'                    # Another left arrow variant
            'â€¢' = '•'                   # Bullet point corruption
            'öŸZ' = ''                    # Remove öŸZ corruption
            'öŸ"' = ''                    # Remove öŸ" corruption
            'Ã°Å¸â€œâ€ž' = '📄'           # Document emoji corruption
            'Ã°Å¸â€œâ€‹' = '📋'           # Clipboard emoji corruption
            'â€œ' = '"'                   # Left double quote
            'â€' = '"'                    # Right double quote variant
            'â€™' = "'"                   # Right single quote
            'â€˜' = "'"                   # Left single quote
            'â€"' = '—'                   # Em dash
            'â€"' = '–'                   # En dash
            'â€¦' = '…'                   # Ellipsis
            'Â' = ''                      # Non-breaking space corruption
            'ÃÂ' = ''                     # Double encoding corruption
            'Ã¢â‚¬' = ''                  # Complex corruption pattern
            'â‚¬' = ''                    # Euro symbol corruption
        }
        
        # Apply replacements
        foreach ($corruption in $replacements.Keys) {
            if ($content.Contains($corruption)) {
                $count = ([regex]::Matches($content, [regex]::Escape($corruption))).Count
                $content = $content.Replace($corruption, $replacements[$corruption])
                $changes += "'$corruption' → '$($replacements[$corruption])' ($count times)"
                $changed = $true
            }
        }
        
        # Fix question mark sequences before Export/Enhanced/Quick
        $patterns = @{
            '\?{2,}\s*(Export|Enhanced|Quick)' = '📄 $1'
            '[^\w\s]{3,}\s*(Export to PDF)' = '📄 $1'
            '[^\w\s]{3,}\s*(Quick Export)' = '📋 $1'
            '[^\w\s]{3,}\s*(Enhanced Export)' = '📄 $1'
            '[\x80-\xFF]{3,}' = ''
            '[^\w\s<>="''-]{2,}\s*(Enhanced|Export|Quick|Back)' = '$1'
        }
        
        foreach ($pattern in $patterns.Keys) {
            $newContent = $content -replace $pattern, $patterns[$pattern]
            if ($newContent -ne $content) {
                $content = $newContent
                $changes += "Pattern '$pattern' applied"
                $changed = $true
            }
        }
        
        # Write back if changes were made
        if ($changed) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
            $fixedFiles++
            Write-Host "✅ Fixed $($file.Name):" -ForegroundColor Green
            $changes | Select-Object -First 3 | ForEach-Object { Write-Host "   - $_" -ForegroundColor White }
            if ($changes.Count -gt 3) {
                Write-Host "   - and $($changes.Count - 3) more fixes..." -ForegroundColor Gray
            }
            Write-Host ""
        }
    }
    catch {
        Write-Host "❌ Error processing $($file.Name): $_" -ForegroundColor Red
    }
}

Write-Progress -Activity "Fixing Templates" -Completed

Write-Host ""
Write-Host "🎯 FINAL RESULTS:" -ForegroundColor Green
Write-Host "=" * 40
Write-Host "📊 Total HTML files checked: $totalFiles" -ForegroundColor Cyan
Write-Host "🔧 Files with corruption fixed: $fixedFiles" -ForegroundColor Green

if ($fixedFiles -gt 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Fixed corruption in $fixedFiles files!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Restart Django server: python manage.py runserver" -ForegroundColor White
    Write-Host "2. Clear browser cache: Ctrl+Shift+Delete" -ForegroundColor White
    Write-Host "3. Hard refresh pages: Ctrl+F5" -ForegroundColor White
    Write-Host "4. All character corruption should be FIXED! ✅" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✅ No corruption found - templates are clean!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎊 Character corruption fix COMPLETE!" -ForegroundColor Magenta