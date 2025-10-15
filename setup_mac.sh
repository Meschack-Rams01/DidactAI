#!/bin/bash
# DidactAI macOS Setup Script
# Run: chmod +x setup_mac.sh && ./setup_mac.sh

echo "ðŸŽ Setting up DidactAI on macOS..."
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "✓Œ Python 3 not found. Installing via Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "ðŸ“¦ Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install Python
    brew install python
else
    echo "✓œ… Python 3 found: $(python3 --version)"
fi

# Create virtual environment
echo "ðŸ”§ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "ðŸ”„ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "ðŸ“¦ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "ðŸ“š Installing project dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "ðŸ“ Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓œ… .env file created from template"
else
    echo "✓š ï¸  .env file already exists, skipping..."
fi

echo ""
echo "ðŸŽ‰ Setup Complete!"
echo "=================="
echo ""
echo "ðŸ“ Next Steps:"
echo "1. Edit your environment file with API keys:"
echo "   nano .env"
echo ""
echo "2. Run database migrations:"
echo "   python3 manage.py migrate"
echo ""
echo "3. Create a superuser account:"
echo "   python3 manage.py createsuperuser"
echo ""
echo "4. Start the development server:"
echo "   python3 manage.py runserver"
echo ""
echo "5. Open your browser to:"
echo "   http://localhost:8000"
echo ""
echo "ðŸ”‘ Don't forget to add your API keys to .env:"
echo "   - GEMINI_API_KEY=your-gemini-api-key"
echo "   - HUGGINGFACE_API_TOKEN=your-huggingface-token"
echo ""
echo "✓œ¨ Happy coding! Your DidactAI AI platform is ready!"
