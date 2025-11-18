# 🎯 AI Article Credibility Scoring Web App

A web-based application for evaluating AI news articles across 5 key credibility dimensions. Features password protection, collaborative scoring, and comprehensive export options.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)

## 🌟 Features

- **📊 Rubric-Based Scoring** - 5 comprehensive categories (1-10 scale)
- **🔒 Password Protected** - Secure access control
- **👥 Collaborative** - Multiple users can score simultaneously
- **📱 Mobile Responsive** - Works on all devices
- **📤 Import Support** - CSV, Excel, and TXT files
- **💾 Export Options** - TXT reports and JSON data
- **📈 Statistics Dashboard** - Track scoring progress
- **🔍 Search & Filter** - Find articles by score range

## 🚀 Live Demo

[Access the live app](https://your-app-name.onrender.com) (Password required)

## 📋 Scoring Categories

1. **Accuracy of Truthfulness** - Classification as True/Partially True/False
2. **Author & Source Credibility** - Publisher reputation and expertise
3. **Citation & Evidence Quality** - Quality of references
4. **Reasoning Transparency** - Logical coherence
5. **Confidence Calibration** - Alignment between claims and evidence

## 🛠️ Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-article-scoring.git
cd ai-article-scoring

# Install dependencies
pip install -r requirements_deploy.txt

# Run the app
python webapp_secure.py

# Access at http://localhost:5000
# Default password: scoring2025
```

### Environment Variables

```bash
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-secure-password
FLASK_ENV=production
```

## 🌐 Deployment

### Quick Deploy to Render.com (Free)

1. Fork this repository
2. Sign up at [Render.com](https://render.com)
3. Create new Web Service from your fork
4. Set environment variables
5. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Supported Platforms

- ✅ **Render.com** (Recommended - Free tier)
- ✅ **Railway.app** ($5/month)
- ✅ **PythonAnywhere** (Free tier available)
- ✅ **Heroku** ($5-7/month)
- ✅ **DigitalOcean** ($5/month)

## 📖 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[SQUARESPACE_HOSTING.md](SQUARESPACE_HOSTING.md)** - Integration with Squarespace
- **[WEBAPP_README.md](WEBAPP_README.md)** - Full feature documentation
- **[WEBAPP_QUICK_START.md](WEBAPP_QUICK_START.md)** - Get started in 3 steps
- **[GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)** - Import articles from Google Sheets

## 🔒 Security

- Password-protected access
- Session-based authentication
- HTTPS encryption (on hosting platforms)
- Configurable via environment variables

**⚠️ Important:** Change the default password before deployment!

## 💡 Usage

### Import Articles

Upload a file with article URLs or import directly from Google Sheets:

**Google Sheets:** Share your sheet publicly and paste the URL in the app. See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for details.

**CSV Format:**
```csv
URL,Title
https://example.com/article1,Article Title 1
https://example.com/article2,Article Title 2
```

**TXT Format:**
```
# Comments start with #
https://example.com/article1
https://example.com/article2,Custom Title
```

### Score Articles

1. Click "Score Article" on any card
2. Adjust 5 sliders (1-10 scale)
3. Add optional notes
4. Submit

### Export Results

- **TXT Format:** Individual reports in ZIP file
- **JSON Format:** Structured data for analysis

## 🤝 Collaboration

Multiple users can:
- Score articles independently
- View peer scores and statistics
- Compare ratings across categories
- Export combined results

## 📱 Mobile Support

Fully responsive design works on:
- 📱 Phones (iOS/Android)
- 💻 Tablets
- 🖥️ Desktops

## 🔗 Squarespace Integration

Add to your Squarespace site:

**Option 1:** Direct link in navigation
**Option 2:** Iframe embed
**Option 3:** Custom subdomain

See [SQUARESPACE_HOSTING.md](SQUARESPACE_HOSTING.md) for details.

## 🛣️ Roadmap

- [ ] OAuth authentication (Google, GitHub)
- [ ] PostgreSQL database support
- [ ] Real-time collaboration (WebSockets)
- [ ] Advanced analytics dashboard
- [ ] API for programmatic access
- [ ] Batch import/export
- [ ] User roles (admin, reviewer, viewer)

## 🤔 FAQ

**Q: Can I use this without Squarespace?**  
A: Yes! It's a standalone web app that works independently.

**Q: Is the data persistent?**  
A: Yes, with paid hosting plans. Free tiers may reset on restart.

**Q: Can I customize the scoring categories?**  
A: Yes, edit `webapp_secure.py` to modify categories.

**Q: How many users can score simultaneously?**  
A: Depends on hosting tier. Free tiers: 5-10 concurrent users.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with Flask
- Styled with custom CSS
- Deployed on Render.com
- Scoring rubric based on research standards

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/ai-article-scoring/issues)
- **Documentation:** See docs folder
- **Email:** your-email@example.com

## 🌟 Star This Repo

If you find this useful, please star the repository!

---

**Made with ❤️ for AI research and journalism evaluation**

## Screenshots

### Login Page
![Login](screenshots/login.png)

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Scoring Interface
![Scoring](screenshots/scoring.png)

### Peer Scores
![Peer Scores](screenshots/peer-scores.png)

---

## Quick Links

- 📖 [Full Documentation](WEBAPP_README.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)
- 🌐 [Squarespace Integration](SQUARESPACE_HOSTING.md)
- ⚡ [Quick Start](WEBAPP_QUICK_START.md)

**Ready to deploy?** Follow the [deployment guide](DEPLOYMENT.md)!



