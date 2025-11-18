"""
Google Sheets integration for article scoring app.
Allows importing articles directly from publicly shared Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
import os
import re


class GoogleSheetsImporter:
    """Handle Google Sheets imports with public URL access"""
    
    def __init__(self, credentials_json=None):
        """
        Initialize Google Sheets client
        
        Args:
            credentials_json: Path to service account JSON or JSON string from env var
        """
        self.client = None
        self.use_service_account = False
        
        # Try to use service account if credentials provided
        if credentials_json:
            try:
                if os.path.exists(credentials_json):
                    # Load from file
                    creds = Credentials.from_service_account_file(
                        credentials_json,
                        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
                    )
                else:
                    # Load from JSON string (for environment variable)
                    creds_dict = json.loads(credentials_json)
                    creds = Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
                    )
                
                self.client = gspread.authorize(creds)
                self.use_service_account = True
            except Exception as e:
                print(f"Could not load service account credentials: {e}")
                print("Falling back to public sheet access")
    
    def extract_sheet_id(self, url):
        """
        Extract Google Sheet ID from various URL formats
        
        Args:
            url: Google Sheets URL
            
        Returns:
            Sheet ID string or None
        """
        patterns = [
            r'/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Standard URL
            r'docs.google.com/spreadsheets/d/([a-zA-Z0-9-_]+)',  # Full URL
            r'^([a-zA-Z0-9-_]{30,})$',  # Just the ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def parse_public_sheet(self, url):
        """
        Parse a publicly shared Google Sheet without authentication
        
        Args:
            url: Google Sheets URL (must be publicly accessible)
            
        Returns:
            pandas DataFrame with sheet data
        """
        # Extract sheet ID
        sheet_id = self.extract_sheet_id(url)
        if not sheet_id:
            raise ValueError("Invalid Google Sheets URL")
        
        # Construct CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        try:
            # Read directly from CSV export URL
            df = pd.read_csv(csv_url)
            return df
        except Exception as e:
            raise ValueError(f"Could not access Google Sheet. Make sure it's set to 'Anyone with the link can view': {str(e)}")
    
    def parse_authenticated_sheet(self, url, sheet_name=None):
        """
        Parse Google Sheet using service account authentication
        
        Args:
            url: Google Sheets URL
            sheet_name: Optional worksheet name (default: first sheet)
            
        Returns:
            pandas DataFrame with sheet data
        """
        if not self.client:
            raise ValueError("No service account credentials configured")
        
        # Extract sheet ID
        sheet_id = self.extract_sheet_id(url)
        if not sheet_id:
            raise ValueError("Invalid Google Sheets URL")
        
        try:
            # Open the spreadsheet
            spreadsheet = self.client.open_by_key(sheet_id)
            
            # Get worksheet
            if sheet_name:
                worksheet = spreadsheet.worksheet(sheet_name)
            else:
                worksheet = spreadsheet.sheet1  # First sheet
            
            # Get all values
            data = worksheet.get_all_values()
            
            # Convert to DataFrame
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            raise ValueError(f"Could not access Google Sheet: {str(e)}")
    
    def import_sheet(self, url, sheet_name=None):
        """
        Import Google Sheet, trying authenticated access first, then public
        
        Args:
            url: Google Sheets URL
            sheet_name: Optional worksheet name
            
        Returns:
            pandas DataFrame with sheet data
        """
        # Try authenticated access first if available
        if self.use_service_account:
            try:
                return self.parse_authenticated_sheet(url, sheet_name)
            except Exception as e:
                print(f"Authenticated access failed: {e}")
                print("Trying public access...")
        
        # Fall back to public access
        return self.parse_public_sheet(url)


def create_google_sheets_importer():
    """
    Factory function to create GoogleSheetsImporter with credentials from environment
    
    Returns:
        GoogleSheetsImporter instance
    """
    # Check for credentials in environment variable
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    
    if creds_json:
        return GoogleSheetsImporter(creds_json)
    else:
        # No credentials - will use public access only
        return GoogleSheetsImporter()


# Global importer instance
_importer = None


def get_sheets_importer():
    """Get or create the global Google Sheets importer instance"""
    global _importer
    if _importer is None:
        _importer = create_google_sheets_importer()
    return _importer
